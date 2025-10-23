# 🔮 Google Gemini Setup Guide

## ✨ Why Gemini?

Google's Gemini is a great alternative to OpenAI:
- ✅ **Free tier** - Generous free quota
- ✅ **Fast** - Quick response times
- ✅ **Multimodal** - Supports text and images
- ✅ **Good quality** - Comparable to GPT-3.5
- ✅ **Easy to use** - Simple API

---

## 🚀 Quick Setup

### Step 1: Get Your Gemini API Key

1. Go to: https://makersuite.google.com/app/apikey
2. Click **"Create API Key"**
3. Choose a project or create new one
4. Copy your API key (starts with `AIza...`)

### Step 2: Install Gemini Package

```bash
cd backend
./venv/bin/pip install google-generativeai
```

### Step 3: Add API Key to .env

```bash
cd backend
echo "GEMINI_API_KEY=AIza-your-key-here" >> .env
echo "CHAT_MODEL=gemini-1.5-flash" >> .env
```

### Step 4: Restart Backend

```bash
cd backend
./venv/bin/python main.py
```

You should see:
```
🚀 Starting Art.Decor.AI Backend...
✅ Supabase client initialized
✅ FAISS client initialized (10 vectors)
✨ Backend ready!
```

### Step 5: Test Chat

Go to: http://localhost:3000/chat

Type: "Hello, recommend me some art!"

You'll get natural language responses from Gemini! 🎉

---

## 🎯 Available Gemini Models

### **gemini-1.5-flash** (Recommended)
- ⚡ Fastest
- 💰 Most cost-effective
- ✅ Best for chat

### **gemini-1.5-pro**
- 🧠 Smartest
- 💪 Most capable
- 🎯 Best for complex tasks

### **gemini-pro**
- ⚖️ Balanced
- 📝 Good for general use

To change model:
```bash
echo "CHAT_MODEL=gemini-1.5-pro" >> backend/.env
```

---

## 🔄 Provider Priority

The chat agent automatically detects which API key you have:

**Priority order:**
1. **Gemini** - If `GEMINI_API_KEY` is set
2. **OpenAI** - If `OPENAI_API_KEY` is set
3. **Groq** - If `GROQ_API_KEY` is set
4. **Fallback** - Rule-based responses

You can have multiple API keys and switch by commenting/uncommenting in `.env`:

```bash
# Option 1: Use Gemini
GEMINI_API_KEY=AIza-your-key
CHAT_MODEL=gemini-1.5-flash

# Option 2: Use OpenAI (comment out Gemini)
# GEMINI_API_KEY=AIza-your-key
# OPENAI_API_KEY=sk-your-key
# CHAT_MODEL=gpt-3.5-turbo

# Option 3: Use Groq (comment out others)
# GROQ_API_KEY=your-key
# CHAT_MODEL=llama3-8b-8192
```

---

## 💡 Example Conversations

### With Gemini:
**You:** "I want modern art for my living room"  
**AI:** "I'd be happy to help you find modern art for your living room! To give you the best recommendations, could you tell me a bit more about your space? For example, what's the color palette of your room? What kind of mood are you hoping to create?"

### Features:
- ✅ Natural language understanding
- ✅ Context-aware responses
- ✅ Creative suggestions
- ✅ Personalized recommendations
- ✅ Follow-up questions

---

## 📊 Comparison

| Feature | Gemini | OpenAI | Groq | Fallback |
|---------|--------|--------|------|----------|
| Free Tier | ✅ Yes | ❌ No | ✅ Yes | ✅ Always |
| Speed | ⚡⚡⚡ | ⚡⚡ | ⚡⚡⚡⚡ | ⚡⚡⚡⚡⚡ |
| Quality | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Cost | 💰 Free tier | 💰💰 Paid | 💰 Free tier | 💰 Free |
| Multimodal | ✅ Yes | ✅ Yes | ❌ No | ❌ No |

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'google.generativeai'"
**Fix:**
```bash
cd backend
./venv/bin/pip install google-generativeai
```

### "API key not valid"
**Fix:**
- Check your key starts with `AIza...`
- Make sure you enabled the API in Google Cloud Console
- Verify the key is in `backend/.env`

### "Chat works but uses fallback responses"
**Fix:**
- Make sure `GEMINI_API_KEY` is set in `.env`
- Restart backend to pick up new environment variables
- Check backend terminal for error messages

### "Quota exceeded"
**Fix:**
- Gemini has generous free tier (60 requests/minute)
- Wait a minute and try again
- Or upgrade to paid tier for higher limits

---

## 🎉 You're All Set!

Your chat now uses Google Gemini for:
- ✅ Natural conversations
- ✅ Smart recommendations
- ✅ Context awareness
- ✅ Creative suggestions

**Test it now at:** http://localhost:3000/chat

---

## 📚 Resources

- **Gemini API Docs:** https://ai.google.dev/docs
- **Get API Key:** https://makersuite.google.com/app/apikey
- **Pricing:** https://ai.google.dev/pricing
- **Models:** https://ai.google.dev/models

---

**Made with ❤️ by Art.Decor.AI**
