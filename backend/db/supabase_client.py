"""
Supabase database client for PostgreSQL operations
"""

import os
from typing import Optional, List, Dict, Any
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()


class SupabaseClient:
    """Wrapper for Supabase operations"""

    def __init__(self):
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")

        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment")

        self.client: Client = create_client(supabase_url, supabase_key)

    # User Profile Operations
    async def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve user profile by ID"""
        try:
            response = self.client.table("profiles").select("*").eq("id", user_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error fetching user profile: {e}")
            return None

    async def create_user_profile(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user profile"""
        try:
            response = self.client.table("profiles").insert(profile_data).execute()
            return response.data[0]
        except Exception as e:
            print(f"Error creating user profile: {e}")
            raise

    async def update_user_profile(
        self, user_id: str, profile_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update existing user profile"""
        try:
            response = (
                self.client.table("profiles")
                .update(profile_data)
                .eq("id", user_id)
                .execute()
            )
            return response.data[0]
        except Exception as e:
            print(f"Error updating user profile: {e}")
            raise

    # Artwork Metadata Operations
    async def get_artwork_by_id(self, artwork_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve artwork metadata by ID"""
        try:
            response = (
                self.client.table("artworks").select("*").eq("id", artwork_id).execute()
            )
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error fetching artwork: {e}")
            return None

    async def get_artworks(
        self, filters: Optional[Dict[str, Any]] = None, limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Retrieve artworks with optional filters"""
        try:
            query = self.client.table("artworks").select("*")

            if filters:
                for key, value in filters.items():
                    query = query.eq(key, value)

            response = query.limit(limit).execute()
            return response.data
        except Exception as e:
            print(f"Error fetching artworks: {e}")
            return []

    async def search_artworks_by_style(
        self, style: str, limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Search artworks by style"""
        try:
            response = (
                self.client.table("artworks")
                .select("*")
                .ilike("style", f"%{style}%")
                .limit(limit)
                .execute()
            )
            return response.data
        except Exception as e:
            print(f"Error searching artworks: {e}")
            return []

    # Room Analysis History
    async def save_room_analysis(
        self, user_id: Optional[str], analysis_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Save room analysis results"""
        try:
            data = {
                "user_id": user_id,
                "style": analysis_data.get("style"),
                "colors": analysis_data.get("colors"),
                "lighting": analysis_data.get("lighting"),
                "metadata": analysis_data,
            }
            response = self.client.table("room_analyses").insert(data).execute()
            return response.data[0]
        except Exception as e:
            print(f"Error saving room analysis: {e}")
            raise

    async def get_user_room_analyses(
        self, user_id: str, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get user's room analysis history"""
        try:
            response = (
                self.client.table("room_analyses")
                .select("*")
                .eq("user_id", user_id)
                .order("created_at", desc=True)
                .limit(limit)
                .execute()
            )
            return response.data
        except Exception as e:
            print(f"Error fetching room analyses: {e}")
            return []

    # Favorites
    async def add_favorite(self, user_id: str, artwork_id: str) -> Dict[str, Any]:
        """Add artwork to user favorites"""
        try:
            data = {"user_id": user_id, "artwork_id": artwork_id}
            response = self.client.table("favorites").insert(data).execute()
            return response.data[0]
        except Exception as e:
            print(f"Error adding favorite: {e}")
            raise

    async def remove_favorite(self, user_id: str, artwork_id: str) -> bool:
        """Remove artwork from user favorites"""
        try:
            self.client.table("favorites").delete().eq("user_id", user_id).eq(
                "artwork_id", artwork_id
            ).execute()
            return True
        except Exception as e:
            print(f"Error removing favorite: {e}")
            return False

    async def get_user_favorites(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user's favorite artworks"""
        try:
            response = (
                self.client.table("favorites")
                .select("*, artworks(*)")
                .eq("user_id", user_id)
                .execute()
            )
            return response.data
        except Exception as e:
            print(f"Error fetching favorites: {e}")
            return []


# Singleton instance
_supabase_client: Optional[SupabaseClient] = None


def get_supabase_client() -> SupabaseClient:
    """Get or create Supabase client singleton"""
    global _supabase_client
    if _supabase_client is None:
        _supabase_client = SupabaseClient()
    return _supabase_client

