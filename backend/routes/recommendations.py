"""
Recommendations API routes
POST /recommend - Get artwork recommendations
"""

import time
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

router = APIRouter(prefix="/api", tags=["Recommendations"])

# Initialize agents
trend_agent = TrendIntelAgent()
chat_agent = get_chat_agent()


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
        trends = await trend_agent.get_trending_styles(location=room_style)

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
                
                # Convert FAISS results to recommendations
                if results:
                    for dist, artwork_meta in zip(distances, results):
                        similarity = 1.0 / (1.0 + dist)
                        match_score = similarity * 100
                        
                        # Generate AI reasoning with Gemini
                        reasoning = await chat_agent.generate_reasoning(
                            artwork_title=artwork_meta.get('title', 'Untitled'),
                            artwork_style=artwork_meta.get('style', 'Contemporary'),
                            room_style=request.user_style or request.room_style,
                            colors=request.color_preferences or request.colors,
                            match_score=match_score,
                            artwork_tags=artwork_meta.get('tags', [])
                        )
                        
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
                            stores=artwork_meta.get('stores', []),
                            dimensions=artwork_meta.get('dimensions', 'Standard'),
                            medium=artwork_meta.get('medium'),
                            style=artwork_meta.get('style', 'Contemporary')
                        ))
                        
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
    """Generate mock recommendations with AI reasoning"""
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
            "stores": [
                {"name": "Gallery Downtown", "distance": "1.2 km"},
                {"name": "Art House", "distance": "2.5 km"},
            ],
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
            "tags": ["Botanical", "Minimalist", "Line Art"],
            "stores": [
                {"name": "Green Gallery", "distance": "3.1 km"},
                {"name": "Urban Décor", "distance": "4.2 km"},
            ],
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
            "tags": ["Watercolor", "Warm Tones", "Abstract"],
            "stores": [{"name": "Sunset Art Co.", "distance": "5.0 km"}],
            "dimensions": "20x30 inches",
            "medium": "Watercolor Print",
            "style": "Abstract",
        },
    ]
    
    # Generate AI reasoning for each mock recommendation
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

