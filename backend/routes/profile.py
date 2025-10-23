"""
User profile API routes
GET /profile - Get user profile
POST /profile - Create/update user profile
"""

from typing import Optional
from fastapi import APIRouter, HTTPException
from datetime import datetime

from models.profile import UserProfile, ProfileRequest, ProfileResponse
from db.supabase_client import get_supabase_client

router = APIRouter(prefix="/api", tags=["User Profile"])


@router.get("/profile/{user_id}", response_model=ProfileResponse)
async def get_profile(user_id: str):
    """
    Get user profile by ID

    - **user_id**: User identifier

    Returns complete user profile including:
    - Favorite styles and artworks
    - Style preferences with weights
    - Budget range
    - Location
    """
    try:
        db = get_supabase_client()
        profile_data = await db.get_user_profile(user_id)

        if not profile_data:
            raise HTTPException(status_code=404, detail="Profile not found")

        profile = UserProfile(**profile_data)

        return ProfileResponse(profile=profile, message="Profile retrieved successfully")

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching profile: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching profile: {str(e)}")


@router.post("/profile", response_model=ProfileResponse)
async def create_or_update_profile(
    user_id: str,
    profile_request: ProfileRequest,
):
    """
    Create or update user profile

    - **user_id**: User identifier
    - **profile_request**: Profile data to update

    Updates:
    - Name
    - Favorite styles
    - Favorite artworks
    - Style preferences
    - Budget range
    - Location
    """
    try:
        db = get_supabase_client()

        # Check if profile exists
        existing_profile = await db.get_user_profile(user_id)

        profile_data = profile_request.model_dump(exclude_none=True)
        profile_data["updated_at"] = datetime.utcnow().isoformat()

        if existing_profile:
            # Update existing profile
            updated_data = await db.update_user_profile(user_id, profile_data)
            message = "Profile updated successfully"
        else:
            # Create new profile
            profile_data["id"] = user_id
            profile_data["created_at"] = datetime.utcnow().isoformat()
            updated_data = await db.create_user_profile(profile_data)
            message = "Profile created successfully"

        profile = UserProfile(**updated_data)

        return ProfileResponse(profile=profile, message=message)

    except Exception as e:
        print(f"Error saving profile: {e}")
        raise HTTPException(status_code=500, detail=f"Error saving profile: {str(e)}")


@router.post("/profile/{user_id}/favorites")
async def add_favorite(user_id: str, artwork_id: str):
    """
    Add artwork to user favorites

    - **user_id**: User identifier
    - **artwork_id**: Artwork identifier
    """
    try:
        db = get_supabase_client()
        result = await db.add_favorite(user_id, artwork_id)

        return {"message": "Artwork added to favorites", "favorite": result}

    except Exception as e:
        print(f"Error adding favorite: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error adding favorite: {str(e)}"
        )


@router.delete("/profile/{user_id}/favorites/{artwork_id}")
async def remove_favorite(user_id: str, artwork_id: str):
    """
    Remove artwork from user favorites

    - **user_id**: User identifier
    - **artwork_id**: Artwork identifier
    """
    try:
        db = get_supabase_client()
        success = await db.remove_favorite(user_id, artwork_id)

        if success:
            return {"message": "Artwork removed from favorites"}
        else:
            raise HTTPException(status_code=404, detail="Favorite not found")

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error removing favorite: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error removing favorite: {str(e)}"
        )


@router.get("/profile/{user_id}/favorites")
async def get_favorites(user_id: str):
    """
    Get user's favorite artworks

    - **user_id**: User identifier
    """
    try:
        db = get_supabase_client()
        favorites = await db.get_user_favorites(user_id)

        return {"favorites": favorites, "count": len(favorites)}

    except Exception as e:
        print(f"Error fetching favorites: {e}")
        raise HTTPException(
            status_code=500, detail=f"Error fetching favorites: {str(e)}"
        )

