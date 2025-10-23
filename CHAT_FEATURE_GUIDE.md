# 🗣️ Chat Interface - Setup & Usage Guide

## ✨ What's New

You now have a **fully functional AI chat interface** for conversational décor recommendations!

### Features:
- 💬 **Natural language conversations** with AI designer
- 🎨 **Context-aware responses** (uses room analysis data)
- 📸 **Image upload** in chat for room analysis
- 💡 **Smart suggestions** for follow-up questions
- 🔄 **Conversation history** maintained per session
- ⚡ **Real-time responses** with loading indicators
- 🎯 **Artwork recommendations** directly in chat

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd backend
./venv/bin/pip install openai groq
```

**Or install all updated requirements:**
```bash
./venv/bin/pip install -r requirements.txt
```

### 2. Set Up API Keys

You need **ONE** of these LLM providers:

**Option A: OpenAI (Recommended for best quality)**
```bash
cd backend
echo "OPENAI_API_KEY=sk-your-key-here" >> .env
echo "CHAT_MODEL=gpt-3.5-turbo" >> .env
```

Get your key: https://platform.openai.com/api-keys

**Option B: Groq (Free tier, faster)**
```bash
cd backend
echo "GROQ_API_KEY=your-key-here" >> .env
echo "CHAT_MODEL=llama3-8b-8192" >> .env
```

Get your key: https://console.groq.com/keys

### 3. Start Backend

```bash
cd backend
./venv/bin/python main.py
```

**Expected output:**
```
🚀 Starting Art.Decor.AI Backend...
✅ Supabase client initialized
✅ FAISS client initialized (10 vectors)
🤖 Initializing AI agents...
✅ AI agents ready
✨ Backend ready!
```

### 4. Test Chat API

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I want modern art for my living room"
  }'
```

**Expected response:**
```json
{
  "message": "Great choice! Modern art is...",
  "conversation_id": "uuid-here",
  "suggestions": [
    "Show me the top recommendations",
    "I want something in a different color",
    "What's trending in décor right now?"
  ],
  "metadata": {
    "processing_time": 0.5
  }
}
```

### 5. Use Chat Interface

1. Go to: http://localhost:3000/chat
2. Type a message or upload a room image
3. Get AI-powered recommendations!

---

## 💡 Example Conversations

### Simple Query
**You:** "I need artwork for my bedroom"
**AI:** Suggests styles, asks about preferences

### With Context
**You:** (After analyzing room on /upload page)
       Go to /chat
**You:** "Show me recommendations for my room"
**AI:** Uses your room analysis to give personalized suggestions

### With Image
**You:** (Click image icon, upload room photo)
       "What style would work here?"
**AI:** Analyzes image and recommends artwork

---

## 🎯 How It Works

### Backend Flow:
```
1. User sends message
   ↓
2. ChatAgent receives request
   ↓
3. Checks for conversation history
   ↓
4. Adds context (room analysis if available)
   ↓
5. Calls LLM (OpenAI/Groq)
   ↓
6. Generates suggestions
   ↓
7. Returns response
```

### Frontend Flow:
```
1. User types message
   ↓
2. Checks sessionStorage for room analysis
   ↓
3. Sends to /api/chat with context
   ↓
4. Displays response
   ↓
5. Shows suggestions
   ↓
6. User clicks suggestion or types new message
```

---

## 🛠️ API Endpoints

### POST `/api/chat`
Send a chat message

**Request:**
```json
{
  "message": "I want minimalist art",
  "conversation_id": "optional-uuid",
  "image": "optional-base64-image",
  "context": {
    "style": "Modern",
    "style_vector": [512 floats],
    "colors": ["#FFFFFF", "#000000"]
  }
}
```

**Response:**
```json
{
  "message": "For minimalist spaces...",
  "conversation_id": "uuid",
  "suggestions": ["...", "...", "..."],
  "recommendations": [...],  // Optional artwork list
  "metadata": {
    "processing_time": 0.5
  }
}
```

### GET `/api/chat/history/{conversation_id}`
Get conversation history

### DELETE `/api/chat/history/{conversation_id}`
Clear conversation history

---

## 🎨 Fallback Mode

**No API key?** The chat still works!

The `ChatAgent` has intelligent fallback responses:
- Style recommendations
- Color advice
- Budget suggestions
- Design tips

It won't use LLM but will provide helpful rule-based responses.

---

## 🔧 Customization

### Change LLM Model

**For OpenAI:**
```bash
# GPT-3.5 Turbo (faster, cheaper)
CHAT_MODEL=gpt-3.5-turbo

# GPT-4 (smarter, slower)
CHAT_MODEL=gpt-4

# GPT-4 Turbo
CHAT_MODEL=gpt-4-turbo-preview
```

### Change System Prompt

Edit `backend/agents/chat_agent.py`:
```python
self.system_prompt = """
Your custom prompt here...
"""
```

### Add Custom Suggestions

Edit `_generate_suggestions()` in `chat_agent.py`

---

## 🐛 Troubleshooting

### "Chat error: No API key configured"
**Fix:** Add `OPENAI_API_KEY` or `GROQ_API_KEY` to `.env`

### "ModuleNotFoundError: No module named 'openai'"
**Fix:** `./venv/bin/pip install openai groq`

### Chat works but responses are generic
**Fix:** Using fallback mode. Add API key for LLM responses.

### Image upload not working
**Fix:** Check file size < 5MB and type is image/*

### Suggestions not showing
**Fix:** Normal, suggestions appear after first AI response

---

## 📊 What's Next?

**Current Status:**
- ✅ Basic chat working
- ✅ Image upload
- ✅ Context awareness
- ✅ Suggestions
- ⏳ Streaming responses (optional enhancement)
- ⏳ Voice input (optional enhancement)

**Optional Enhancements:**
1. **Streaming Responses** - Real-time word-by-word responses
2. **Voice Input** - Whisper API integration
3. **Multi-turn Analysis** - Remember multiple room analyses
4. **Artwork Preview** - Show images inline in chat
5. **Export Conversation** - Download chat history

---

## 🎉 Ready to Use!

Your chat interface is fully functional. Try it now:

1. **Start backend:** `cd backend && ./venv/bin/python main.py`
2. **Go to:** http://localhost:3000/chat
3. **Ask anything** about décor!

Example prompts:
- "What style works for small apartments?"
- "Show me colorful abstract art"
- "I have a modern living room, recommend art"
- (Upload image) "Analyze this room"

---

**Made with ❤️ by Art.Decor.AI**
