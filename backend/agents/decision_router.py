"""
DecisionRouter: Orchestrates all AI agents and forms final recommendations
Integrates Vision, Trend, and Geo agents to create cohesive responses
"""

from typing import Dict, List, Any, Optional
from PIL import Image
import numpy as np

from .vision_match_agent import VisionMatchAgent
from .trend_intel_agent import TrendIntelAgent
from .geo_finder_agent import GeoFinderAgent


class DecisionRouter:
    """
    Main orchestrator for AI agent system
    - Coordinates VisionMatchAgent, TrendIntelAgent, and GeoFinderAgent
    - Synthesizes data from multiple sources
    - Generates natural language explanations
    """

    def __init__(self):
        self.vision_agent = VisionMatchAgent()
        self.trend_agent = TrendIntelAgent()
        self.geo_agent = GeoFinderAgent()
        print("DecisionRouter initialized with all agents")

    async def analyze_and_recommend(
        self,
        image: Image.Image,
        description: Optional[str] = None,
        user_location: Optional[Dict[str, float]] = None,
        user_preferences: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Complete analysis and recommendation pipeline

        Args:
            image: Room image
            description: Optional text description
            user_location: Optional {"lat": 0, "lng": 0}
            user_preferences: Optional user preferences dict

        Returns:
            Comprehensive analysis and recommendations
        """
        # Step 1: Vision Analysis
        room_analysis = await self.vision_agent.analyze_room(image, description)

        # Step 2: Trend Intelligence
        trends = await self.trend_agent.get_trending_styles(
            location=user_location.get("city") if user_location else None
        )

        # Step 3: Match trends to room style
        trend_recommendations = await self.trend_agent.match_trends_to_style(
            room_analysis["style"],
            [color["hex"] for color in room_analysis["colors"]],
        )

        # Step 4: Find nearby stores (if location provided)
        nearby_stores = []
        if user_location and "lat" in user_location and "lng" in user_location:
            nearby_stores = await self.geo_agent.find_nearby_stores(
                user_location["lat"], user_location["lng"]
            )

        # Step 5: Generate reasoning
        reasoning = await self._generate_reasoning(
            room_analysis, trends, user_preferences
        )

        return {
            "room_analysis": room_analysis,
            "trending_styles": trends,
            "trend_recommendations": trend_recommendations,
            "nearby_stores": nearby_stores,
            "reasoning": reasoning,
            "confidence": self._calculate_overall_confidence(room_analysis, trends),
        }

    async def _generate_reasoning(
        self,
        room_analysis: Dict[str, Any],
        trends: List[Dict[str, Any]],
        user_prefs: Optional[Dict[str, Any]],
    ) -> str:
        """
        Generate natural language reasoning for recommendations

        Args:
            room_analysis: Vision analysis results
            trends: Current trends
            user_prefs: User preferences

        Returns:
            Reasoning text
        """
        style = room_analysis["style"]
        colors = room_analysis["colors"]
        lighting = room_analysis["lighting"]

        reasoning_parts = [
            f"Your room has a {style.lower()} aesthetic with {lighting.lower()} lighting.",
        ]

        # Color analysis
        if colors:
            color_names = [self._get_color_name(c["hex"]) for c in colors[:2]]
            reasoning_parts.append(
                f"The dominant colors are {', '.join(color_names)}, creating a balanced palette."
            )

        # Trend alignment
        if trends:
            top_trend = trends[0]["style"]
            reasoning_parts.append(
                f"This aligns well with the current {top_trend} trend, which emphasizes comfort and natural elements."
            )

        # User preferences
        if user_prefs and "favorite_styles" in user_prefs:
            fav_styles = user_prefs["favorite_styles"]
            if fav_styles:
                reasoning_parts.append(
                    f"Based on your preference for {', '.join(fav_styles[:2])}, we've selected pieces that complement your taste."
                )

        return " ".join(reasoning_parts)

    def _calculate_overall_confidence(
        self, room_analysis: Dict[str, Any], trends: List[Dict[str, Any]]
    ) -> float:
        """Calculate overall confidence score"""
        vision_confidence = room_analysis.get("confidence_score", 0.8)
        trend_confidence = (
            trends[0]["relevance_score"] if trends else 0.7
        )

        # Weighted average
        overall = (vision_confidence * 0.7) + (trend_confidence * 0.3)
        return round(overall, 2)

    def _get_color_name(self, hex_color: str) -> str:
        """Convert hex color to approximate name"""
        # Simplified color naming
        color_map = {
            "#ffffff": "white",
            "#000000": "black",
            "#ff0000": "red",
            "#00ff00": "green",
            "#0000ff": "blue",
            "#ffff00": "yellow",
            "#ff00ff": "magenta",
            "#00ffff": "cyan",
            "#808080": "gray",
            "#c0c0c0": "silver",
            "#800000": "maroon",
            "#808000": "olive",
            "#008000": "dark green",
            "#800080": "purple",
            "#008080": "teal",
            "#000080": "navy",
        }

        # Check exact match
        if hex_color.lower() in color_map:
            return color_map[hex_color.lower()]

        # Approximate by RGB
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)

        if r > 200 and g > 200 and b > 200:
            return "light gray"
        elif r < 50 and g < 50 and b < 50:
            return "dark gray"
        elif r > g and r > b:
            return "warm tone"
        elif g > r and g > b:
            return "cool tone"
        elif b > r and b > g:
            return "cool blue"
        else:
            return "neutral"

    async def refine_recommendations(
        self,
        original_analysis: Dict[str, Any],
        user_feedback: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Refine recommendations based on user feedback

        Args:
            original_analysis: Previous analysis results
            user_feedback: User's feedback and preferences

        Returns:
            Refined recommendations
        """
        # Adjust based on feedback
        adjusted_style = user_feedback.get("preferred_style", original_analysis["room_analysis"]["style"])

        # Re-fetch trends with adjusted parameters
        trends = await self.trend_agent.get_trending_styles()

        return {
            "adjusted_style": adjusted_style,
            "new_trends": trends,
            "reasoning": f"Based on your feedback, we've adjusted the recommendations to focus more on {adjusted_style} aesthetics.",
        }

