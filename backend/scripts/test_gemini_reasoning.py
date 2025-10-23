"""
Test script for Gemini-powered reasoning in recommendations
"""

import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.chat_agent import get_chat_agent


async def test_reasoning():
    """Test AI reasoning generation"""
    print("=" * 70)
    print("Testing Gemini Reasoning for Artwork Recommendations")
    print("=" * 70)
    print()
    
    agent = get_chat_agent()
    
    if not agent.api_key:
        print("❌ No API key configured!")
        print("   Please set GEMINI_API_KEY, OPENAI_API_KEY, or GROQ_API_KEY in .env")
        return
    
    print(f"✅ Using {agent.provider.upper()} with model: {agent.model}")
    print()
    
    # Test cases
    test_cases = [
        {
            "artwork_title": "Abstract Geometric Canvas",
            "artwork_style": "Modern",
            "room_style": "Modern Minimalist",
            "colors": ["#E8E8E8", "#4A4A4A", "#FFFFFF"],
            "match_score": 95.0,
            "artwork_tags": ["Modern", "Abstract", "Geometric"],
        },
        {
            "artwork_title": "Botanical Line Art Print",
            "artwork_style": "Contemporary",
            "room_style": "Scandinavian",
            "colors": ["#F5F5DC", "#8B7355", "#A8D5BA"],
            "match_score": 92.0,
            "artwork_tags": ["Botanical", "Minimalist", "Line Art"],
        },
        {
            "artwork_title": "Sunset Watercolor",
            "artwork_style": "Abstract",
            "room_style": "Bohemian",
            "colors": ["#FF6B6B", "#FFD93D", "#6BCB77"],
            "match_score": 88.0,
            "artwork_tags": ["Watercolor", "Warm Tones", "Abstract"],
        },
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}: {test_case['artwork_title']}")
        print("-" * 70)
        print(f"  Artwork Style: {test_case['artwork_style']}")
        print(f"  Room Style: {test_case['room_style']}")
        print(f"  Colors: {', '.join(test_case['colors'])}")
        print(f"  Match Score: {test_case['match_score']}%")
        print(f"  Tags: {', '.join(test_case['artwork_tags'])}")
        print()
        
        try:
            reasoning = await agent.generate_reasoning(**test_case)
            print(f"  🤖 AI Reasoning:")
            print(f"     {reasoning}")
            print()
        except Exception as e:
            print(f"  ❌ Error: {e}")
            print()
    
    print("=" * 70)
    print("✅ Testing Complete!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(test_reasoning())

