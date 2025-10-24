"""
Chat API routes for conversational décor recommendations
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from typing import Dict, Any
import time
import os

from models.chat import ChatRequest, ChatResponse, ChatMessage
from agents.chat_agent import get_chat_agent

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """
    Chat with AI assistant about décor recommendations
    
    **Flow:**
    1. User sends message (with optional image or context)
    2. AI processes with conversation history
    3. Returns response with suggestions
    4. Optional: Returns artwork recommendations
    
    **Features:**
    - Conversation history maintained per conversation_id
    - Context-aware responses (room analysis, preferences)
    - Suggested follow-up questions
    - Integration with recommendation engine
    """
    try:
        start_time = time.time()
        
        # Get chat agent
        chat_agent = get_chat_agent()
        
        # Process chat message
        response_text, conversation_id, suggestions = await chat_agent.chat(
            message=request.message,
            conversation_id=request.conversation_id,
            context=request.context,
        )
        
        # Check if user is asking for recommendations
        recommendations = None
        if any(
            word in request.message.lower()
            for word in ["recommend", "show", "find", "suggest", "options", "artwork", "art", "pieces"]
        ):
            try:
                # Import recommendation components
                from models.recommendation import RecommendationRequest
                import numpy as np
                
                # Get user style from context or message
                user_style = "Modern"  # Default
                colors = []
                style_vector = None
                
                # If we have context from previous room analysis, use it
                if request.context and isinstance(request.context, dict):
                    user_style = request.context.get("style", "Modern")
                    colors = request.context.get("colors", [])
                    if "style_vector" in request.context:
                        style_vector = request.context["style_vector"]
                
                # If no style vector, create a default one
                if not style_vector:
                    # Generate a random style vector for demonstration
                    # In production, you'd want to generate this based on the message content
                    style_vector = np.random.rand(512).tolist()
                
                # Get recommendations
                from routes.recommendations import get_recommendations as get_recs
                rec_request = RecommendationRequest(
                    style_vector=style_vector,
                    user_style=user_style,
                    color_preferences=colors or ["#E8E8E8"],
                    limit=3
                )
                
                rec_response = await get_recs(rec_request)
                recommendations = [
                    {
                        "id": rec.id,
                        "title": rec.title,
                        "artist": rec.artist,
                        "price": rec.price,
                        "image_url": str(rec.image_url),
                        "thumbnail_url": str(rec.thumbnail_url) if rec.thumbnail_url else None,
                        "match_score": rec.match_score,
                        "reasoning": rec.reasoning,
                        "source": rec.source,
                        "purchase_url": rec.purchase_url,
                        "download_url": rec.download_url,
                    }
                    for rec in rec_response.recommendations[:3]
                ]
                
                print(f"✅ Generated {len(recommendations)} recommendations for chat")
                
            except Exception as e:
                print(f"⚠️  Could not get recommendations: {e}")
                import traceback
                traceback.print_exc()
        
        processing_time = time.time() - start_time
        
        return ChatResponse(
            message=response_text,
            conversation_id=conversation_id,
            suggestions=suggestions,
            recommendations=recommendations,
            metadata={"processing_time": processing_time},
        )
    
    except Exception as e:
        print(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")


@router.get("/chat/history/{conversation_id}")
async def get_chat_history(conversation_id: str) -> Dict[str, Any]:
    """
    Retrieve conversation history
    
    **Returns:**
    - List of messages in conversation
    - Metadata (created_at, message count)
    """
    try:
        chat_agent = get_chat_agent()
        history = chat_agent.get_conversation(conversation_id)
        
        if not history:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        return {
            "conversation_id": conversation_id,
            "messages": history,
            "message_count": len(history),
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error retrieving history: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.delete("/chat/history/{conversation_id}")
async def clear_chat_history(conversation_id: str) -> Dict[str, str]:
    """
    Clear conversation history
    
    **Use case:** Start fresh conversation or privacy
    """
    try:
        chat_agent = get_chat_agent()
        
        if conversation_id in chat_agent.conversations:
            del chat_agent.conversations[conversation_id]
            return {"status": "success", "message": "Conversation cleared"}
        else:
            raise HTTPException(status_code=404, detail="Conversation not found")
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error clearing history: {e}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.post("/chat/feedback")
async def submit_feedback(
    conversation_id: str, message_index: int, feedback: str
) -> Dict[str, str]:
    """
    Submit feedback on AI response
    
    **Use case:** Improve AI quality over time
    """
    # In production, store feedback in database
    print(f"Feedback received for {conversation_id}[{message_index}]: {feedback}")
    
    return {
        "status": "success",
        "message": "Thank you for your feedback!",
    }

