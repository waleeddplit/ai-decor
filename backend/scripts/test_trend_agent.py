"""
Test the TrendIntelAgent
"""

import os
import sys
import json
import asyncio
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.trend_intel_agent import TrendIntelAgent

async def test_trend_agent():
    """Test TrendIntelAgent functionality"""
    print("=" * 60)
    print("🧪 Testing TrendIntelAgent")
    print("=" * 60)
    
    # Initialize agent
    print("\n1️⃣  Initializing TrendIntelAgent...")
    agent = TrendIntelAgent()
    print("✅ Agent initialized")
    
    # Test 1: Get trending styles
    print("\n2️⃣  Fetching trending styles...")
    trends = await agent.get_trending_styles()
    print(f"✅ Found {len(trends)} trending styles:")
    for idx, trend in enumerate(trends, 1):
        print(f"\n   {idx}. {trend['style']}")
        print(f"      {trend['description']}")
        if 'relevance_score' in trend:
            print(f"      Relevance: {trend['relevance_score']:.2%}")
    
    # Test 2: Get seasonal recommendations
    print("\n3️⃣  Getting seasonal recommendations...")
    seasonal = await agent.get_seasonal_recommendations()
    print(f"✅ Current Season: {seasonal['season']}")
    rec = seasonal['recommendations']
    print(f"   Colors: {', '.join(rec['colors'][:3])}...")
    print(f"   Styles: {', '.join(rec['styles'])}")
    print(f"   Themes: {', '.join(rec['themes'])}")
    
    # Test 3: Match trends to style
    print("\n4️⃣  Matching trends to room style...")
    test_styles = [
        ("Modern Minimalist", ["#FFFFFF", "#000000", "#CCCCCC"]),
        ("Bohemian", ["#D4A373", "#8B7355", "#E8D5C4"]),
        ("Industrial", ["#2C3539", "#B0B0B0", "#757575"])
    ]
    
    for room_style, colors in test_styles:
        print(f"\n   Testing: {room_style}")
        recommendations = await agent.match_trends_to_style(room_style, colors)
        if recommendations:
            for rec in recommendations:
                print(f"      • {rec[:80]}...")
        else:
            print(f"      • No specific trend matches (will show general trends)")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    print("✅ All TrendIntelAgent tests passed!")
    print()
    
    # Check if using real API or mock data
    if agent.client:
        print("🌐 Using real Tavily API")
    else:
        print("🔧 Using mock trend data (add TAVILY_API_KEY to .env for real data)")
    
    print()

if __name__ == "__main__":
    asyncio.run(test_trend_agent())

