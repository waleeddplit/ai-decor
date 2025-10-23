# 🦙 Ollama + LLaVA/Llama Vision Setup

## ✅ Why Use Ollama + LLaVA?

**Advantages over Gemini:**
- ✅ **100% Free** - No API costs
- ✅ **No Safety Blocks** - Full control over responses
- ✅ **Privacy** - Runs locally on your machine
- ✅ **Fast** - No network latency (after initial download)
- ✅ **Reliable** - No rate limits or API failures
- ✅ **Open Source** - Meta's Llama models

**Perfect for:**
- Interior design recommendations
- Artwork reasoning generation
- Local development and testing

---

## 🚀 Quick Setup (5 minutes)

### Step 1: Install Ollama

**macOS/Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
Download from: https://ollama.com/download

**Verify installation:**
```bash
ollama --version
```

### Step 2: Pull LLaVA Model

**Option A: LLaVA (Recommended for reasoning)**
```bash
ollama pull llava
```
Size: ~4.7 GB

**Option B: Llama 3.2 Vision (Latest, better quality)**
```bash
ollama pull llama3.2-vision
```
Size: ~7.9 GB

**Option C: Llama 3.2 3B (Smaller, faster)**
```bash
ollama pull llama3.2
```
Size: ~2 GB

### Step 3: Test Ollama

```bash
ollama run llava "Describe modern interior design in one sentence"
```

Expected output:
```
Modern interior design emphasizes clean lines, minimal ornamentation...
```

### Step 4: Configure Backend

**Edit `backend/.env`:**
```bash
# Enable Ollama
USE_OLLAMA="true"
OLLAMA_BASE_URL="http://localhost:11434"
CHAT_MODEL="llava"

# Comment out other API keys
# GEMINI_API_KEY="..."
# OPENAI_API_KEY="..."
```

### Step 5: Install httpx (if needed)

```bash
cd backend
./venv/bin/pip install httpx==0.27.0
```

### Step 6: Restart Backend

```bash
cd backend
pkill -f "python.*main.py"
./venv/bin/python main.py
```

---

## 🧪 Test Reasoning

```bash
cd backend
./venv/bin/python scripts/test_gemini_reasoning.py
```

**Expected Output:**
```
✅ Using OLLAMA with model: llava

Test 1: Abstract Geometric Canvas
  🤖 AI Reasoning:
     The abstract geometric canvas complements a modern minimalist room 
     through its clean lines and neutral color palette, creating visual 
     harmony while adding artistic interest without overwhelming the space.
```

---

## 📊 Model Comparison

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| **llava** | 4.7GB | Fast | Good | General reasoning |
| **llama3.2-vision** | 7.9GB | Medium | Excellent | High-quality responses |
| **llama3.2** | 2GB | Very Fast | Good | Quick responses |

---

## 🎯 Configuration Options

### Basic Configuration
```bash
# backend/.env
USE_OLLAMA="true"
CHAT_MODEL="llava"
```

### Custom Ollama Host
```bash
# If Ollama runs on different port/host
OLLAMA_BASE_URL="http://localhost:11434"  # Default
# or
OLLAMA_BASE_URL="http://192.168.1.100:11434"  # Remote host
```

### Switch Models
```bash
# For best quality
CHAT_MODEL="llama3.2-vision"

# For fastest responses
CHAT_MODEL="llama3.2"

# For balanced performance
CHAT_MODEL="llava"
```

---

## 🔄 How It Works

### Architecture:
```
Frontend Upload Image
    ↓
Backend Analyze Room
    ↓
FAISS Find Artworks
    ↓
For each artwork:
    ↓
Ollama (LLaVA) Generate Reasoning ✨
    ↓
Return Recommendations
```

### API Call:
```python
# ChatAgent automatically uses Ollama
reasoning = await chat_agent.generate_reasoning(
    artwork_title="Abstract Canvas",
    artwork_style="Modern",
    room_style="Minimalist",
    colors=["#E8E8E8", "#4A4A4A"],
    match_score=95.0
)
```

### Ollama Request:
```json
POST http://localhost:11434/api/generate
{
  "model": "llava",
  "prompt": "Write 1-2 sentences explaining why...",
  "stream": false,
  "options": {
    "temperature": 0.7,
    "num_predict": 150
  }
}
```

---

## 🐛 Troubleshooting

### Ollama not found
```bash
# Check if running
ollama list

# Start Ollama service (if not running)
ollama serve
```

### Model not found
```bash
# List installed models
ollama list

# Pull missing model
ollama pull llava
```

### Connection refused
```bash
# Check Ollama is running
curl http://localhost:11434/api/tags

# If not, start Ollama
ollama serve
```

### Slow responses
```bash
# Use smaller model
ollama pull llama3.2
# Update .env
CHAT_MODEL="llama3.2"
```

---

## 💡 Tips

### Performance Optimization:
1. **Use GPU** - Ollama auto-detects CUDA/Metal
2. **Smaller models** - llama3.2 for speed
3. **Keep Ollama running** - Faster subsequent requests
4. **Increase context** - For longer responses

### Quality Optimization:
1. **Use llama3.2-vision** - Best quality
2. **Adjust temperature** - Lower for consistency
3. **Specific prompts** - Better results

### Cost Savings:
```
Gemini API: ~$0.10 per 1K requests
OpenAI GPT-4: ~$0.30 per 1K requests
Ollama LLaVA: $0.00 (FREE!) ✅
```

---

## 🎉 Benefits

### With Ollama + LLaVA:
- ✅ **No safety blocks** - Gemini issue solved!
- ✅ **Free forever** - No API costs
- ✅ **Fast responses** - Local inference
- ✅ **Full control** - Customize prompts
- ✅ **Privacy** - Data stays local

### Example Reasoning (LLaVA):
```
"The modern abstract geometric canvas perfectly complements your 
minimalist aesthetic with its clean lines and neutral gray tones, 
creating a sophisticated focal point that enhances the room's 
contemporary style without overwhelming the space."
```

---

## 📚 Resources

- **Ollama**: https://ollama.com
- **LLaVA**: https://llava-vl.github.io
- **Llama 3.2**: https://ai.meta.com/llama
- **Models**: https://ollama.com/library

---

## 🔄 Fallback Chain

```
1. Try Ollama (if USE_OLLAMA=true)
   ↓ fail
2. Try Groq (if GROQ_API_KEY set)
   ↓ fail
3. Try Gemini (if GEMINI_API_KEY set)
   ↓ fail
4. Try OpenAI (if OPENAI_API_KEY set)
   ↓ fail
5. Use template fallback
```

**With Ollama, you'll never need fallback!** ✅

---

**Status:** ✅ Ollama + LLaVA Support Complete  
**Your Art.Decor.AI now runs 100% locally with open-source AI!** 🦙

