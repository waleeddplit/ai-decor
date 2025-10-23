"""
API route modules
"""

from .room_analysis import router as room_analysis_router
from .recommendations import router as recommendations_router
from .profile import router as profile_router
from .chat import router as chat_router

__all__ = [
    "room_analysis_router",
    "recommendations_router",
    "profile_router",
    "chat_router",
]

