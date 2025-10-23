"""
Pydantic models for request/response schemas
"""

from .room_analysis import RoomAnalysisRequest, RoomAnalysisResponse
from .recommendation import RecommendationRequest, RecommendationResponse
from .profile import UserProfile, ProfileRequest, ProfileResponse
from .common import ErrorResponse, SuccessResponse

__all__ = [
    "RoomAnalysisRequest",
    "RoomAnalysisResponse",
    "RecommendationRequest",
    "RecommendationResponse",
    "UserProfile",
    "ProfileRequest",
    "ProfileResponse",
    "ErrorResponse",
    "SuccessResponse",
]

