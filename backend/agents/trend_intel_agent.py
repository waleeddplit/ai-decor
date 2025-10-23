"""
TrendIntelAgent: Fetch and analyze current décor trends
Uses Tavily API for real-time trend data
"""

import os
from typing import List, Dict, Any, Optional
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


class TrendIntelAgent:
    """
    Analyzes current interior design and décor trends
    - Fetches trending styles via Tavily API
    - Provides seasonal recommendations
    - Adapts suggestions based on regional trends
    """

    def __init__(self):
        self.api_key = os.getenv("TAVILY_API_KEY")

        if self.api_key:
            try:
                from tavily import TavilyClient

                self.client = TavilyClient(api_key=self.api_key)
                print("TrendIntelAgent initialized with Tavily API")
            except ImportError:
                print("Warning: tavily-python not installed. Using mock trends.")
                self.client = None
        else:
            print("Warning: TAVILY_API_KEY not set. Using mock trends.")
            self.client = None

    async def get_trending_styles(
        self, location: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Fetch current trending décor styles using Tavily API ONLY

        Args:
            location: Optional location for regional trends

        Returns:
            List of trending styles with metadata
        """
        if self.client:
            try:
                return await self._fetch_real_trends(location)
            except Exception as e:
                print(f"❌ Error fetching trends from Tavily: {e}")
                raise Exception(f"Tavily API error: {e}. Please check your TAVILY_API_KEY.")
        else:
            raise Exception("TAVILY_API_KEY not configured. Please set it in .env file.")

    async def _fetch_real_trends(
        self, location: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Fetch real trends from Tavily API"""
        try:
            # More diverse query to get varied results
            query = "interior design trends 2025 Japandi Biophilic Quiet Luxury Maximalist Cottagecore"
            if location:
                query += f" {location} style"

            response = self.client.search(query, max_results=15)  # Increased for more variety

            trends = []
            seen_styles = set()
            
            for result in response.get("results", []):
                title = result.get("title", "")
                content = result.get("content", "")
                combined_text = f"{title} {content}"
                
                # Extract ALL styles mentioned in this article
                found_styles = self._extract_all_styles(combined_text)
                
                # Add each unique style
                for style in found_styles:
                    if style not in seen_styles:
                        seen_styles.add(style)
                        trends.append(
                            {
                                "style": style,
                                "description": content[:200] if content else title[:200],
                                "source": result.get("url", ""),
                                "relevance_score": result.get("score", 0.5),
                                "tags": self._extract_tags(combined_text),
                            }
                        )
                        
                # Stop if we have enough diverse styles
                if len(trends) >= 8:
                    break

            # Shuffle for variety
            import random
            random.shuffle(trends)
            
            # Return trends from Tavily
            if len(trends) < 3:
                raise Exception(f"Tavily returned insufficient trends: {len(trends)}. Expected at least 3.")
            
            return trends
        except Exception as e:
            print(f"❌ Error in Tavily API call: {e}")
            raise Exception(f"Tavily API error: {e}")

    def _extract_all_styles(self, text: str) -> List[str]:
        """Extract ALL style names mentioned in text"""
        styles = [
            # 2024-2025 Trending Styles (check these first)
            "Japandi",
            "Minimal Earthy",
            "Quiet Luxury",
            "Warm Minimalism",
            "Biophilic Design",
            "Biophilic",
            "Cottagecore",
            "Grandmillennial",
            "Sustainable Design",
            "Maximalist Revival",
            "Maximalist",
            "Organic Modern",
            # Classic Styles
            "Mid-Century Modern",
            "Minimalist",
            "Modern Farmhouse",
            "Scandinavian",
            "Bohemian",
            "Industrial",
            "Coastal",
            "Contemporary",
            "Art Deco",
            "Rustic",
            "Modern",
        ]

        found_styles = []
        text_lower = text.lower()
        
        for style in styles:
            if style.lower() in text_lower:
                found_styles.append(style)
        
        # Return at least one style
        return found_styles if found_styles else ["Contemporary"]
    
    def _extract_style_name(self, title: str) -> str:
        """Extract first style name from text (for backward compatibility)"""
        styles = self._extract_all_styles(title)
        return styles[0] if styles else "Contemporary"
    
    def _extract_tags(self, text: str) -> List[str]:
        """Extract relevant tags from text"""
        tags = []
        tag_keywords = {
            "Minimalist": ["minimal", "simple", "clean"],
            "Natural": ["natural", "organic", "wood"],
            "Sustainable": ["sustainable", "eco", "green"],
            "Cozy": ["cozy", "warm", "comfortable"],
            "Elegant": ["elegant", "luxury", "sophisticated"],
            "Modern": ["modern", "contemporary", "sleek"],
            "Vintage": ["vintage", "retro", "antique"],
            "Bold": ["bold", "vibrant", "colorful"],
        }
        
        text_lower = text.lower()
        for tag, keywords in tag_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                tags.append(tag)
        
        return tags[:4]  # Return up to 4 tags

    def _get_mock_trends(self) -> List[Dict[str, Any]]:
        """Return mock trending styles"""
        import random
        current_season = self._get_current_season()

        trends = [
            {
                "style": "Japandi",
                "description": "Fusion of Japanese and Scandinavian aesthetics featuring clean lines, natural materials, and muted color palettes.",
                "relevance_score": 0.96,
                "season": current_season,
                "tags": ["Minimalist", "Natural", "Zen", "Warm Wood"],
            },
            {
                "style": "Minimal Earthy",
                "description": "Neutral earth tones, organic textures, and sustainable materials creating calm, grounded spaces.",
                "relevance_score": 0.93,
                "season": current_season,
                "tags": ["Sustainable", "Natural", "Neutral", "Organic"],
            },
            {
                "style": "Quiet Luxury",
                "description": "Understated elegance with high-quality materials, subtle details, and timeless sophistication.",
                "relevance_score": 0.91,
                "season": current_season,
                "tags": ["Elegant", "Timeless", "Premium", "Subtle"],
            },
            {
                "style": "Warm Minimalism",
                "description": "Minimalist design with warm, natural materials and earth tones. Perfect for creating cozy yet uncluttered spaces.",
                "relevance_score": 0.90,
                "season": current_season,
                "tags": ["Cozy", "Simple", "Warm Tones", "Functional"],
            },
            {
                "style": "Biophilic Design",
                "description": "Incorporating natural elements, plants, and organic shapes to connect indoor spaces with nature.",
                "relevance_score": 0.88,
                "season": current_season,
                "tags": ["Nature", "Plants", "Wellness", "Green Living"],
            },
            {
                "style": "Cottagecore",
                "description": "Romantic, countryside-inspired aesthetic with vintage pieces, floral patterns, and handcrafted details.",
                "relevance_score": 0.82,
                "season": current_season,
                "tags": ["Vintage", "Floral", "Cozy", "Handmade"],
            },
            {
                "style": "Maximalist Revival",
                "description": "Bold colors, mixed patterns, and eclectic artwork creating personality-rich spaces.",
                "relevance_score": 0.78,
                "season": current_season,
                "tags": ["Bold", "Eclectic", "Colorful", "Layered"],
            },
            {
                "style": "Organic Modern",
                "description": "Contemporary design softened with natural materials, curved shapes, and earth-inspired color palettes.",
                "relevance_score": 0.85,
                "season": current_season,
                "tags": ["Contemporary", "Natural", "Curved", "Sophisticated"],
            },
        ]

        # Shuffle to show different trends each time
        random.shuffle(trends)
        return trends

    async def get_trending_style_tags(self) -> List[str]:
        """
        Get list of trending style tag names only
        
        Returns:
            List of trending style names (e.g., ["Japandi", "Minimal Earthy", ...])
        """
        trends = await self.get_trending_styles()
        return [trend["style"] for trend in trends]
    
    async def get_top_trends(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get top N trending styles sorted by relevance
        
        Args:
            limit: Number of trends to return
            
        Returns:
            List of top trending styles
        """
        trends = await self.get_trending_styles()
        # Sort by relevance score
        sorted_trends = sorted(trends, key=lambda x: x.get("relevance_score", 0), reverse=True)
        return sorted_trends[:limit]
    
    async def get_seasonal_recommendations(self) -> Dict[str, Any]:
        """Get seasonal décor recommendations"""
        season = self._get_current_season()

        seasonal_palettes = {
            "Winter": {
                "colors": ["#2C3E50", "#34495E", "#95A5A6", "#ECF0F1"],
                "styles": ["Cozy Minimalism", "Nordic", "Industrial"],
                "themes": ["warm textures", "layered lighting", "rich woods"],
            },
            "Spring": {
                "colors": ["#F8B500", "#82C4C3", "#A8E6CF", "#FFE5B4"],
                "styles": ["Fresh Contemporary", "Botanical", "Coastal"],
                "themes": ["floral patterns", "light fabrics", "pastel accents"],
            },
            "Summer": {
                "colors": ["#00CED1", "#F0E68C", "#FFB6C1", "#E0FFFF"],
                "styles": ["Coastal", "Mediterranean", "Tropical"],
                "themes": ["bright colors", "natural fibers", "open spaces"],
            },
            "Fall": {
                "colors": ["#D2691E", "#8B4513", "#CD853F", "#DEB887"],
                "styles": ["Rustic Modern", "Bohemian", "Traditional"],
                "themes": ["warm tones", "cozy textiles", "natural elements"],
            },
        }

        return {
            "season": season,
            "recommendations": seasonal_palettes.get(season, seasonal_palettes["Fall"]),
        }

    def _get_current_season(self) -> str:
        """Determine current season"""
        month = datetime.now().month

        if month in [12, 1, 2]:
            return "Winter"
        elif month in [3, 4, 5]:
            return "Spring"
        elif month in [6, 7, 8]:
            return "Summer"
        else:
            return "Fall"

    async def match_trends_to_style(
        self, room_style: str, room_colors: List[str]
    ) -> List[str]:
        """
        Match room style with current trends

        Args:
            room_style: Detected room style
            room_colors: Dominant colors in the room

        Returns:
            List of trend-aligned recommendations
        """
        trends = await self.get_trending_styles()

        recommendations = []
        for trend in trends:
            if self._style_similarity(room_style, trend["style"]) > 0.6:
                recommendations.append(
                    f"Consider {trend['style']} elements: {trend['description']}"
                )

        return recommendations[:3]  # Top 3 recommendations

    def _style_similarity(self, style1: str, style2: str) -> float:
        """Calculate similarity between two styles (simplified)"""
        # Simple word overlap - in production, use embeddings
        words1 = set(style1.lower().split())
        words2 = set(style2.lower().split())

        if not words1 or not words2:
            return 0.0

        intersection = words1 & words2
        union = words1 | words2

        return len(intersection) / len(union) if union else 0.0

