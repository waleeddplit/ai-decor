# Art.Decor.AI Frontend

Modern Next.js frontend for the Art.Decor.AI platform - an AI-powered home décor recommendation system.

## 🚀 Tech Stack

- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS 4
- **Icons**: Lucide React
- **Theme**: next-themes (dark/light mode)
- **Font**: Inter (Google Fonts)

## 📁 Project Structure

```
src/
├── app/                    # Next.js App Router pages
│   ├── page.tsx           # Landing page (/)
│   ├── upload/            # Image upload & input page
│   ├── results/           # AI recommendations display
│   ├── chat/              # Chat interface
│   ├── layout.tsx         # Root layout with theme provider
│   └── globals.css        # Global styles
│
└── components/             # Reusable components
    ├── navbar.tsx         # Navigation bar
    ├── theme-provider.tsx # Theme context provider
    └── theme-toggle.tsx   # Dark/light mode toggle
```

## 🎨 Pages

### `/` - Landing Page
- Hero section with value proposition
- Feature highlights (AI analysis, trends, local stores)
- How it works workflow
- Call-to-action sections

### `/upload` - Upload Page
- Drag-and-drop image upload
- File browser integration
- Optional text description input
- Room analysis submission
- Tips for best results

### `/results` - Results Page
- Room analysis summary (style, colors, lighting)
- AI-curated décor recommendations grid
- Match scores and reasoning
- Local store availability
- Favorite/save functionality

### `/chat` - Chat Interface
- Conversational AI interaction
- Message history display
- Text and voice input support
- Real-time responses
- Contextual décor advice

## 🎨 Design System

### Colors
- **Primary**: Purple (#7C3AED) - Brand color for CTAs
- **Secondary**: Pink (#EC4899) - Accent color
- **Neutral**: Gray scale for text and backgrounds

### Typography
- **Font**: Inter (Google Fonts)
- **Headings**: Bold, 2xl-6xl sizes
- **Body**: Regular, sm-base sizes

### Components
- Consistent rounded corners (rounded-lg, rounded-xl)
- Shadow elevation for depth
- Smooth transitions and hover states
- Accessible color contrast ratios

## 🌗 Theme Support

The app includes full dark/light mode support:
- System preference detection
- Manual toggle via navbar
- Persistent theme selection
- Smooth transitions between modes

## 🚀 Getting Started

### Prerequisites
- Node.js 18+ 
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the app.

### Build for Production

```bash
# Create optimized production build
npm run build

# Start production server
npm start
```

## 🔧 Configuration

### Environment Variables

Create a `.env.local` file:

```env
# Backend API endpoint
NEXT_PUBLIC_API_URL=http://localhost:8000

# Optional: Analytics, monitoring, etc.
```

## 📦 Dependencies

### Core
- `next` - React framework
- `react` - UI library
- `react-dom` - React DOM renderer

### UI & Styling
- `tailwindcss` - Utility-first CSS
- `@tailwindcss/postcss` - PostCSS plugin
- `next-themes` - Theme management
- `lucide-react` - Icon library

### Development
- `typescript` - Type safety
- `eslint` - Code linting
- `eslint-config-next` - Next.js ESLint config

## 🔗 API Integration

The frontend communicates with the FastAPI backend via REST endpoints:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/analyze_room` | POST | Upload room image for analysis |
| `/api/recommend` | POST | Get décor recommendations |
| `/api/chat` | POST | Chat with AI assistant |
| `/api/stores` | GET | Find nearby décor stores |

Example API call:

```typescript
const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/analyze_room`, {
  method: 'POST',
  body: formData,
})
```

## 🎯 Features Roadmap

- [x] Landing page with feature showcase
- [x] Image upload with drag-and-drop
- [x] Results page with recommendations
- [x] Chat interface for AI interaction
- [x] Dark/light theme support
- [ ] User authentication (Supabase Auth)
- [ ] User profile and preferences
- [ ] Favorites and saved collections
- [ ] Share recommendations
- [ ] Store locator map integration
- [ ] Voice input (Whisper API)
- [ ] Real-time backend integration

## 🧪 Development Notes

### Mock Data
Currently using placeholder data for demonstration:
- Mock recommendations in `/results`
- Simulated AI responses in `/chat`
- Placeholder images from Unsplash

### Backend Connection
Replace mock API calls with real endpoints once backend is ready:
1. Update `NEXT_PUBLIC_API_URL` in `.env.local`
2. Implement API client in `src/lib/api.ts`
3. Replace mock data with API responses

## 📱 Responsive Design

Fully responsive layouts for:
- Mobile (< 640px)
- Tablet (640px - 1024px)
- Desktop (> 1024px)

## ♿ Accessibility

- Semantic HTML elements
- ARIA labels for interactive elements
- Keyboard navigation support
- Color contrast compliance (WCAG AA)
- Focus states for all interactive elements

## 🚀 Deployment

### Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Environment Variables on Vercel
Add `NEXT_PUBLIC_API_URL` in project settings.

## 📄 License

MIT License - Educational and demonstration purposes

---

**Built with ❤️ using Next.js and TypeScript**
