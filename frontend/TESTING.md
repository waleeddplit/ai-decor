# 🧪 Frontend Testing Guide

Manual testing guide for the Art.Decor.AI frontend application.

---

## 🚀 Before You Start

1. Ensure development server is running:
```bash
npm run dev
```

2. Open browser to: http://localhost:3000

---

## ✅ Test Checklist

### 1. Landing Page (`/`)

#### Layout & Design
- [ ] Hero section displays correctly
- [ ] Brand logo and title visible in navbar
- [ ] "AI-Powered Interior Design" badge shows
- [ ] Gradient text renders properly ("AI-Curated Décor")
- [ ] Three feature cards display in grid
- [ ] "How It Works" section shows 4 steps
- [ ] Footer displays at bottom

#### Interactive Elements
- [ ] "Upload Room Photo" button navigates to `/upload`
- [ ] "Start Chatting" button navigates to `/chat`
- [ ] "Get Started Now" (bottom CTA) navigates to `/upload`
- [ ] All hover effects work smoothly

#### Responsive Design
- [ ] Mobile view: Single column layout
- [ ] Tablet view: Features in 2 columns
- [ ] Desktop view: Features in 3 columns
- [ ] Navbar collapses appropriately

---

### 2. Upload Page (`/upload`)

#### Upload Area
- [ ] Dashed border upload zone visible
- [ ] Upload icon and instructions show
- [ ] "Choose File" button clickable
- [ ] File input accepts images (JPG, PNG, WEBP)

#### Drag & Drop
- [ ] Drag image file over zone
- [ ] Drop file triggers upload
- [ ] Image preview displays after upload
- [ ] Remove button (X) appears on preview

#### Text Input
- [ ] Description textarea accepts input
- [ ] Placeholder text visible
- [ ] Auto-resize works (test with multiline text)

#### Form Submission
- [ ] Submit button disabled when no input
- [ ] Submit button enabled with image OR text
- [ ] Loading spinner shows during "analysis"
- [ ] Redirects to `/results` after 2 seconds

#### Tips Section
- [ ] Tips card visible at bottom
- [ ] All 4 tips display correctly

---

### 3. Results Page (`/results`)

#### Room Analysis Summary
- [ ] Analysis card displays at top
- [ ] "Modern Minimalist" style shows
- [ ] 4 color circles render correctly
- [ ] "Natural, Bright" lighting displays

#### Recommendations Grid
- [ ] 3 recommendation cards display
- [ ] Images load from Unsplash
- [ ] Match score badges show (95%, 92%, 88%)
- [ ] Favorite (heart) buttons work
- [ ] Heart fills red when clicked
- [ ] Tags display below each item

#### AI Reasoning
- [ ] "Why this matches" button toggleable
- [ ] Chevron icon changes (up/down)
- [ ] Reasoning text expands/collapses
- [ ] Works independently for each card

#### Store Information
- [ ] "Available at X stores" shows
- [ ] "View Stores" button displays
- [ ] Store count accurate

#### Action Buttons
- [ ] "Try Another Room" navigates to `/upload`
- [ ] "Refine with Chat" navigates to `/chat`

---

### 4. Chat Page (`/chat`)

#### Initial State
- [ ] Header displays "Chat with AI Designer"
- [ ] Welcome message from assistant visible
- [ ] Bot avatar (purple circle) shows
- [ ] Input textarea at bottom
- [ ] Send button (paper plane icon) visible

#### Sending Messages
- [ ] Type message in input
- [ ] Press Enter to send (without Shift)
- [ ] Message appears with user avatar
- [ ] User message has purple background
- [ ] Timestamp displays correctly

#### Receiving Responses
- [ ] "Thinking..." indicator appears
- [ ] Bot avatar shows for assistant messages
- [ ] Response appears after ~1.5 seconds
- [ ] Assistant message has gray background
- [ ] Timestamp displays

#### Message Behavior
- [ ] Auto-scroll to latest message
- [ ] Messages stack in correct order
- [ ] Older messages remain visible
- [ ] Scroll works properly

#### Voice Input (UI Only)
- [ ] Microphone button visible in input
- [ ] Click mic turns it red (listening state)
- [ ] Icon changes to MicOff
- [ ] Click again stops listening
- [ ] Note: Actual voice input not yet implemented

#### Keyboard Shortcuts
- [ ] Enter sends message
- [ ] Shift+Enter creates new line
- [ ] Send button disabled when input empty

---

### 5. Navigation (`Navbar`)

#### Links
- [ ] "Home" navigates to `/`
- [ ] "Upload" navigates to `/upload`
- [ ] "Chat" navigates to `/chat`
- [ ] Logo/title navigates to `/`

#### Active States
- [ ] Current page link highlighted
- [ ] Purple background on active link
- [ ] Other links have gray text

#### Theme Toggle
- [ ] Sun icon shows in dark mode
- [ ] Moon icon shows in light mode
- [ ] Click toggles theme smoothly
- [ ] Theme persists on page refresh

---

### 6. Theme System (Dark/Light Mode)

#### Light Mode
- [ ] White background
- [ ] Dark gray text
- [ ] Purple accents maintained
- [ ] Cards have subtle shadows
- [ ] Borders visible

#### Dark Mode
- [ ] Near-black background (#0a0a0a)
- [ ] Light gray text
- [ ] Purple accents adjusted for contrast
- [ ] Cards have dark borders
- [ ] Reduced shadow intensity

#### Transitions
- [ ] Smooth color transitions
- [ ] No flash/flicker
- [ ] All elements transition together
- [ ] Theme persists across pages

#### System Preference
- [ ] Detects OS dark/light mode
- [ ] Applies on first visit
- [ ] Manual override works

---

## 🐛 Common Issues to Check

### Performance
- [ ] Pages load within 2 seconds
- [ ] No layout shift during load
- [ ] Images load progressively
- [ ] Smooth scrolling throughout

### Cross-Browser Testing
- [ ] Chrome/Edge (Chromium)
- [ ] Safari (WebKit)
- [ ] Firefox

### Responsive Breakpoints
- [ ] Mobile: 375px, 414px
- [ ] Tablet: 768px, 1024px
- [ ] Desktop: 1280px, 1440px, 1920px

### Accessibility
- [ ] Tab navigation works
- [ ] Focus indicators visible
- [ ] ARIA labels present
- [ ] Color contrast sufficient
- [ ] Interactive elements keyboard-accessible

---

## 📊 Expected Behaviors

### Mock Data (Current State)

| Feature | Behavior |
|---------|----------|
| Room Analysis | 2-second simulated delay |
| Recommendations | Static array of 3 items |
| Chat Responses | Rule-based mock replies |
| Store Locations | Placeholder names |
| Image Analysis | No actual processing |

### Coming Soon (Backend Integration)

| Feature | Future Behavior |
|---------|-----------------|
| Room Analysis | YOLOv8 + CLIP processing |
| Recommendations | FAISS vector search results |
| Chat Responses | LLaVA/Llama AI responses |
| Store Locations | Google Maps API data |
| Image Analysis | Real computer vision |

---

## 🎯 Test Scenarios

### Scenario 1: First-Time User
1. Land on homepage
2. Read features
3. Click "Upload Room Photo"
4. Upload an image
5. View results
6. Try "Refine with Chat"
7. Have conversation
8. Toggle theme

### Scenario 2: Quick Upload
1. Go directly to `/upload`
2. Drag-drop image
3. Add description
4. Submit
5. Review recommendations
6. Favorite items
7. Check store availability

### Scenario 3: Chat-First
1. Navigate to `/chat`
2. Ask about décor styles
3. Request color advice
4. Get room size tips
5. Switch between pages
6. Return to chat (history preserved)

---

## ✅ Sign-Off Checklist

Before marking as complete:

- [ ] All pages load without errors
- [ ] No console errors in browser DevTools
- [ ] No TypeScript compilation errors
- [ ] Navigation works between all pages
- [ ] Theme toggle functional
- [ ] All interactive elements respond
- [ ] Mobile responsive design verified
- [ ] Production build succeeds (`npm run build`)

---

## 🚨 Known Limitations (Current MVP)

1. **No Backend Connection** - All responses are mocked
2. **No User Authentication** - No login/signup
3. **No Persistence** - Data doesn't save between sessions
4. **No Real AI** - Computer vision not integrated
5. **Voice Input** - UI only, no actual speech recognition
6. **Store Locator** - No map or real locations

These will be addressed in subsequent development phases.

---

## 📝 Bug Report Template

If you find issues, document them:

```
**Page**: /upload
**Issue**: Image preview not showing
**Steps to Reproduce**:
1. Navigate to /upload
2. Click "Choose File"
3. Select a PNG image
4. No preview appears

**Expected**: Image should display in preview area
**Actual**: Upload area remains unchanged
**Browser**: Chrome 120
**Device**: Desktop (Mac)
```

---

## 🎉 Testing Complete!

If all tests pass, the frontend is ready for:
- ✅ Backend integration
- ✅ User testing
- ✅ Production deployment preparation

---

**Happy Testing!** 🧪🚀

