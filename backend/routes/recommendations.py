"""
Recommendations API routes
POST /recommend - Get artwork recommendations
"""

import time
import json
import random
import asyncio
from pathlib import Path
from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from models.recommendation import (
    RecommendationRequest,
    RecommendationResponse,
    ArtworkRecommendation,
)
from db.faiss_client import get_faiss_client
from db.supabase_client import get_supabase_client
from agents.trend_intel_agent import TrendIntelAgent
from agents.chat_agent import get_chat_agent
from agents.store_inventory_agent import get_store_inventory_agent
from agents.geo_finder_agent import GeoFinderAgent

router = APIRouter(prefix="/api", tags=["Recommendations"])

# Initialize agents
trend_agent = TrendIntelAgent()
chat_agent = get_chat_agent()
store_agent = get_store_inventory_agent()
geo_agent = GeoFinderAgent()

# Load local catalog
LOCAL_CATALOG = []
LOCAL_CATALOG_PATH = Path(__file__).parent.parent / "data" / "local_catalog.json"

def load_local_catalog():
    """Load local catalog from JSON file"""
    global LOCAL_CATALOG
    if LOCAL_CATALOG_PATH.exists():
        with open(LOCAL_CATALOG_PATH, 'r') as f:
            LOCAL_CATALOG = json.load(f)
            print(f"✅ Loaded {len(LOCAL_CATALOG)} items from local catalog")
    else:
        print("⚠️  Local catalog not found. Run scripts/build_catalog.py first.")

# Load catalog on module import
load_local_catalog()


async def _process_artwork_recommendation(
    idx: int,
    artwork_meta: dict,
    match_score: float,
    request: RecommendationRequest,
):
    """
    Process a single artwork recommendation in parallel
    Fetches store data and generates AI reasoning
    """
    # Initialize with FAISS metadata
    title = artwork_meta.get('title', 'Untitled')
    artist = artwork_meta.get('artist', 'Unknown Artist')
    price = f"${artwork_meta.get('price', 0)}"
    image_url = artwork_meta.get('image_url', 'https://via.placeholder.com/400')
    thumbnail_url = artwork_meta.get('thumbnail_url')
    purchase_url = None
    download_url = None
    source = "Local Catalog"
    purchase_options = []
    print_on_demand = []
    
    # Fetch real store data with timeout protection
    try:
        # Build search query from FAISS metadata
        style = artwork_meta.get('style', 'modern')
        tags = artwork_meta.get('tags', [])
        
        if tags and len(tags) > idx:
            search_query = f"{style} {tags[idx]} wall art"
        elif tags:
            search_query = f"{style} {tags[0]} art print"
        else:
            variations = ['wall art', 'canvas print', 'framed art', 'poster print']
            search_query = f"{style} {variations[idx % len(variations)]}"
        
        print(f"🔍 Search #{idx+1}: {search_query}")
        
        # Fetch real store data (async - runs in parallel with timeout!)
        store_results = await asyncio.wait_for(
            store_agent.search_artwork(
                query=search_query,
                style=style,
                limit=1  # Only need 1 result per recommendation for speed
            ),
            timeout=3.0  # Max 3 seconds per search
        )
        
        # Use first result if available
        if store_results:
            real_item = store_results[0]
            title = real_item.get('title', title)
            artist = real_item.get('artist', artist)
            price = real_item.get('price', price)
            image_url = real_item.get('image_url', image_url)
            thumbnail_url = real_item.get('thumbnail_url', thumbnail_url)
            purchase_url = real_item.get('purchase_url')
            download_url = real_item.get('download_url')
            source = real_item.get('source')
            purchase_options = real_item.get('purchase_options', [])
            print_on_demand = real_item.get('print_on_demand', [])
            print(f"✅ Replaced with real store item: '{title}' from {source}")
    
    except asyncio.TimeoutError:
        print(f"⏱️  Store search timed out for item {idx} (>3s)")
    except Exception as e:
        print(f"⚠️  Store search failed for item {idx}: {e}")
    
    # Generate AI reasoning (async - runs in parallel!)
    try:
        reasoning = await chat_agent.generate_reasoning(
            artwork_title=artwork_meta.get('title', 'Untitled'),
            artwork_style=artwork_meta.get('style', 'Contemporary'),
            room_style=request.user_style or request.room_style,
            colors=request.color_preferences or request.colors,
            match_score=match_score,
            artwork_tags=artwork_meta.get('tags', [])
        )
    except Exception as e:
        print(f"⚠️  LLM reasoning failed for item {idx}: {e}")
        reasoning = f"This {artwork_meta.get('style', 'Contemporary').lower()} piece matches your room's aesthetic with a {match_score:.0f}% compatibility score."
    
    return ArtworkRecommendation(
        id=artwork_meta.get('id', 'unknown'),
        title=title,
        artist=artist,
        price=price,
        image_url=image_url,
        thumbnail_url=thumbnail_url,
        match_score=match_score,
        tags=artwork_meta.get('tags', []),
        reasoning=reasoning,
        stores=artwork_meta.get('stores', []),
        dimensions=artwork_meta.get('dimensions', 'Standard'),
        medium=artwork_meta.get('medium'),
        style=artwork_meta.get('style', 'Contemporary'),
        purchase_url=purchase_url,
        download_url=download_url,
        source=source,
        purchase_options=purchase_options,
        print_on_demand=print_on_demand
    )


def get_local_catalog_recommendations(style: str, limit: int = 3) -> list:
    """
    Get recommendations from local catalog
    Returns items matching the style
    """
    if not LOCAL_CATALOG:
        return []
    
    # Simple keyword matching for now
    style_keywords = style.lower().split()
    
    # Score each item based on keyword matches
    scored_items = []
    for item in LOCAL_CATALOG:
        score = 0
        item_text = f"{item['title']} {item['description']} {' '.join(item['tags'])}".lower()
        
        for keyword in style_keywords:
            if keyword in item_text:
                score += 1
        
        if score > 0:
            scored_items.append((score, item))
    
    # Sort by score and get top items
    scored_items.sort(key=lambda x: x[0], reverse=True)
    
    # If we have scored items, return them
    if scored_items:
        return [item for score, item in scored_items[:limit]]
    
    # Otherwise return random selection
    return random.sample(LOCAL_CATALOG, min(limit, len(LOCAL_CATALOG)))


@router.post("/nearby-stores")
async def get_nearby_stores(
    latitude: float,
    longitude: float,
    radius: int = 10000,
    store_type: str = "art_gallery"
):
    """
    Find nearby art stores and galleries
    
    Args:
        latitude: User's latitude
        longitude: User's longitude
        radius: Search radius in meters (default 10km)
        store_type: Type of store (art_gallery, home_goods_store, furniture_store)
    
    Returns:
        List of nearby stores with details
    """
    try:
        stores = await geo_agent.find_nearby_stores(
            latitude=latitude,
            longitude=longitude,
            radius=radius,
            store_type=store_type
        )
        
        return {
            "stores": stores,
            "total": len(stores),
            "search_location": {"latitude": latitude, "longitude": longitude},
            "radius_km": radius / 1000
        }
    except Exception as e:
        print(f"Error finding nearby stores: {e}")
        raise HTTPException(status_code=500, detail=f"Error finding stores: {str(e)}")


@router.post("/directions")
async def get_store_directions(
    origin_lat: float,
    origin_lng: float,
    dest_lat: float,
    dest_lng: float
):
    """
    Get directions from user location to store
    
    Args:
        origin_lat: User's latitude
        origin_lng: User's longitude
        dest_lat: Store's latitude
        dest_lng: Store's longitude
    
    Returns:
        Directions with distance, duration, and steps
    """
    try:
        directions = await geo_agent.get_directions(
            origin=(origin_lat, origin_lng),
            destination=(dest_lat, dest_lng)
        )
        
        return {
            "directions": directions,
            "origin": {"lat": origin_lat, "lng": origin_lng},
            "destination": {"lat": dest_lat, "lng": dest_lng}
        }
    except Exception as e:
        print(f"Error getting directions: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting directions: {str(e)}")


@router.post("/recommend/fast", response_model=RecommendationResponse)
async def get_fast_recommendations(request: RecommendationRequest):
    """
    FAST recommendations - Only FAISS search + local catalog (2-3 seconds)
    No external API calls, no AI reasoning, no trends
    Use this for initial fast display, then enrich with other APIs
    """
    try:
        start_time = time.time()
        
        # Query FAISS vector database for similar artworks
        faiss_client = get_faiss_client()
        recommendations = []
        
        if request.style_vector and len(request.style_vector) > 0:
            try:
                import numpy as np
                style_vector = np.array(request.style_vector, dtype=np.float32)
                distances, results = faiss_client.search(style_vector, k=request.limit)
                
                if results:
                    for idx, (dist, artwork_meta) in enumerate(zip(distances, results)):
                        similarity = 1.0 / (1.0 + dist)
                        match_score = similarity * 100
                        
                        # Simple template reasoning (fast, no LLM call)
                        reasoning = f"This {artwork_meta.get('style', 'contemporary').lower()} piece matches your room's aesthetic with a {match_score:.0f}% compatibility score."
                        
                        recommendations.append(ArtworkRecommendation(
                            id=artwork_meta.get('id', 'unknown'),
                            title=artwork_meta.get('title', 'Untitled'),
                            artist=artwork_meta.get('artist', 'Unknown Artist'),
                            price=f"${artwork_meta.get('price', 0)}",
                            image_url=artwork_meta.get('image_url', 'https://via.placeholder.com/400'),
                            thumbnail_url=artwork_meta.get('thumbnail_url'),
                            match_score=match_score,
                            tags=artwork_meta.get('tags', []),
                            reasoning=reasoning,
                            stores=[],
                            dimensions=artwork_meta.get('dimensions', 'Standard'),
                            medium=artwork_meta.get('medium'),
                            style=artwork_meta.get('style', 'Contemporary'),
                            purchase_url=None,
                            download_url=None,
                            source="FAISS Database",
                            purchase_options=[],
                            print_on_demand=[]
                        ))
            except Exception as e:
                print(f"FAISS search error: {e}")
        
        # Add local catalog items first
        room_style = request.user_style or request.room_style or "Modern"
        local_items = get_local_catalog_recommendations(room_style, limit=2)
        
        # Track image identifiers to avoid duplicates (extract photo ID from URL)
        def extract_photo_id(url):
            """Extract unique photo ID from image URL (handles Unsplash IDs, etc.)"""
            if not url:
                return url
            # For Unsplash: extract photo ID (e.g., tTEYELCR8OA from the URL)
            if 'unsplash.com' in url:
                import re
                # Match pattern like /photo-...-PHOTOID or /photos/PHOTOID
                match = re.search(r'/photo[s]?/[^/]*-([A-Za-z0-9_-]+)', url)
                if not match:
                    match = re.search(r'/photo-\d+-([A-Za-z0-9_-]+)\?', url)
                if match:
                    return match.group(1)
            # For other URLs, use the base URL without query params
            return url.split('?')[0]
        
        seen_photo_ids = set()
        seen_photo_ids.update([extract_photo_id(item['image_url']) for item in local_items])
        
        for item in local_items:
            reasoning = f"Expertly curated {item['category'].replace('_', ' ')} artwork that perfectly complements your {room_style.lower()} aesthetic. High-quality print available for instant download."
            recommendations.append(ArtworkRecommendation(
                id=item['id'],
                title=item['title'],
                artist=item['artist'],
                price=item['price'],
                image_url=item['image_url'],
                thumbnail_url=item['thumbnail_url'],
                style=item['category'].replace('_', ' ').title(),
                tags=item['tags'],
                dimensions=f"{item['width']}x{item['height']}",
                match_score=92.0,  # High score for curated items (was 85)
                reasoning=reasoning,
                download_url=item['download_url'],
                source="Local Catalog",
                purchase_options=[],
                print_on_demand=[{
                    'service': ps['name'],
                    'url': ps['url'],
                    'price': ps['price_from']
                } for ps in item['print_services']],
                attribution={
                    'text': item['attribution'],
                    'url': item['attribution_url']
                }
            ))
        
        # Add 1-2 online store results for variety (after local to avoid duplicates)
        try:
            # Quick search for 3 online results with aggressive timeout (we'll filter duplicates)
            online_results = await asyncio.wait_for(
                store_agent.search_artwork(
                    query=f"{room_style} wall art decor",
                    style=room_style,
                    limit=3
                ),
                timeout=2.0  # Max 2 seconds for online search
            )
            
            online_added = 0
            for online_item in online_results:
                image_url = online_item.get('image_url', '')
                
                # Skip if no valid image URL
                if not image_url or image_url == 'https://via.placeholder.com/400':
                    continue
                
                # Extract photo ID and check for duplicates
                photo_id = extract_photo_id(image_url)
                if photo_id in seen_photo_ids:
                    print(f"⚠️  Skipping duplicate image (ID: {photo_id}): {online_item.get('title', 'Unknown')}")
                    continue
                
                seen_photo_ids.add(photo_id)
                recommendations.append(ArtworkRecommendation(
                    id=online_item.get('id', f"online-{len(recommendations)}"),
                    title=online_item.get('title', 'Artwork'),
                    artist=online_item.get('artist', 'Various Artists'),
                    price=online_item.get('price', 'Price varies'),
                    image_url=image_url,
                    thumbnail_url=online_item.get('thumbnail_url'),
                    match_score=88.0,  # Slightly lower than local catalog
                    tags=online_item.get('tags', []),
                    reasoning="",  # Empty for skeleton loader
                    stores=[],
                    dimensions=online_item.get('dimensions'),
                    style=online_item.get('style', room_style),
                    purchase_url=online_item.get('purchase_url'),
                    source=online_item.get('source', 'Online'),
                    purchase_options=[]
                ))
                online_added += 1
                
                # Stop after adding 2 unique online items
                if online_added >= 2:
                    break
            
            print(f"✅ Added {online_added} unique online results (filtered {len(online_results) - online_added} duplicates)")
        except asyncio.TimeoutError:
            print(f"⏱️  Online search timed out (>2s), skipping")
        except Exception as e:
            print(f"⚠️  Online search failed: {e}, continuing with local only")
        
        # Sort by match score (highest first)
        recommendations.sort(key=lambda x: x.match_score, reverse=True)
        
        query_time = time.time() - start_time
        print(f"⚡ Fast recommendations returned in {query_time:.2f}s with {len(recommendations)} items")
        
        return RecommendationResponse(
            recommendations=recommendations[:request.limit],
            total_matches=len(recommendations),
            query_time=query_time,
            trends=[]
        )
    
    except Exception as e:
        print(f"Error in fast recommendations: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.post("/recommend", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    """
    Get personalized décor recommendations based on room analysis

    - **room_style**: Detected room style (e.g., "Modern Minimalist")
    - **colors**: List of dominant colors (hex format)
    - **lighting**: Lighting conditions
    - **user_preferences**: Optional user preferences
    - **price_range**: Optional price filter
    - **limit**: Number of recommendations (default: 10)

    Returns:
    - List of recommended artworks with match scores
    - AI reasoning for each recommendation
    - Local store availability
    - Current trending styles
    """
    try:
        start_time = time.time()

        # Get trending styles for context (pass room style for more relevant results)
        room_style = request.user_style or request.room_style
        try:
            trends = await trend_agent.get_trending_styles(location=room_style)
        except Exception as e:
            print(f"⚠️  Trends API failed: {e}")
            trends = []

        # Query FAISS vector database for similar artworks using style_vector
        faiss_client = get_faiss_client()
        recommendations = []

        # Try FAISS search if style_vector is provided
        if request.style_vector and len(request.style_vector) > 0:
            try:
                import numpy as np
                
                style_vector = np.array(request.style_vector, dtype=np.float32)
                
                # Search FAISS for similar artworks
                distances, results = faiss_client.search(style_vector, k=request.limit)
                
                # Convert FAISS results to recommendations using PARALLEL processing
                if results:
                    print(f"⚡ Processing {len(results)} recommendations in PARALLEL for speed...")
                    
                    # Create tasks for parallel execution
                    tasks = []
                    for idx, (dist, artwork_meta) in enumerate(zip(distances, results)):
                        similarity = 1.0 / (1.0 + dist)
                        match_score = similarity * 100
                        
                        # Create async task (don't await yet - will run in parallel!)
                        task = _process_artwork_recommendation(
                            idx=idx,
                            artwork_meta=artwork_meta,
                            match_score=match_score,
                            request=request
                        )
                        tasks.append(task)
                    
                    # Execute ALL tasks in parallel (10x faster!)
                    print(f"⏱️  Starting parallel execution of {len(tasks)} tasks...")
                    parallel_start = time.time()
                    recommendations = await asyncio.gather(*tasks, return_exceptions=True)
                    parallel_time = time.time() - parallel_start
                    
                    # Filter out any exceptions
                    recommendations = [r for r in recommendations if isinstance(r, ArtworkRecommendation)]
                    print(f"✅ Parallel processing complete in {parallel_time:.2f}s (was ~{len(tasks)*3:.1f}s sequential)")
                        
            except Exception as e:
                print(f"FAISS search error: {e}, falling back to mock data")

        # Fall back to mock recommendations if FAISS is empty or failed
        if not recommendations:
            room_style = request.user_style or request.room_style or "Modern"
            colors = request.color_preferences or request.colors or []
            mock_recommendations = await _get_mock_recommendations(
                room_style, colors, request.limit
            )
            recommendations = mock_recommendations

        # ==================================================================
        # ADD LOCAL CATALOG RECOMMENDATIONS (Hybrid Approach)
        # ==================================================================
        # Strategy: Keep 1-2 online recommendations, add 2 local catalog items
        # This ensures users see both local and online options
        room_style = request.user_style or request.room_style or "Modern"
        
        # Keep only 1 online recommendation if we have any
        online_recommendations = recommendations[:1] if recommendations else []
        local_catalog_recommendations = []
        
        # Get 2 local catalog items
        local_items = get_local_catalog_recommendations(room_style, limit=2)
        
        if local_items:
            print(f"📁 Adding {len(local_items)} local catalog recommendations")
            for item in local_items:
                # Generate AI reasoning for local catalog items
                try:
                    reasoning = await chat_agent.generate_reasoning(
                        artwork_title=item['title'],
                        artwork_style=item['category'].replace('_', ' ').title(),
                        room_style=room_style,
                        match_score=85.0  # High match for curated items
                    )
                except Exception as e:
                    print(f"⚠️  LLM reasoning failed for local item: {e}")
                    reasoning = f"This curated {item['category'].replace('_', ' ')} piece is expertly selected to complement your {room_style.lower()} style with 85% compatibility."
                
                local_catalog_recommendations.append(ArtworkRecommendation(
                    id=item['id'],
                    title=item['title'],
                    artist=item['artist'],
                    price=item['price'],
                    image_url=item['image_url'],
                    thumbnail_url=item['thumbnail_url'],
                    style=item['category'].replace('_', ' ').title(),
                    tags=item['tags'],
                    dimensions=f"{item['width']}x{item['height']}",
                    match_score=85.0,
                    reasoning=reasoning,
                    download_url=item['download_url'],
                    source="📁 Local Catalog",  # Clear indicator
                    purchase_options=[],
                    print_on_demand=[{
                        'service': ps['name'],
                        'url': ps['url'],
                        'price': ps['price_from']
                    } for ps in item['print_services']],
                    attribution={
                        'text': item['attribution'],
                        'url': item['attribution_url']
                    }
                ))
        
        # Combine: 2 local + 1 online
        recommendations = local_catalog_recommendations + online_recommendations
        print(f"📊 Final mix: {len(local_catalog_recommendations)} local + {len(online_recommendations)} online")

        # Add nearby stores if user location provided
        if request.user_location and request.user_location.get('latitude') and request.user_location.get('longitude'):
            try:
                print(f"🗺️  Finding nearby art stores for location: {request.user_location}")
                nearby_stores = await geo_agent.find_nearby_stores(
                    latitude=request.user_location['latitude'],
                    longitude=request.user_location['longitude'],
                    radius=request.user_location.get('radius', 10000),  # Default 10km
                    store_type="art_gallery"
                )
                
                # Add nearby stores to each recommendation
                if nearby_stores:
                    print(f"✅ Found {len(nearby_stores)} nearby stores")
                    for rec in recommendations:
                        # Format stores for response
                        rec.stores = [
                            {
                                "name": store["name"],
                                "address": store["address"],
                                "distance": f"{store['distance']} km",
                                "rating": store.get("rating", "N/A"),
                                "phone": store.get("phone", "N/A"),
                                "website": store.get("website", "N/A"),
                                "is_open": store.get("is_open"),
                                "lat": store["location"]["lat"],
                                "lng": store["location"]["lng"]
                            }
                            for store in nearby_stores[:5]  # Top 5 closest stores
                        ]
                else:
                    print("ℹ️  No nearby stores found")
            except Exception as e:
                print(f"⚠️  Error finding nearby stores: {e}")
                # Continue without local stores

        query_time = time.time() - start_time

        return RecommendationResponse(
            recommendations=recommendations,
            total_matches=len(recommendations),
            query_time=query_time,
            trends=[trend["style"] for trend in trends[:5]],  # Show top 5 trends
        )

    except Exception as e:
        print(f"Error in recommendations: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error generating recommendations: {str(e)}"
        )


class EnrichReasoningRequest(BaseModel):
    artworks: list[dict]
    room_style: str
    colors: list[str] = []


@router.post("/recommend/enrich-reasoning")
async def enrich_recommendations_with_reasoning(request: EnrichReasoningRequest):
    """
    Generate AI reasoning for multiple artworks in parallel
    Use this to enrich fast recommendations with LLM-powered explanations
    
    Args:
        artworks: List of {id, title, style, match_score, tags}
        room_style: User's room style
        colors: Room color palette
    
    Returns:
        List of {artwork_id, reasoning}
    """
    try:
        artworks = request.artworks
        room_style = request.room_style
        colors = request.colors
        # Generate reasoning for all artworks in parallel
        async def generate_single_reasoning(artwork):
            try:
                reasoning = await chat_agent.generate_reasoning(
                    artwork_title=artwork.get('title', 'Untitled'),
                    artwork_style=artwork.get('style', 'Contemporary'),
                    room_style=room_style,
                    colors=colors,
                    match_score=artwork.get('match_score', 90.0),
                    artwork_tags=artwork.get('tags', [])
                )
                return {
                    "artwork_id": artwork.get('id'),
                    "reasoning": reasoning
                }
            except Exception as e:
                print(f"Error generating reasoning for {artwork.get('id')}: {e}")
                return {
                    "artwork_id": artwork.get('id'),
                    "reasoning": f"This {artwork.get('style', 'contemporary').lower()} piece complements your {room_style.lower()} room beautifully."
                }
        
        # Process all artworks in parallel
        tasks = [generate_single_reasoning(artwork) for artwork in artworks]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filter out exceptions
        enriched = [r for r in results if isinstance(r, dict)]
        
        return {
            "enriched_count": len(enriched),
            "reasoning_list": enriched
        }
    
    except Exception as e:
        print(f"Error in batch reasoning generation: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.post("/recommend/{artwork_id}/reasoning")
async def generate_artwork_reasoning(
    artwork_id: str,
    artwork_title: str,
    artwork_style: str,
    room_style: str,
    colors: list = [],
    match_score: float = 90.0
):
    """
    Generate AI reasoning for a single artwork
    Use this to enrich recommendations with LLM-powered explanations
    """
    try:
        reasoning = await chat_agent.generate_reasoning(
            artwork_title=artwork_title,
            artwork_style=artwork_style,
            room_style=room_style,
            colors=colors,
            match_score=match_score,
            artwork_tags=[]
        )
        
        return {
            "artwork_id": artwork_id,
            "reasoning": reasoning
        }
    except Exception as e:
        print(f"Error generating reasoning: {e}")
        return {
            "artwork_id": artwork_id,
            "reasoning": f"This {artwork_style.lower()} piece matches your {room_style.lower()} room perfectly."
        }


@router.get("/recommend/trending")
async def get_trending_recommendations(limit: int = 10):
    """
    Get recommendations based on current trends

    - **limit**: Number of trending items to return
    """
    try:
        trends = await trend_agent.get_trending_styles()

        return {
            "trending_styles": trends,
            "seasonal": await trend_agent.get_seasonal_recommendations(),
        }

    except Exception as e:
        print(f"Error fetching trends: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching trends: {str(e)}")


async def _get_mock_recommendations(
    style: str, colors: list, limit: int
) -> list[ArtworkRecommendation]:
    """
    Generate recommendations using REAL store data
    Falls back to curated links if no API keys configured
    """
    try:
        # Search for real artwork from online stores
        print(f"🔍 Searching real stores for {style} artwork...")
        
        store_results = await store_agent.search_artwork(
            query=f"{style} wall art",
            style=style,
            color=colors[0] if colors else None,
            limit=limit
        )
        
        print(f"✅ Found {len(store_results)} real artworks!")
        
        # Convert store results to recommendations with AI reasoning
        recommendations = []
        for idx, item in enumerate(store_results):
            # Calculate decreasing match score
            match_score = 95.0 - (idx * 3)
            
            # Generate AI reasoning
            reasoning = await chat_agent.generate_reasoning(
                artwork_title=item["title"],
                artwork_style=item.get("tags", [style])[0] if item.get("tags") else style,
                room_style=style,
                colors=colors,
                match_score=match_score,
                artwork_tags=item.get("tags", [])
            )
            
            # Create recommendation with real store data
            recommendations.append(ArtworkRecommendation(
                id=item["id"],
                title=item["title"],
                artist=item["artist"],
                price=item["price"],
                image_url=item["image_url"],
                thumbnail_url=item.get("thumbnail_url", item["image_url"]),
                match_score=match_score,
                tags=item.get("tags", [style]),
                reasoning=reasoning,
                stores=[{
                    "name": item["source"],
                    "url": item.get("purchase_url", ""),
                    "distance": "Online"
                }],
                dimensions=item.get("dimensions", "Multiple sizes available"),
                medium=item.get("materials", ["Canvas"])[0] if item.get("materials") else "Canvas",
                style=item.get("tags", [style])[0] if item.get("tags") else style,
                # Real store integration fields
                purchase_url=item.get("purchase_url"),
                download_url=item.get("download_url"),
                source=item.get("source"),
                purchase_options=item.get("purchase_options", []),
                print_on_demand=item.get("print_on_demand", []),
                attribution=item.get("attribution")
            ))
        
        return recommendations
        
    except Exception as e:
        print(f"❌ Error fetching real store data: {e}")
        print("   Falling back to static mock data...")
        
        # Fallback to static data if store agent fails
        mock_data_raw = [
            {
                "id": "artwork_001",
                "title": "Abstract Geometric Canvas",
                "artist": "Modern Art Studio",
                "price": "$249",
                "image_url": "https://images.unsplash.com/photo-1541961017774-22349e4a1262?w=800",
                "thumbnail_url": "https://images.unsplash.com/photo-1541961017774-22349e4a1262?w=400",
                "match_score": 95.0,
                "tags": ["Modern", "Abstract", "Geometric"],
                "stores": [{"name": "Gallery Downtown", "distance": "1.2 km"}],
                "dimensions": "24x36 inches",
                "medium": "Canvas Print",
                "style": "Modern",
            },
            {
                "id": "artwork_002",
                "title": "Botanical Line Art Print",
                "artist": "Nature Studio",
                "price": "$129",
                "image_url": "https://images.unsplash.com/photo-1513519245088-0e12902e35ca?w=800",
                "thumbnail_url": "https://images.unsplash.com/photo-1513519245088-0e12902e35ca?w=400",
                "match_score": 92.0,
                "tags": ["Botanical", "Minimalist"],
                "stores": [{"name": "Green Gallery", "distance": "3.1 km"}],
                "dimensions": "18x24 inches",
                "medium": "Framed Print",
                "style": "Contemporary",
            },
            {
                "id": "artwork_003",
                "title": "Sunset Watercolor",
                "artist": "Color Waves",
                "price": "$189",
                "image_url": "https://images.unsplash.com/photo-1578926375605-eaf7559b0220?w=800",
                "thumbnail_url": "https://images.unsplash.com/photo-1578926375605-eaf7559b0220?w=400",
                "match_score": 88.0,
                "tags": ["Watercolor", "Warm Tones"],
                "stores": [{"name": "Sunset Art Co.", "distance": "5.0 km"}],
                "dimensions": "20x30 inches",
                "medium": "Watercolor Print",
                "style": "Abstract",
            },
        ]
        
        recommendations = []
        for item in mock_data_raw[:limit]:
            reasoning = await chat_agent.generate_reasoning(
                artwork_title=item["title"],
                artwork_style=item["style"],
                room_style=style,
                colors=colors,
                match_score=item["match_score"],
                artwork_tags=item["tags"]
            )
            item["reasoning"] = reasoning
            recommendations.append(ArtworkRecommendation(**item))
        
        return recommendations

