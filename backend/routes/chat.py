"""
Chat API routes for conversational décor recommendations
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import time

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
        # If so, we could integrate with recommendation agent here
        recommendations = None
        if any(
            word in request.message.lower()
            for word in ["recommend", "show", "find", "suggest", "options"]
        ):
            # Check if we have style context for recommendations
            if request.context and isinstance(request.context, dict) and "style_vector" in request.context:
                try:
                    from agents.decision_router import get_decision_router
                    
                    router_agent = get_decision_router()
                    rec_result = await router_agent.recommend(
                        style_vector=request.context["style_vector"],
                        preferences=request.context.get("preferences", {}),
                    )
                    recommendations = rec_result.get("recommendations", [])[:3]  # Top 3
                except Exception as e:
                    print(f"Could not get recommendations: {e}")
        
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

