"""
Recommendation request and response models
"""

from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl


class ArtworkRecommendation(BaseModel):
    """Single artwork recommendation"""

    id: str
    title: str
    artist: str
    price: str
    image_url: HttpUrl
    thumbnail_url: Optional[HttpUrl] = None
    match_score: float = Field(..., ge=0, le=100, description="Match percentage")
    tags: List[str] = Field(default_factory=list)
    reasoning: str = Field(..., description="AI reasoning for this recommendation")
    stores: List[dict] = Field(default_factory=list, description="Available stores")
    dimensions: Optional[str] = None
    medium: Optional[str] = None
    style: Optional[str] = None


class RecommendationRequest(BaseModel):
    """Request for décor recommendations"""

    # Primary fields from frontend
    style_vector: List[float] = Field(..., description="512-dim style embedding from CLIP")
    user_style: Optional[str] = Field(None, description="Detected room style")
    color_preferences: Optional[List[str]] = Field(None, description="Preferred colors in hex")
    
    # Optional fields
    room_type: Optional[str] = None
    budget: Optional[dict] = Field(None, description="Budget with min/max")
    user_location: Optional[dict] = Field(None, description="User location with lat/lng")
    
    # Legacy fields for backward compatibility
    room_style: Optional[str] = None
    colors: Optional[List[str]] = None
    lighting: Optional[str] = None
    user_preferences: Optional[dict] = None
    price_range: Optional[dict] = Field(None, description="Min/max price filter")
    
    limit: int = Field(default=3, ge=1, le=50, description="Number of recommendations")
    user_id: Optional[str] = None
    
    class Config:
        extra = "allow"  # Allow extra fields


class RecommendationResponse(BaseModel):
    """Response with recommendations"""

    recommendations: List[ArtworkRecommendation]
    total_matches: int
    query_time: float = Field(..., description="Query time in seconds")
    trends: Optional[List[str]] = Field(
        None, description="Current trending styles/themes"
    )

