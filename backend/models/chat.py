"""
Pydantic models for chat interactions
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class ChatMessage(BaseModel):
    """Single chat message"""

    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: Optional[str] = Field(None, description="Message timestamp")
    image_url: Optional[str] = Field(None, description="Optional image attachment")


class ChatRequest(BaseModel):
    """Request for chat interaction"""

    message: str = Field(..., description="User's message")
    conversation_id: Optional[str] = Field(None, description="Conversation ID for history")
    image: Optional[str] = Field(None, description="Base64 encoded image (optional)")
    context: Optional[Dict[str, Any]] = Field(
        None, description="Additional context (e.g., previous room analysis)"
    )
    user_id: Optional[str] = None

    class Config:
        extra = "allow"


class ChatResponse(BaseModel):
    """Response from chat interaction"""

    message: str = Field(..., description="Assistant's response")
    conversation_id: str = Field(..., description="Conversation ID")
    suggestions: Optional[List[str]] = Field(
        None, description="Suggested follow-up questions"
    )
    recommendations: Optional[List[Dict[str, Any]]] = Field(
        None, description="Artwork recommendations if applicable"
    )
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class ConversationHistory(BaseModel):
    """Conversation history"""

    conversation_id: str
    messages: List[ChatMessage] = Field(default_factory=list)
    created_at: str
    updated_at: str
    user_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

