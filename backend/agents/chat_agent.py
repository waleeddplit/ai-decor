"""
Chat Agent for conversational décor recommendations
Integrates with LLM (OpenAI/Groq) for natural language interactions
"""

import os
import json
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime
import uuid


class ChatAgent:
    """
    Conversational AI agent for décor recommendations
    Supports context-aware responses and integrates with other agents
    """

    def __init__(self):
        """Initialize chat agent with LLM configuration"""
        # Detect which provider to use based on available API keys
        # Priority: Ollama (local) > Groq (free) > Gemini > OpenAI
        if os.getenv("USE_OLLAMA") == "true" or os.getenv("OLLAMA_BASE_URL"):
            self.provider = "ollama"
            self.api_key = None  # Ollama doesn't need API key
            self.model = os.getenv("CHAT_MODEL", "llava")  # llava, llama3.2-vision
            self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        elif os.getenv("GROQ_API_KEY"):
            self.provider = "groq"
            self.api_key = os.getenv("GROQ_API_KEY")
            self.model = os.getenv("CHAT_MODEL", "llama-3.2-90b-vision-preview")
        elif os.getenv("GEMINI_API_KEY"):
            self.provider = "gemini"
            self.api_key = os.getenv("GEMINI_API_KEY")
            self.model = os.getenv("CHAT_MODEL", "gemini-1.5-flash")
        elif os.getenv("OPENAI_API_KEY"):
            self.provider = "openai"
            self.api_key = os.getenv("OPENAI_API_KEY")
            self.model = os.getenv("CHAT_MODEL", "gpt-3.5-turbo")
        else:
            self.provider = None
            self.api_key = None
            self.model = None
        
        # In-memory conversation storage (for development)
        # In production, use Redis or database
        self.conversations: Dict[str, List[Dict[str, str]]] = {}
        
        # System prompt for décor context
        self.system_prompt = """You are an expert interior design AI assistant for Art.Decor.AI. 
You help users find perfect wall art and décor for their spaces.

Your capabilities:
- Analyze room photos to detect style, colors, and lighting
- Recommend artwork based on room aesthetics
- Suggest color palettes and design styles
- Find local stores with artwork availability
- Stay updated on trending décor styles

Personality:
- Friendly, enthusiastic, and knowledgeable
- Ask clarifying questions when needed
- Provide specific, actionable recommendations
- Use emojis sparingly for warmth

Guidelines:
- Keep responses concise (2-3 paragraphs max)
- Always consider user's budget and preferences
- Suggest 2-3 follow-up actions
- If user shares a room image, acknowledge you'll analyze it
"""

    def get_conversation_id(self) -> str:
        """Generate new conversation ID"""
        return str(uuid.uuid4())

    def get_conversation(self, conversation_id: str) -> List[Dict[str, str]]:
        """Retrieve conversation history"""
        return self.conversations.get(conversation_id, [])

    def add_message(
        self, conversation_id: str, role: str, content: str
    ) -> None:
        """Add message to conversation history"""
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []
        
        self.conversations[conversation_id].append(
            {
                "role": role,
                "content": content,
                "timestamp": datetime.utcnow().isoformat(),
            }
        )

    async def chat(
        self,
        message: str,
        conversation_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> Tuple[str, str, List[str]]:
        """
        Process chat message and return response
        
        Args:
            message: User's message
            conversation_id: Optional conversation ID for history
            context: Optional context (e.g., room analysis results)
        
        Returns:
            Tuple of (response, conversation_id, suggestions)
        """
        # Create or retrieve conversation
        if not conversation_id:
            conversation_id = self.get_conversation_id()
        
        # Add user message to history
        self.add_message(conversation_id, "user", message)
        
        # Prepare messages for LLM
        messages = [{"role": "system", "content": self.system_prompt}]
        
        # Add context if available
        if context:
            context_msg = self._format_context(context)
            messages.append({"role": "system", "content": context_msg})
        
        # Add conversation history
        history = self.get_conversation(conversation_id)
        for msg in history[-10:]:  # Last 10 messages for context
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        # Get LLM response
        try:
            response_text = await self._get_llm_response(messages)
        except Exception as e:
            print(f"LLM error: {e}")
            # Fallback disabled - raise error to show Gemini is required
            raise Exception(f"Gemini API error: {e}. Please check your GEMINI_API_KEY.")
            # FALLBACK DISABLED: Uncomment below to re-enable fallback responses
            # response_text = await self._fallback_response(message, context)
        
        # Add assistant response to history
        self.add_message(conversation_id, "assistant", response_text)
        
        # Generate suggestions
        suggestions = self._generate_suggestions(message, context)
        
        return response_text, conversation_id, suggestions

    async def _get_llm_response(self, messages: List[Dict[str, str]]) -> str:
        """
        Get response from LLM (OpenAI or Groq)
        """
        if not self.api_key:
            raise ValueError("No API key configured")
        
        if self.provider == "openai":
            return await self._openai_request(messages)
        elif self.provider == "groq":
            return await self._groq_request(messages)
        elif self.provider == "gemini":
            return await self._gemini_request(messages)
        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    async def _openai_request(self, messages: List[Dict[str, str]]) -> str:
        """Make request to OpenAI API"""
        try:
            import openai
            
            client = openai.AsyncOpenAI(api_key=self.api_key)
            
            response = await client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500,
            )
            
            return response.choices[0].message.content
        except ImportError:
            raise ValueError("openai package not installed. Run: pip install openai")
        except Exception as e:
            raise Exception(f"OpenAI API error: {e}")

    async def _groq_request(self, messages: List[Dict[str, str]]) -> str:
        """Make request to Groq API"""
        try:
            from groq import AsyncGroq
            
            client = AsyncGroq(api_key=self.api_key)
            
            response = await client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=500,
            )
            
            return response.choices[0].message.content
        except ImportError:
            raise ValueError("groq package not installed. Run: pip install groq")
        except Exception as e:
            raise Exception(f"Groq API error: {e}")

    async def _gemini_request(self, messages: List[Dict[str, str]]) -> str:
        """Make request to Google Gemini API"""
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel(self.model)
            
            # Convert messages to Gemini format
            # Gemini uses a simpler format: just the conversation text
            conversation_text = ""
            for msg in messages:
                role = msg["role"]
                content = msg["content"]
                if role == "system":
                    conversation_text += f"Instructions: {content}\n\n"
                elif role == "user":
                    conversation_text += f"User: {content}\n\n"
                elif role == "assistant":
                    conversation_text += f"Assistant: {content}\n\n"
            
            # Generate response
            response = await model.generate_content_async(
                conversation_text,
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": 500,
                }
            )
            
            return response.text
        except ImportError:
            raise ValueError("google-generativeai package not installed. Run: pip install google-generativeai")
        except Exception as e:
            raise Exception(f"Gemini API error: {e}")

    async def _fallback_response(
        self, message: str, context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Fallback response when LLM is unavailable
        Provides rule-based responses
        """
        message_lower = message.lower()
        
        # Room analysis request
        if any(word in message_lower for word in ["analyze", "room", "photo", "image", "picture"]):
            return (
                "I'd love to help you find the perfect artwork! 🎨\n\n"
                "To give you personalized recommendations, please upload a photo of your room. "
                "I'll analyze the style, colors, and lighting to suggest artwork that complements your space perfectly.\n\n"
                "You can also tell me about your preferences - what style do you like? "
                "Modern, minimalist, bohemian, or something else?"
            )
        
        # Style inquiry
        elif any(word in message_lower for word in ["style", "modern", "minimalist", "bohemian"]):
            styles_mentioned = []
            style_map = {
                "modern": "Modern",
                "minimalist": "Minimalist",
                "bohemian": "Bohemian",
                "scandinavian": "Scandinavian",
                "abstract": "Abstract",
                "contemporary": "Contemporary"
            }
            for key, value in style_map.items():
                if key in message_lower:
                    styles_mentioned.append(value)
            
            if styles_mentioned:
                return (
                    f"Great choice! {styles_mentioned[0]} style is very popular right now. 🌟\n\n"
                    f"For a {styles_mentioned[0].lower()} aesthetic, I'd recommend artwork with clean lines, "
                    "neutral colors, and simple compositions. Would you like me to show you some options?\n\n"
                    "To give you the best recommendations, you can:\n"
                    "• Upload a photo of your room\n"
                    "• Tell me your budget range\n"
                    "• Share your favorite colors"
                )
            else:
                return (
                    "I can help you find artwork in various styles:\n\n"
                    "🎨 Modern - Bold, contemporary pieces\n"
                    "✨ Minimalist - Clean, simple designs\n"
                    "🌿 Bohemian - Eclectic, colorful art\n"
                    "🏔️ Scandinavian - Natural, serene aesthetics\n\n"
                    "Which style resonates with you?"
                )
        
        # Budget inquiry
        elif any(word in message_lower for word in ["budget", "price", "cost", "cheap", "expensive"]):
            return (
                "I can help you find beautiful artwork at any price point! 💰\n\n"
                "What's your budget range?\n"
                "• Under $100 - Affordable prints and posters\n"
                "• $100-$300 - Quality art prints and canvases\n"
                "• $300-$500 - Premium artwork\n"
                "• $500+ - Original pieces and limited editions\n\n"
                "Once I know your budget, I'll find the perfect pieces for you!"
            )
        
        # Color inquiry
        elif any(word in message_lower for word in ["color", "blue", "red", "green", "neutral"]):
            return (
                "Colors are so important for creating the right atmosphere! 🎨\n\n"
                "Tell me more about your color preferences:\n"
                "• What colors dominate your room?\n"
                "• Do you want artwork that matches or contrasts?\n"
                "• Any colors you absolutely love or want to avoid?\n\n"
                "Or upload a room photo and I'll detect the colors automatically!"
            )
        
        # Context-aware response
        elif context and "style" in context:
            style = context.get("style", "")
            return (
                f"Based on your {style} room, I have some great recommendations! 🎨\n\n"
                "I've analyzed your space and found artwork that perfectly complements your style. "
                "Would you like to see:\n"
                "• Top matches for your room\n"
                "• Options in a specific color\n"
                "• Pieces within a certain budget\n\n"
                "Let me know what you'd like to explore!"
            )
        
        # General greeting
        elif any(word in message_lower for word in ["hello", "hi", "hey", "help"]):
            return (
                "Hello! I'm your AI décor assistant. 👋\n\n"
                "I can help you find the perfect wall art for any room! Here's what I can do:\n\n"
                "🎨 Analyze your room from a photo\n"
                "🖼️ Recommend artwork based on your style\n"
                "🎯 Filter by budget and preferences\n"
                "🏪 Find local stores with availability\n\n"
                "Want to get started? Upload a room photo or tell me about your space!"
            )
        
        # Default response
        else:
            return (
                "I'm here to help you find amazing artwork for your space! 🎨\n\n"
                "To give you the best recommendations, I can:\n"
                "• Analyze a photo of your room\n"
                "• Suggest artwork based on your style preferences\n"
                "• Help you find pieces within your budget\n\n"
                "What would you like to do first?"
            )

    def _format_context(self, context: Dict[str, Any]) -> str:
        """Format context information for LLM"""
        parts = ["Current context:"]
        
        if "style" in context:
            parts.append(f"- Room style: {context['style']}")
        
        if "colors" in context and context["colors"]:
            try:
                # Handle both list of dicts and list of strings
                color_list = []
                for c in context["colors"][:3]:
                    if isinstance(c, dict):
                        color_list.append(c.get("name", c.get("hex", str(c))))
                    else:
                        color_list.append(str(c))
                colors = ", ".join(color_list)
                parts.append(f"- Dominant colors: {colors}")
            except Exception as e:
                print(f"Error formatting colors: {e}")
        
        if "lighting" in context:
            lighting = context["lighting"]
            if isinstance(lighting, dict):
                parts.append(f"- Lighting: {lighting.get('type', 'Natural')}")
            else:
                parts.append(f"- Lighting: {lighting}")
        
        if "budget" in context and isinstance(context["budget"], dict):
            parts.append(f"- Budget: ${context['budget'].get('min', 0)}-${context['budget'].get('max', 1000)}")
        
        return "\n".join(parts)

    def _generate_suggestions(
        self, message: str, context: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """Generate follow-up suggestions"""
        message_lower = message.lower()
        
        # Context-aware suggestions
        if context and "style" in context:
            return [
                "Show me the top recommendations",
                "I want something in a different color",
                "What's trending in décor right now?",
            ]
        
        # Based on message content
        if any(word in message_lower for word in ["upload", "photo", "image", "analyze"]):
            return [
                "What style works best for my room?",
                "Show me similar artwork",
                "Find stores near me",
            ]
        elif any(word in message_lower for word in ["budget", "price", "cost"]):
            return [
                "Show me options under $100",
                "What about mid-range pieces?",
                "Find premium artwork",
            ]
        else:
            return [
                "Upload a room photo for analysis",
                "Tell me about different styles",
                "What's in my price range?",
            ]
    
    async def generate_reasoning(
        self,
        artwork_title: str,
        artwork_style: str,
        room_style: Optional[str] = None,
        colors: Optional[List[str]] = None,
        match_score: float = 0.0,
        artwork_tags: Optional[List[str]] = None,
    ) -> str:
        """
        Generate AI-powered reasoning for why an artwork matches a room
        
        Args:
            artwork_title: Name of the artwork
            artwork_style: Style of the artwork (e.g., "Abstract", "Modern")
            room_style: Detected room style (e.g., "Modern Minimalist")
            colors: Dominant colors in the room
            match_score: FAISS similarity score (0-100)
            artwork_tags: Tags associated with the artwork
        
        Returns:
            AI-generated reasoning text
        """
        if not self.api_key:
            # Fallback to template if no API key
            return f"This {artwork_style} piece complements your {room_style or 'room'} with a {match_score:.0f}% match."
        
        try:
            # Build context for LLM
            color_desc = f" with colors like {', '.join(colors[:2])}" if colors else ""
            prompt = f"""Write 1-2 sentences explaining why the {artwork_style} artwork "{artwork_title}" matches a {room_style or 'modern'} room{color_desc}. Focus on style harmony and aesthetic benefits."""

            if self.provider == "ollama":
                return await self._ollama_reasoning_request(prompt)
            elif self.provider == "groq":
                return await self._groq_reasoning_request(prompt)
            elif self.provider == "gemini":
                return await self._gemini_reasoning_request(prompt)
            elif self.provider == "openai":
                return await self._openai_reasoning_request(prompt)
            else:
                return f"This {artwork_style} piece complements your {room_style or 'room'} with a {match_score:.0f}% match."
                
        except Exception as e:
            print(f"Error generating reasoning: {e}")
            # Fallback to template
            return f"This {artwork_style} piece complements your {room_style or 'room'} with a {match_score:.0f}% match."
    
    async def _ollama_reasoning_request(self, prompt: str) -> str:
        """Generate reasoning using Ollama (LLaVA/Llama Vision)"""
        try:
            import httpx
            
            url = f"{self.ollama_base_url}/api/generate"
            
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 150,
                }
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                result = response.json()
                
                if "response" in result:
                    return result["response"].strip()
                else:
                    raise Exception(f"Unexpected Ollama response format: {result}")
                    
        except Exception as e:
            raise Exception(f"Ollama reasoning error: {e}")
    
    async def _gemini_reasoning_request(self, prompt: str) -> str:
        """Generate reasoning using Gemini"""
        try:
            import google.generativeai as genai
            from google.generativeai.types import HarmCategory, HarmBlockThreshold
            
            genai.configure(api_key=self.api_key)
            
            # Configure with minimal safety restrictions for interior design content
            safety_settings = {
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }
            
            model = genai.GenerativeModel(
                model_name=self.model,
                safety_settings=safety_settings
            )
            
            response = await model.generate_content_async(
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=150,
                )
            )
            
            # Handle response properly
            if hasattr(response, 'text') and response.text:
                return response.text.strip()
            
            # If blocked or no text, check candidates
            if response.candidates and len(response.candidates) > 0:
                candidate = response.candidates[0]
                
                # Check if we have content despite safety block
                if candidate.content and candidate.content.parts:
                    text = "".join(part.text for part in candidate.content.parts if hasattr(part, 'text'))
                    if text:
                        return text.strip()
                
                # Log finish reason for debugging
                finish_reason = candidate.finish_reason if hasattr(candidate, 'finish_reason') else 'unknown'
                print(f"Gemini finish_reason: {finish_reason}")
                
                if finish_reason == 2:  # SAFETY
                    print("Safety block - using simplified prompt fallback")
                    # Try again with even simpler prompt
                    simple_prompt = f"Describe how {prompt.split('artwork')[1].split('matches')[0] if 'artwork' in prompt else 'this art'} complements the room decor."
                    simple_response = await model.generate_content_async(
                        simple_prompt,
                        generation_config=genai.GenerationConfig(
                            temperature=0.5,
                            max_output_tokens=100,
                        )
                    )
                    if hasattr(simple_response, 'text') and simple_response.text:
                        return simple_response.text.strip()
            
            # If all else fails, raise to trigger template fallback
            raise Exception(f"No valid response from Gemini (finish_reason: {finish_reason if 'finish_reason' in locals() else 'unknown'})")
            
        except Exception as e:
            raise Exception(f"Gemini reasoning error: {e}")
    
    async def _openai_reasoning_request(self, prompt: str) -> str:
        """Generate reasoning using OpenAI"""
        try:
            import openai
            client = openai.AsyncOpenAI(api_key=self.api_key)
            
            response = await client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=150,
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"OpenAI reasoning error: {e}")
    
    async def _groq_reasoning_request(self, prompt: str) -> str:
        """Generate reasoning using Groq"""
        try:
            from groq import AsyncGroq
            client = AsyncGroq(api_key=self.api_key)
            
            response = await client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=150,
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"Groq reasoning error: {e}")


# Singleton instance
_chat_agent_instance = None


def get_chat_agent() -> ChatAgent:
    """Get or create chat agent instance"""
    global _chat_agent_instance
    if _chat_agent_instance is None:
        _chat_agent_instance = ChatAgent()
    return _chat_agent_instance

