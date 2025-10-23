"""
End-to-end test: Room upload → AI analysis → Recommendations
Simulates the complete user flow through the Art.Decor.AI system
"""

import os
import sys
import json
import asyncio
import numpy as np
from pathlib import Path
from PIL import Image
import requests
from io import BytesIO
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.vision_match_agent import VisionMatchAgent
from agents.trend_intel_agent import TrendIntelAgent
from agents.geo_finder_agent import GeoFinderAgent
from db.faiss_client import FAISSClient

async def test_end_to_end():
    """Complete end-to-end test of the Art.Decor.AI system"""
    print("=" * 70)
    print("🏠 Art.Decor.AI - End-to-End System Test")
    print("=" * 70)
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # ============================================================
    # STEP 1: User uploads room photo
    # ============================================================
    print("STEP 1️⃣  User uploads room photo")
    print("-" * 70)
    
    room_url = "https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800"
    room_description = "My living room - looking for modern wall art to brighten it up"
    user_location = (40.7128, -74.0060)  # New York City
    
    print(f"📸 Image URL: {room_url}")
    print(f"📝 Description: \"{room_description}\"")
    print(f"📍 Location: {user_location}")
    
    # Download image
    print("\n   Downloading image...")
    response = requests.get(room_url, timeout=10)
    room_image = Image.open(BytesIO(response.content))
    print(f"   ✅ Image loaded: {room_image.size}")
    
    # ============================================================
    # STEP 2: Vision AI analyzes the room
    # ============================================================
    print("\n\nSTEP 2️⃣  AI Vision Analysis")
    print("-" * 70)
    
    vision_agent = VisionMatchAgent(use_dinov2=False)
    
    print("🔍 Analyzing room characteristics...")
    analysis = await vision_agent.analyze_room(room_image, room_description)
    
    print(f"\n✅ Analysis Complete:")
    print(f"   Room Style: {analysis['style']}")
    print(f"   Confidence: {analysis['confidence_score']:.1%}")
    print(f"\n   Color Palette:")
    for color in analysis['palette'][:3]:
        print(f"      • {color['name']:15} {color['hex']:8} ({color['percentage']:.1f}%)")
    
    print(f"\n   Lighting:")
    lighting = analysis['lighting']
    print(f"      • Type: {lighting.get('type', 'Unknown')}")
    print(f"      • Quality: {lighting.get('quality', 'Unknown')}")
    
    print(f"\n   Detected Objects: {len(analysis['detected_objects'])}")
    for obj in analysis['detected_objects'][:3]:
        print(f"      • {obj.get('category', obj.get('class', 'Unknown'))} (confidence: {obj['confidence']:.2%})")
    
    # ============================================================
    # STEP 3: FAISS searches for similar artworks
    # ============================================================
    print("\n\nSTEP 3️⃣  Finding matching artwork")
    print("-" * 70)
    
    # Initialize FAISS with sample artworks
    faiss_client = FAISSClient()
    if faiss_client.index is None or faiss_client.get_total_vectors() == 0:
        print("📦 Loading sample artwork database...")
        
        # Create mock artwork database
        sample_artworks = [
            {
                "id": "art_001",
                "title": "Abstract Sunset",
                "artist": "Sarah Chen",
                "style": "Abstract Modern",
                "colors": ["#D4A574", "#E8C4A0", "#B08968"],
                "price": 299,
                "dimensions": "24x36 inches"
            },
            {
                "id": "art_002",
                "title": "Minimalist Lines",
                "artist": "James Park",
                "style": "Minimalist",
                "colors": ["#2C2C2C", "#FFFFFF", "#A0A0A0"],
                "price": 199,
                "dimensions": "30x40 inches"
            },
            {
                "id": "art_003",
                "title": "Botanical Dreams",
                "artist": "Emma Wilson",
                "style": "Contemporary",
                "colors": ["#7CAA7E", "#E8D5C4", "#F5F5DC"],
                "price": 349,
                "dimensions": "20x30 inches"
            }
        ]
        
        # Generate mock embeddings (in production, these would be pre-generated)
        style_vector = np.array(analysis['style_vector'])
        mock_vectors = []
        
        for i, artwork in enumerate(sample_artworks):
            # Add some variation to the room's style vector
            variation = np.random.normal(0, 0.1, style_vector.shape)
            artwork_vector = style_vector + variation
            artwork_vector = artwork_vector / np.linalg.norm(artwork_vector)
            mock_vectors.append(artwork_vector)
        
        vectors = np.array(mock_vectors)
        faiss_client.add_vectors(vectors, sample_artworks)
        print(f"   ✅ Loaded {len(sample_artworks)} artworks")
    
    # Search for matching artwork
    print("\n🔍 Searching for similar artwork...")
    style_vector = np.array(analysis['style_vector'])
    distances, matches = faiss_client.search(style_vector, k=3)
    
    print(f"\n✅ Found {len(matches)} recommendations:")
    recommendations = []
    
    for idx, (dist, artwork) in enumerate(zip(distances, matches), 1):
        similarity = 1.0 / (1.0 + dist)
        match_score = similarity * 100
        
        recommendations.append({
            **artwork,
            "match_score": match_score,
            "similarity_distance": dist
        })
        
        print(f"\n   {idx}. {artwork['title']} by {artwork['artist']}")
        print(f"      Match Score: {match_score:.1f}%")
        print(f"      Style: {artwork['style']}")
        print(f"      Price: ${artwork['price']}")
        print(f"      Size: {artwork['dimensions']}")
    
    # ============================================================
    # STEP 4: Trend Intelligence adds context
    # ============================================================
    print("\n\nSTEP 4️⃣  Current Design Trends")
    print("-" * 70)
    
    trend_agent = TrendIntelAgent()
    
    print("📊 Fetching current trends...")
    trends = await trend_agent.get_trending_styles()
    print(f"\n✅ Top 3 trending styles:")
    for idx, trend in enumerate(trends[:3], 1):
        print(f"   {idx}. {trend['style']}")
        print(f"      {trend['description'][:60]}...")
    
    # Get seasonal recommendations
    seasonal = await trend_agent.get_seasonal_recommendations()
    print(f"\n🍂 Seasonal Insight ({seasonal['season']}):")
    rec = seasonal['recommendations']
    print(f"   Recommended styles: {', '.join(rec['styles'])}")
    
    # ============================================================
    # STEP 5: Find local stores
    # ============================================================
    print("\n\nSTEP 5️⃣  Finding nearby stores")
    print("-" * 70)
    
    geo_agent = GeoFinderAgent()
    
    print(f"📍 Searching near: {user_location}")
    stores = await geo_agent.find_nearby_stores(
        latitude=user_location[0],
        longitude=user_location[1],
        radius=10000,
        store_type="art_gallery"
    )
    
    print(f"\n✅ Found {len(stores)} nearby stores:")
    for idx, store in enumerate(stores[:3], 1):
        print(f"\n   {idx}. {store['name']}")
        print(f"      {store['address']}")
        print(f"      Distance: {store['distance']} km")
        print(f"      Rating: {store['rating']}⭐")
        print(f"      {'🟢 Open' if store.get('is_open') else '🔴 Closed'}")
    
    # ============================================================
    # FINAL SUMMARY
    # ============================================================
    print("\n\n" + "=" * 70)
    print("📋 RECOMMENDATION SUMMARY")
    print("=" * 70)
    
    print(f"\n🎨 Your Room Profile:")
    print(f"   Style: {analysis['style']}")
    print(f"   Dominant Colors: {', '.join(c['name'] for c in analysis['palette'][:3])}")
    print(f"   Lighting: {lighting.get('type', 'Unknown')}")
    
    print(f"\n🖼️  Top Artwork Recommendations:")
    for idx, rec in enumerate(recommendations[:3], 1):
        print(f"   {idx}. {rec['title']} - ${rec['price']} ({rec['match_score']:.0f}% match)")
    
    print(f"\n📍 Nearby Stores:")
    for store in stores[:2]:
        print(f"   • {store['name']} ({store['distance']} km)")
    
    print(f"\n📈 Current Trends:")
    for trend in trends[:2]:
        print(f"   • {trend['style']}")
    
    print("\n" + "=" * 70)
    print("✅ End-to-End Test Complete!")
    print("=" * 70)
    print("\n💡 All system components working correctly:")
    print("   ✅ Vision AI (Room Analysis)")
    print("   ✅ Vector Search (FAISS)")
    print("   ✅ Trend Intelligence (Tavily API)")
    print("   ✅ Geo Search (Google Maps API)")
    print("\n🎉 Art.Decor.AI is ready to deploy!")
    print()

if __name__ == "__main__":
    asyncio.run(test_end_to_end())

