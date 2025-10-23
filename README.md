# 🎨 Art.Decor.AI

> **AI-Powered Home Décor Recommendation Platform**

Art.Decor.AI is an intelligent interior design assistant that helps users discover wall art and décor perfectly matched to their space. By analyzing room photos or processing text/voice descriptions, it provides curated, trend-aware décor recommendations tailored to your room's style, lighting, and color palette.

---

## 🌟 Key Features

- **📸 Multimodal Input**: Upload room photos, describe via text, or use voice commands
- **🤖 AI-Powered Analysis**: Computer vision detects walls, furniture, colors, and lighting
- **🎯 Smart Recommendations**: Personalized décor suggestions based on room aesthetics
- **📈 Trend Intelligence**: Real-time trending styles and seasonal décor insights
- **📍 Local Store Finder**: Discover nearby galleries and décor stores with availability
- **💬 Conversational UI**: Natural chat interface powered by multimodal AI agents
- **👤 User Profiles**: Save preferences and get increasingly personalized suggestions

---

## 🏗️ Architecture

### Frontend (`/frontend`)
- **Framework**: Next.js 14+ (TypeScript)
- **Styling**: Tailwind CSS + shadcn/ui components
- **Features**: Image upload, chat interface, recommendation gallery, voice input

### Backend (`/backend`)
- **Framework**: FastAPI (Python)
- **Purpose**: AI agent orchestration, session management, API gateway
- **Structure**:
  - `/agents/` — AI logic modules
  - `/routes/` — REST API endpoints
  - `/db/` — Database integrations

---

## 🤖 AI Agent System

### 1. **VisionMatchAgent**
- Object detection with YOLOv8
- Style embedding via CLIP/DINOv2
- Extracts: wall space, furniture, color palette, lighting conditions

### 2. **TrendIntelAgent**
- Fetches current décor trends via Tavily API
- Seasonal and regional style adaptation
- Influences recommendation ranking

### 3. **GeoFinderAgent**
- Google Maps API integration
- Finds local art galleries and décor stores
- Provides availability and distance info

### 4. **DecisionRouter**
- Orchestrates all agents
- Multimodal reasoning with LLaVA/Llama 3 Vision
- Generates natural language explanations

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Frontend** | Next.js, TypeScript, Tailwind CSS, shadcn/ui |
| **Backend** | FastAPI, Python 3.10+ |
| **Vision AI** | YOLOv8, CLIP, DINOv2, LLaVA |
| **Voice** | Whisper (transcription), Groq TTS |
| **Database** | Supabase (PostgreSQL) |
| **Vector DB** | FAISS (Meta) |
| **Storage** | AWS S3 |
| **APIs** | Tavily (trends), Google Maps (geo) |
| **Hosting** | Vercel (frontend), Render (backend) |

---

## 📁 Project Structure

```
ai-decorator/
├── frontend/           # Next.js TypeScript app
│   ├── app/           # App router pages
│   ├── components/    # React components
│   ├── lib/           # Utilities & API clients
│   └── public/        # Static assets
│
├── backend/           # FastAPI Python server
│   ├── agents/        # AI agent modules
│   ├── routes/        # API endpoints
│   ├── db/            # Database connectors
│   ├── models/        # Pydantic schemas
│   └── main.py        # FastAPI app entry
│
└── README.md          # This file
```

---

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ (for frontend)
- Python 3.10+ (for backend)
- Supabase account
- AWS S3 bucket
- API keys: Tavily, Google Maps, OpenAI/Groq

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## 🎯 Core Workflow

1. **User uploads** room photo or provides text description
2. **VisionMatchAgent** analyzes room aesthetics and extracts features
3. **TrendIntelAgent** fetches current décor trends relevant to the style
4. **Backend** queries FAISS vector DB for matching artwork embeddings
5. **GeoFinderAgent** finds local stores with similar items
6. **DecisionRouter** synthesizes all data into ranked recommendations
7. **Frontend** displays results with reasoning and purchase options

---

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/analyze_room` | POST | Upload image for room analysis |
| `/recommend` | POST | Get décor recommendations |
| `/profile` | GET/PUT | Manage user preferences |
| `/stores` | GET | Find nearby décor stores |
| `/trends` | GET | Fetch current design trends |

---

## 🎨 Design Philosophy

- **Modular**: Each agent is independently testable and swappable
- **Scalable**: Designed for cloud deployment and horizontal scaling
- **Type-Safe**: Full TypeScript frontend + Pydantic backend schemas
- **User-Centric**: Natural language interactions, clear explanations
- **Extensible**: Easy to add new agents or data sources

---

## 📅 Development Roadmap

- [x] Project architecture defined
- [ ] Backend agent system implementation
- [ ] Frontend UI components and layout
- [ ] Database schema and integrations
- [ ] AI model pipeline integration
- [ ] Voice input/output features
- [ ] User authentication and profiles
- [ ] Local store API integration
- [ ] Testing and optimization
- [ ] Production deployment

---

## 👥 Contributing

This is an educational project demonstrating:
- Multi-agent AI systems
- Full-stack TypeScript/Python development
- Computer vision and NLP integration
- Vector database usage
- Modern web architecture patterns

---

## 📄 License

MIT License - Educational and demonstration purposes

---

## 🙏 Acknowledgments

Built with:
- [Next.js](https://nextjs.org/) - React framework
- [FastAPI](https://fastapi.tiangolo.com/) - Python web framework
- [YOLOv8](https://github.com/ultralytics/ultralytics) - Object detection
- [CLIP](https://github.com/openai/CLIP) - Vision embeddings
- [Supabase](https://supabase.com/) - Backend as a service
- [FAISS](https://github.com/facebookresearch/faiss) - Vector similarity search

---

**Built with ❤️ for creative spaces**

