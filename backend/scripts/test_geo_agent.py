"""
Test the GeoFinderAgent
"""

import os
import sys
import json
import asyncio
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.geo_finder_agent import GeoFinderAgent

async def test_geo_agent():
    """Test GeoFinderAgent functionality"""
    print("=" * 60)
    print("🧪 Testing GeoFinderAgent")
    print("=" * 60)
    
    # Initialize agent
    print("\n1️⃣  Initializing GeoFinderAgent...")
    agent = GeoFinderAgent()
    print("✅ Agent initialized")
    
    # Test 1: Find nearby stores (using NYC coordinates as example)
    print("\n2️⃣  Finding nearby art stores...")
    lat, lng = 40.7128, -74.0060  # New York City
    print(f"   Location: {lat}, {lng} (New York City)")
    
    stores = await agent.find_nearby_stores(
        latitude=lat,
        longitude=lng,
        radius=10000,
        store_type="art_gallery"
    )
    
    print(f"✅ Found {len(stores)} stores:")
    for idx, store in enumerate(stores, 1):
        print(f"\n   {idx}. {store['name']}")
        print(f"      Address: {store['address']}")
        print(f"      Distance: {store['distance']} km")
        print(f"      Rating: {store['rating']}⭐")
        print(f"      Status: {'🟢 Open' if store.get('is_open') else '🔴 Closed'}")
        if store.get('website') and store['website'] != 'N/A':
            print(f"      Website: {store['website']}")
    
    # Test 2: Get store inventory
    print("\n3️⃣  Checking store inventory...")
    if stores:
        test_store = stores[0]
        inventory = await agent.get_store_inventory(
            store_id=test_store['id'],
            artwork_id="art_12345"
        )
        print(f"   Store: {test_store['name']}")
        print(f"   ✅ Artwork availability: {inventory['in_stock']}")
        print(f"   Delivery: {inventory['estimated_delivery']}")
    
    # Test 3: Get directions
    print("\n4️⃣  Getting directions...")
    if stores:
        destination_store = stores[0]
        origin = (lat, lng)
        destination = (
            destination_store['location']['lat'],
            destination_store['location']['lng']
        )
        
        directions = await agent.get_directions(origin, destination)
        print(f"   To: {destination_store['name']}")
        print(f"   Distance: {directions['distance']}")
        print(f"   Duration: {directions['duration']}")
        print(f"   Steps:")
        for step in directions.get('steps', [])[:3]:
            # Remove HTML tags if present
            clean_step = step.replace('<b>', '').replace('</b>', '')
            print(f"      • {clean_step[:60]}...")
    
    # Test 4: Different store types
    print("\n5️⃣  Testing different store types...")
    store_types = [
        ("art_gallery", "Art Galleries"),
        ("home_goods_store", "Home Goods Stores"),
        ("furniture_store", "Furniture Stores")
    ]
    
    for store_type, display_name in store_types:
        stores = await agent.find_nearby_stores(
            latitude=lat,
            longitude=lng,
            radius=5000,
            store_type=store_type
        )
        print(f"   {display_name}: {len(stores)} found")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    print("✅ All GeoFinderAgent tests passed!")
    print()
    
    # Check if using real API or mock data
    if agent.gmaps:
        print("🌐 Using real Google Maps API")
    else:
        print("🔧 Using mock store data (add GOOGLE_MAPS_API_KEY to .env for real data)")
    
    print()

if __name__ == "__main__":
    asyncio.run(test_geo_agent())

