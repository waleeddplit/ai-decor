# 🚀 Quick Start Guide - Art.Decor.AI

Get the Art.Decor.AI platform running on your local machine in minutes.

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** 18+ ([Download](https://nodejs.org/))
- **Python** 3.10+ ([Download](https://www.python.org/))
- **Git** ([Download](https://git-scm.com/))

---

## 🎯 Project Structure

```
ai-decorator/
├── frontend/          # Next.js TypeScript app
├── backend/           # FastAPI Python server (to be implemented)
└── README.md          # Project overview
```

---

## 🖥️ Frontend Setup (Next.js)

### 1. Navigate to Frontend Directory
```bash
cd ai-decorator/frontend
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Start Development Server
```bash
npm run dev
```

The frontend will be available at: **http://localhost:3000**

### 4. Build for Production (Optional)
```bash
npm run build
npm start
```

---

## 🐍 Backend Setup (FastAPI)

> **Note**: Backend implementation is pending. This section will be updated in future steps.

### Coming Soon:
1. Python virtual environment setup
2. FastAPI server installation
3. AI model integration
4. Database configuration
5. API endpoint implementation

---

## 🌐 Access the Application

Once the frontend is running:

1. **Landing Page**: http://localhost:3000
2. **Upload Room**: http://localhost:3000/upload
3. **Chat Interface**: http://localhost:3000/chat
4. **Results** (demo): http://localhost:3000/results

---

## 🎨 Features Available

### ✅ Currently Working
- ✨ Beautiful landing page with feature showcase
- 📤 Image upload interface with drag-and-drop
- 💬 Interactive chat UI (mock responses)
- 🎨 Recommendation display (mock data)
- 🌗 Dark/light theme toggle
- 📱 Fully responsive design

### ⏳ Coming Soon (Backend Integration)
- 🤖 Real AI room analysis (YOLOv8 + CLIP)
- 🎯 Personalized décor recommendations
- 📈 Trend intelligence (Tavily API)
- 📍 Local store finder (Google Maps API)
- 🗣️ Voice input (Whisper)
- 👤 User profiles (Supabase)

---

## 🔧 Configuration

### Frontend Environment Variables

Create `/frontend/.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend Environment Variables (Coming Soon)

Create `/backend/.env`:
```env
# Database
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key

# AI APIs
OPENAI_API_KEY=your_openai_key
GROQ_API_KEY=your_groq_key
TAVILY_API_KEY=your_tavily_key

# Google Maps
GOOGLE_MAPS_API_KEY=your_google_maps_key

# AWS S3
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_S3_BUCKET=your_bucket_name
```

---

## 🧪 Testing the Frontend

### 1. Navigate Through Pages
- Click "Upload Room Photo" on landing page
- Try uploading an image (mock flow)
- Explore the chat interface
- View mock recommendations on results page

### 2. Test Theme Toggle
- Click the sun/moon icon in navbar
- Verify smooth dark/light mode transition

### 3. Check Responsive Design
- Resize browser window
- Test on mobile viewport (DevTools)
- Verify all pages are mobile-friendly

---

## 📦 Tech Stack Reference

### Frontend
- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS 4
- **Icons**: Lucide React
- **Theme**: next-themes

### Backend (Planned)
- **Framework**: FastAPI
- **Language**: Python 3.10+
- **AI Models**: YOLOv8, CLIP, LLaVA
- **Database**: Supabase (PostgreSQL)
- **Vector DB**: FAISS
- **Storage**: AWS S3

---

## 🐛 Troubleshooting

### Frontend Issues

**Problem**: `npm install` fails
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Problem**: Port 3000 already in use
```bash
# Use different port
PORT=3001 npm run dev
```

**Problem**: Build errors
```bash
# Check Node.js version
node --version  # Should be 18+

# Reinstall dependencies
npm install
```

### Common Errors

| Error | Solution |
|-------|----------|
| "Cannot find module" | Run `npm install` |
| "Port already in use" | Kill process or use different port |
| TypeScript errors | Check `tsconfig.json` and dependencies |

---

## 📚 Next Steps

### For Developers

1. ✅ **Explore the frontend** - Navigate through all pages
2. ⏳ **Wait for backend steps** - FastAPI implementation coming
3. 🔌 **API integration** - Connect frontend to backend
4. 🧪 **Add tests** - Unit and E2E testing
5. 🚀 **Deploy** - Vercel (frontend) + Render (backend)

### Current Development Status

| Component | Status |
|-----------|--------|
| Frontend Structure | ✅ Complete |
| UI/UX Design | ✅ Complete |
| Theme System | ✅ Complete |
| Backend Setup | ⏳ Pending |
| AI Agents | ⏳ Pending |
| Database | ⏳ Pending |
| API Integration | ⏳ Pending |

---

## 🤝 Getting Help

### Documentation
- Frontend README: `/frontend/README.md`
- Features List: `/frontend/FEATURES.md`
- Main README: `/README.md`

### Resources
- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

---

## 🎉 You're Ready!

The frontend is fully functional and ready for exploration. Backend implementation will follow in subsequent steps.

**Happy coding!** 🚀

---

**Last Updated**: Step 2 - Frontend Complete
**Next**: Step 3 - Backend Setup

