# 🗺️ Art.Decor.AI Project Map

**Complete visual guide to the project structure and navigation**

---

## 📂 Directory Tree

```
ai-decorator/
│
├── 📄 README.md                    # Project overview & architecture
├── 📄 QUICKSTART.md                # Setup and running instructions
├── 📄 STATUS.md                    # Current progress tracker
├── 📄 PROJECT_MAP.md               # This file - navigation guide
├── 📄 STEP2_SUMMARY.md             # Step 2 completion report
│
├── 📁 frontend/                    # ✅ COMPLETE
│   │
│   ├── 📁 src/
│   │   │
│   │   ├── 📁 app/                 # Next.js App Router
│   │   │   ├── 📄 page.tsx         # 🏠 Landing page (/)
│   │   │   ├── 📄 layout.tsx       # Root layout with theme
│   │   │   ├── 📄 globals.css      # Global styles
│   │   │   │
│   │   │   ├── 📁 upload/
│   │   │   │   └── 📄 page.tsx     # 📤 Upload page (/upload)
│   │   │   │
│   │   │   ├── 📁 results/
│   │   │   │   └── 📄 page.tsx     # 🎨 Results page (/results)
│   │   │   │
│   │   │   └── 📁 chat/
│   │   │       └── 📄 page.tsx     # 💬 Chat page (/chat)
│   │   │
│   │   └── 📁 components/
│   │       ├── 📄 navbar.tsx       # Navigation bar
│   │       ├── 📄 theme-provider.tsx  # Theme context
│   │       └── 📄 theme-toggle.tsx    # Theme switcher
│   │
│   ├── 📁 public/                  # Static assets
│   │   ├── file.svg
│   │   ├── globe.svg
│   │   ├── next.svg
│   │   ├── vercel.svg
│   │   └── window.svg
│   │
│   ├── 📄 package.json             # Dependencies
│   ├── 📄 tsconfig.json            # TypeScript config
│   ├── 📄 next.config.ts           # Next.js config
│   ├── 📄 tailwind.config.ts       # Tailwind config (implicit)
│   ├── 📄 README.md                # Frontend documentation
│   ├── 📄 FEATURES.md              # Feature breakdown
│   └── 📄 TESTING.md               # Testing guide
│
└── 📁 backend/                     # ⏳ PENDING (Step 3+)
    └── (to be implemented)
```

---

## 🧭 Page Navigation Map

```
┌─────────────────────────────────────────────────────────┐
│                    🏠 Landing (/)                       │
│  • Hero section with brand messaging                    │
│  • Feature cards (3)                                    │
│  • How it works (4 steps)                              │
│  • CTAs                                                 │
│                                                         │
│  ┌──────────────┐        ┌──────────────┐            │
│  │ Upload Photo │───────▶│ Start Chat   │            │
│  └──────────────┘        └──────────────┘            │
└─────────────────────────────────────────────────────────┘
           │                        │
           ▼                        ▼
┌──────────────────┐      ┌──────────────────┐
│ 📤 Upload        │      │ 💬 Chat          │
│ (/upload)        │◀────▶│ (/chat)          │
│                  │      │                  │
│ • Drag-drop      │      │ • Message UI     │
│ • File browser   │      │ • AI responses   │
│ • Description    │      │ • Voice toggle   │
│ • Submit         │      │ • History        │
└──────────────────┘      └──────────────────┘
           │                        │
           │                        │
           ▼                        │
┌──────────────────────────────────┘
│
│  ┌─────────────────────────────────┐
└─▶│ 🎨 Results (/results)           │
   │                                  │
   │ • Room analysis                  │
   │ • Recommendations (3)            │
   │ • Match scores                   │
   │ • AI reasoning                   │
   │ • Store availability             │
   └──────────────────────────────────┘
```

---

## 🎯 Feature Map

### Core Features (Implemented)

```
Art.Decor.AI Frontend
│
├─ 🎨 UI/UX
│  ├─ Landing page design
│  ├─ Upload interface
│  ├─ Results display
│  ├─ Chat interface
│  └─ Navigation system
│
├─ 🌗 Theme System
│  ├─ Dark mode
│  ├─ Light mode
│  ├─ System detection
│  ├─ Toggle button
│  └─ Persistence
│
├─ 📱 Responsive Design
│  ├─ Mobile (< 640px)
│  ├─ Tablet (640-1024px)
│  └─ Desktop (> 1024px)
│
├─ 🧩 Components
│  ├─ Navbar (with active states)
│  ├─ ThemeProvider
│  └─ ThemeToggle
│
└─ 🎭 Mock Data
   ├─ Room analysis (simulated)
   ├─ Recommendations (static)
   └─ Chat responses (rule-based)
```

### Pending Features (Backend Required)

```
Backend Integration
│
├─ 🤖 AI Processing
│  ├─ YOLOv8 (object detection)
│  ├─ CLIP (embeddings)
│  ├─ LLaVA (multimodal reasoning)
│  └─ Whisper (voice)
│
├─ 💾 Data Storage
│  ├─ Supabase (PostgreSQL)
│  ├─ FAISS (vector DB)
│  └─ AWS S3 (images)
│
├─ 🌐 External APIs
│  ├─ Tavily (trends)
│  └─ Google Maps (stores)
│
└─ 👤 User System
   ├─ Authentication
   ├─ Profiles
   └─ Preferences
```

---

## 📊 Component Hierarchy

```
RootLayout
│
├─ ThemeProvider (wraps everything)
│  │
│  ├─ Navbar
│  │  ├─ Logo
│  │  ├─ Navigation Links
│  │  │  ├─ Home
│  │  │  ├─ Upload
│  │  │  └─ Chat
│  │  └─ ThemeToggle
│  │
│  └─ Main Content (per page)
│     │
│     ├─ Landing Page (/)
│     │  ├─ Hero Section
│     │  ├─ Features Grid
│     │  ├─ How It Works
│     │  ├─ CTA Section
│     │  └─ Footer
│     │
│     ├─ Upload Page (/upload)
│     │  ├─ Header
│     │  ├─ Upload Zone
│     │  ├─ Description Input
│     │  ├─ Submit Button
│     │  └─ Tips Card
│     │
│     ├─ Results Page (/results)
│     │  ├─ Analysis Summary
│     │  ├─ Recommendations Grid
│     │  │  ├─ Product Card 1
│     │  │  ├─ Product Card 2
│     │  │  └─ Product Card 3
│     │  └─ Action Buttons
│     │
│     └─ Chat Page (/chat)
│        ├─ Header
│        ├─ Messages Container
│        │  ├─ Message (Assistant)
│        │  ├─ Message (User)
│        │  └─ Loading Indicator
│        └─ Input Area
│           ├─ Textarea
│           ├─ Voice Button
│           └─ Send Button
```

---

## 🗃️ Data Flow (Current & Future)

### Current (Mock Data)

```
User Action
    │
    ▼
Frontend Component
    │
    ▼
Local State (React)
    │
    ▼
Mock Response (setTimeout)
    │
    ▼
Update UI
```

### Future (With Backend)

```
User Action
    │
    ▼
Frontend Component
    │
    ▼
API Call (fetch)
    │
    ▼
FastAPI Backend
    │
    ├─▶ AI Agent Processing
    │   ├─ VisionMatchAgent
    │   ├─ TrendIntelAgent
    │   ├─ GeoFinderAgent
    │   └─ DecisionRouter
    │
    ├─▶ Database Query
    │   ├─ Supabase
    │   └─ FAISS
    │
    └─▶ External APIs
        ├─ Tavily
        └─ Google Maps
            │
            ▼
        Response JSON
            │
            ▼
    Frontend Update
            │
            ▼
        Display Results
```

---

## 📝 Documentation Map

### For Users
- `README.md` → What is Art.Decor.AI?
- `QUICKSTART.md` → How to get started

### For Developers
- `STATUS.md` → Current progress
- `frontend/README.md` → Frontend tech details
- `frontend/FEATURES.md` → Feature list
- `frontend/TESTING.md` → Testing checklist
- `STEP2_SUMMARY.md` → Step 2 completion
- `PROJECT_MAP.md` → This file (navigation)

### For Future Contributors
- Component comments → In-code documentation
- TypeScript types → Self-documenting interfaces
- Mock data examples → Expected API shapes

---

## 🔗 Key Integration Points

### API Endpoints (To Be Created)

| Endpoint | Frontend Location | Purpose |
|----------|-------------------|---------|
| `POST /api/analyze_room` | `/upload/page.tsx:50` | Room analysis |
| `POST /api/recommend` | `/results/page.tsx` | Get recommendations |
| `POST /api/chat` | `/chat/page.tsx:64` | Chat messages |
| `GET /api/stores` | `/results/page.tsx` | Store locations |

### Environment Variables

| Variable | Usage | Location |
|----------|-------|----------|
| `NEXT_PUBLIC_API_URL` | Backend base URL | All API calls |
| (Future) `NEXT_PUBLIC_SUPABASE_URL` | Database | User features |
| (Future) `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Auth | User features |

---

## 🎨 Design Token Map

### Colors
```css
/* Brand */
--purple-600: #7C3AED
--pink-600: #EC4899

/* Backgrounds */
--bg-light: #FFFFFF
--bg-dark: #0A0A0A

/* Text */
--text-light: #171717
--text-dark: #EDEDED

/* Neutrals */
--gray-100 to --gray-900
```

### Spacing Scale
```
2 → 8px
4 → 16px
6 → 24px
8 → 32px
12 → 48px
16 → 64px
20 → 80px
```

### Typography
```
Font: Inter (Variable)

Sizes:
- xs: 12px
- sm: 14px
- base: 16px
- lg: 18px
- xl: 20px
- 2xl: 24px
- 3xl: 30px
- 4xl: 36px
- 5xl: 48px
- 6xl: 60px

Weights:
- Regular: 400
- Medium: 500
- Semibold: 600
- Bold: 700
```

---

## 🧪 Testing Map

### Manual Tests (See TESTING.md)
1. Landing page → All sections render
2. Upload page → File upload works
3. Results page → Cards display correctly
4. Chat page → Messages send/receive
5. Navigation → Links work
6. Theme → Toggle functions
7. Responsive → Mobile/tablet/desktop
8. Accessibility → Keyboard navigation

### Automated Tests (Future)
- [ ] Unit tests (Jest + Testing Library)
- [ ] E2E tests (Playwright)
- [ ] Visual regression (Percy/Chromatic)
- [ ] Performance (Lighthouse CI)

---

## 🚀 Deployment Map

### Current Setup
```
Development: npm run dev → localhost:3000
Production: npm run build → Static export
```

### Future Deployment
```
┌──────────────┐
│   GitHub     │ (Source control)
└──────┬───────┘
       │
       ▼
┌──────────────┐
│   Vercel     │ (Frontend hosting)
│ Next.js App  │
└──────┬───────┘
       │
       │ API calls
       ▼
┌──────────────┐
│   Render     │ (Backend hosting)
│ FastAPI App  │
└──────┬───────┘
       │
       ├─────▶ Supabase (Database)
       ├─────▶ AWS S3 (Storage)
       ├─────▶ Tavily (Trends API)
       └─────▶ Google Maps (Geo API)
```

---

## 📦 Dependencies Map

### Frontend Production
```json
{
  "next": "16.0.0",           // Framework
  "react": "19.2.0",          // UI library
  "react-dom": "19.2.0",      // React renderer
  "next-themes": "^0.3",      // Theme management
  "lucide-react": "^0.400"    // Icons
}
```

### Frontend Development
```json
{
  "typescript": "^5",              // Type safety
  "@types/node": "^20",            // Node types
  "@types/react": "^19",           // React types
  "@types/react-dom": "^19",       // React DOM types
  "tailwindcss": "^4",             // Styling
  "@tailwindcss/postcss": "^4",    // PostCSS plugin
  "eslint": "^9",                  // Linting
  "eslint-config-next": "16.0.0"   // Next.js ESLint
}
```

### Backend (Future)
```
fastapi
uvicorn
pydantic
supabase
faiss-cpu
ultralytics (YOLOv8)
transformers (CLIP, LLaVA)
openai (Whisper)
tavily-python
googlemaps
boto3 (AWS S3)
```

---

## 🎯 Quick Reference

### Start Development
```bash
cd ai-decorator/frontend
npm run dev
```

### Build Production
```bash
npm run build
npm start
```

### Check Linting
```bash
npm run lint
```

### View Pages
- Landing: http://localhost:3000
- Upload: http://localhost:3000/upload
- Chat: http://localhost:3000/chat
- Results: http://localhost:3000/results

---

## 🏆 Current Status

| Component | Status | Progress |
|-----------|--------|----------|
| Frontend | ✅ Complete | 100% |
| Backend | ⏳ Pending | 0% |
| Database | ⏳ Pending | 0% |
| AI Agents | ⏳ Pending | 0% |
| Integration | ⏳ Pending | 0% |
| Testing | ⏳ Pending | 0% |
| Deployment | ⏳ Pending | 0% |

**Overall: 12.5% Complete (1/8 phases)**

---

## 🎉 You Are Here

```
✅ Step 1: Project Setup
✅ Step 2: Frontend Implementation ← YOU ARE HERE
⏳ Step 3: Backend Setup (NEXT)
⏳ Step 4: Database Configuration
⏳ Step 5: AI Agent Implementation
⏳ Step 6: Integration & Testing
⏳ Step 7: Deployment
⏳ Step 8: Polish & Documentation
```

---

**Ready to proceed to Step 3!** 🚀

---

*This map will be updated as the project progresses*

