"""
Test script for TrendIntelAgent
Tests trend fetching and style tag extraction
"""

import asyncio
import sys
sys.path.insert(0, '.')

from agents.trend_intel_agent import TrendIntelAgent


async def test_trend_agent():
    print("=" * 70)
    print("Testing TrendIntelAgent")
    print("=" * 70)
    print()
    
    agent = TrendIntelAgent()
    
    # Test 1: Get all trending styles
    print("Test 1: Get Trending Styles")
    print("-" * 70)
    trends = await agent.get_trending_styles()
    for i, trend in enumerate(trends, 1):
        print(f"\n{i}. {trend['style']} (Score: {trend.get('relevance_score', 0):.2f})")
        print(f"   Description: {trend['description']}")
        if 'tags' in trend:
            print(f"   Tags: {', '.join(trend['tags'])}")
    print()
    
    # Test 2: Get trending style tags only
    print("\nTest 2: Get Trending Style Tags (names only)")
    print("-" * 70)
    style_tags = await agent.get_trending_style_tags()
    print("Trending Styles:")
    for tag in style_tags:
        print(f"  • {tag}")
    print()
    
    # Test 3: Get top 3 trends
    print("\nTest 3: Get Top 3 Trends")
    print("-" * 70)
    top_trends = await agent.get_top_trends(limit=3)
    for i, trend in enumerate(top_trends, 1):
        print(f"{i}. {trend['style']} ({trend['relevance_score']:.0%})")
    print()
    
    # Test 4: Get seasonal recommendations
    print("\nTest 4: Get Seasonal Recommendations")
    print("-" * 70)
    seasonal = await agent.get_seasonal_recommendations()
    print(f"Current Season: {seasonal['season']}")
    if 'colors' in seasonal:
        print(f"Recommended Colors: {', '.join(seasonal['colors'][:3])}")
    if 'featured_styles' in seasonal:
        print(f"Featured Styles: {', '.join(seasonal['featured_styles'])}")
    print()
    
    print("=" * 70)
    print("✅ All tests completed!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(test_trend_agent())
