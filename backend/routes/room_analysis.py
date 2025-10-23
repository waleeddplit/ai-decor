"""
Room analysis API routes
POST /analyze_room - Upload and analyze room image
"""

import io
import time
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from PIL import Image

from models.room_analysis import RoomAnalysisResponse
from agents.decision_router import DecisionRouter

router = APIRouter(prefix="/api", tags=["Room Analysis"])

# Initialize decision router (orchestrates all agents)
decision_router = DecisionRouter()


@router.post("/analyze_room", response_model=RoomAnalysisResponse)
async def analyze_room(
    image: UploadFile = File(..., description="Room image file"),
    description: Optional[str] = Form(None, description="Optional text description"),
    user_id: Optional[str] = Form(None, description="Optional user ID"),
):
    """
    Analyze uploaded room image using AI vision models

    - **image**: Room photo (JPG, PNG, WEBP)
    - **description**: Optional text description of preferences
    - **user_id**: Optional user ID for personalization

    Returns comprehensive room analysis including:
    - Detected style
    - Color palette
    - Lighting conditions
    - Detected objects
    - Wall spaces for art
    """
    try:
        # Validate file type
        if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")

        # Read and open image
        image_data = await image.read()
        pil_image = Image.open(io.BytesIO(image_data))

        # Convert to RGB if necessary
        if pil_image.mode != "RGB":
            pil_image = pil_image.convert("RGB")

        # Analyze room using VisionMatchAgent
        start_time = time.time()
        analysis = await decision_router.vision_agent.analyze_room(pil_image, description)
        analysis["processing_time"] = time.time() - start_time

        # Save analysis to database (optional, if user_id provided)
        if user_id:
            from db.supabase_client import get_supabase_client

            db = get_supabase_client()
            await db.save_room_analysis(user_id, analysis)

        return RoomAnalysisResponse(**analysis)

    except Exception as e:
        print(f"Error in room analysis: {e}")
        raise HTTPException(status_code=500, detail=f"Error analyzing room: {str(e)}")


@router.get("/analyze_room/history")
async def get_analysis_history(user_id: str, limit: int = 10):
    """
    Get user's room analysis history

    - **user_id**: User identifier
    - **limit**: Number of recent analyses to return (default: 10)
    """
    try:
        from db.supabase_client import get_supabase_client

        db = get_supabase_client()
        analyses = await db.get_user_room_analyses(user_id, limit)

        return {"analyses": analyses, "count": len(analyses)}

    except Exception as e:
        print(f"Error fetching analysis history: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error fetching history: {str(e)}"
        )

