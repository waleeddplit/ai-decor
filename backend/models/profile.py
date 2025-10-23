"""
User profile models
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class StylePreference(BaseModel):
    """User's style preferences"""

    style_name: str
    weight: float = Field(..., ge=0, le=1, description="Preference weight 0-1")


class UserProfile(BaseModel):
    """User profile data"""

    id: Optional[str] = None
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    favorite_styles: List[str] = Field(default_factory=list)
    favorite_artworks: List[str] = Field(default_factory=list)
    style_preferences: List[StylePreference] = Field(default_factory=list)
    budget_range: Optional[dict] = None  # {"min": 0, "max": 1000}
    location: Optional[dict] = None  # {"lat": 0, "lng": 0, "city": ""}
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ProfileRequest(BaseModel):
    """Request to update profile"""

    name: Optional[str] = Field(None, max_length=100)
    favorite_styles: Optional[List[str]] = None
    favorite_artworks: Optional[List[str]] = None
    style_preferences: Optional[List[StylePreference]] = None
    budget_range: Optional[dict] = None
    location: Optional[dict] = None


class ProfileResponse(BaseModel):
    """Profile response"""

    profile: UserProfile
    message: str = "Profile retrieved successfully"

