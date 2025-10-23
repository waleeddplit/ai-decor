"""
Room analysis request and response models
"""

from typing import Optional, List, Union, Dict, Any
from pydantic import BaseModel, Field


class ColorPalette(BaseModel):
    """RGB color with hex representation"""

    r: int = Field(..., ge=0, le=255)
    g: int = Field(..., ge=0, le=255)
    b: int = Field(..., ge=0, le=255)
    hex: str = Field(..., pattern=r"^#[0-9A-Fa-f]{6}$")
    name: Optional[str] = None


class DetectedObject(BaseModel):
    """Object detected in the room"""

    label: str
    confidence: float = Field(..., ge=0, le=1)
    bbox: List[float]  # [x, y, width, height]


class RoomAnalysisRequest(BaseModel):
    """Request for room analysis"""

    description: Optional[str] = Field(
        None, max_length=1000, description="Optional text description of the room"
    )
    user_id: Optional[str] = None


class RoomAnalysisResponse(BaseModel):
    """Response from room analysis"""

    style: str = Field(..., description="Detected room style (e.g., Modern, Minimalist)")
    colors: List[ColorPalette] = Field(..., description="Dominant color palette")
    lighting: Union[str, Dict[str, Any]] = Field(..., description="Lighting conditions (e.g., Natural, Bright) or detailed lighting info")
    detected_objects: List[DetectedObject] = Field(
        default_factory=list, description="Objects detected in the room"
    )
    wall_spaces: List[dict] = Field(
        default_factory=list, description="Available wall spaces for art"
    )
    room_size: Optional[str] = Field(None, description="Estimated room size")
    confidence_score: float = Field(
        ..., ge=0, le=1, description="Overall confidence in analysis"
    )
    processing_time: float = Field(..., description="Processing time in seconds")
    
    class Config:
        extra = "allow"  # Allow extra fields from VisionMatchAgent

