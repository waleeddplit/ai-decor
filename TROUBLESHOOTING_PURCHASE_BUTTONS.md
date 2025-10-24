# 🔧 Troubleshooting: Purchase Buttons Not Showing

## Problem
The purchase buttons ("Buy Now") are not visible on the frontend results page, even though the backend is returning the `purchase_url` data.

---

## Root Cause
The frontend needs to be **restarted** to:
1. Recompile the TypeScript changes
2. Load the new React components
3. Pick up the updated API interface

---

## ✅ Solution (3 Steps)

### Step 1: Restart Frontend

```bash
# Stop the frontend (Ctrl+C if running)
# Then restart:
cd frontend
npm run dev
```

### Step 2: Clear Browser Cache

**Option A (Recommended):**
- Open DevTools: Press `F12` or `Cmd+Option+I` (Mac)
- Right-click the refresh button
- Select **"Empty Cache and Hard Reload"**

**Option B:**
- Press `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows/Linux)

### Step 3: Test Again

1. Go to: http://localhost:3000/upload
2. Upload a room image
3. Wait for analysis
4. Check results page for "Buy Now" buttons

---

## 🐛 Debugging Checklist

### Check 1: Backend is Returning Data

Test the API directly:

```bash
curl -X POST http://localhost:8000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "style_vector":[0.1,0.2,0.3,0.4,0.5],
    "user_style":"Modern",
    "color_preferences":["#E8E8E8"],
    "limit":1
  }' | python3 -m json.tool | grep "purchase_url"
```

**Expected:** You should see:
```json
"purchase_url": "https://society6.com/...",
```

✅ **If you see this:** Backend is working correctly!  
❌ **If you don't:** Backend needs to be restarted

---

### Check 2: Frontend is Receiving Data

1. Open browser DevTools (F12)
2. Go to **Console** tab
3. Upload an image and go to results
4. Look for debug logs:

**Expected logs:**
```
First recommendation: {id: "...", title: "...", purchase_url: "https://..."}
Has purchase_url? true
```

✅ **If you see these:** Frontend is getting the data!  
❌ **If you don't:** Check Network tab for API call issues

---

### Check 3: Button Component is Rendering

1. In DevTools, go to **Elements** tab
2. Find a recommendation card
3. Search for `purchase_url` or `Buy Now`

**Expected:** You should find:
```html
<a href="https://..." class="...">
  <svg>...</svg>
  Buy Now - $89.99
</a>
```

✅ **If you see this:** Button is rendering!  
❌ **If you don't:** Check if `rec.purchase_url` exists in console

---

## 🎯 What You Should See After Fix

### Before (Old):
```
┌─────────────────────────┐
│  [Artwork Image]        │
│  Abstract Art           │
│  $249                   │
│  [View Stores]          │ ← Generic button
└─────────────────────────┘
```

### After (New):
```
┌──────────────────────────────────┐
│  [Artwork Image]                 │
│  Shop Wall Posters               │
│  by Society6 Artists             │
│  View Price                      │
│                                  │
│  ┌────────────────────────────┐ │
│  │  🛒 Buy Now - View Price   │ │ ← Gradient button!
│  └────────────────────────────┘ │
│  From Tavily Search              │ ← Source badge
│                                  │
│  Print on Demand:                │
│  Printful | Printify | Redbubble│ ← POD links
└──────────────────────────────────┘
```

---

## 🔍 Common Issues & Fixes

### Issue 1: "Cannot find module..." error

**Cause:** TypeScript cache issues  
**Fix:**
```bash
cd frontend
rm -rf .next
npm run dev
```

---

### Issue 2: Button shows but link is broken

**Cause:** Backend returning invalid URL  
**Fix:** Check backend logs for errors in StoreInventoryAgent

---

### Issue 3: Price shows as "$undefined"

**Cause:** Price field not in response  
**Fix:** Check API response includes `price` field

---

### Issue 4: TypeScript errors in console

**Cause:** Type mismatch between API and interface  
**Fix:** Verify `frontend/src/lib/api.ts` has updated types:

```typescript
export interface ArtworkRecommendation {
  // ... other fields ...
  purchase_url?: string;
  download_url?: string;
  source?: string;
  // ... etc
}
```

---

## 📝 Quick Verification

Run this complete test:

```bash
# 1. Test backend
curl -s http://localhost:8000/api/recommend \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"style_vector":[0.1,0.2,0.3,0.4,0.5],"user_style":"Modern","limit":1}' \
  | python3 -c "import sys, json; data = json.load(sys.stdin); print('✅ Has purchase_url:', 'purchase_url' in data['recommendations'][0])"

# 2. Check frontend is running
curl -s http://localhost:3000 -I | head -1

# 3. Restart frontend
cd frontend && npm run dev
```

---

## ✨ Success Indicators

You'll know it's working when you see:

✅ Backend logs: `✅ StoreInventoryAgent initialized with FREE sources: Tavily Search`  
✅ Backend logs: `🔍 Searching real stores for Modern artwork...`  
✅ Backend logs: `✅ Found 3 real artworks!`  
✅ Browser console: `First recommendation: {...purchase_url: "https://..."}`  
✅ Browser console: `Has purchase_url? true`  
✅ Results page: Gradient "Buy Now" buttons visible  
✅ Results page: Source badges showing (e.g., "From Tavily Search")  

---

## 🆘 Still Not Working?

### Last Resort Steps:

1. **Hard reset everything:**
```bash
# Kill all processes
pkill -f "npm"
pkill -f "python.*main.py"

# Clear caches
cd frontend
rm -rf .next node_modules/.cache

# Restart backend
cd ../backend
./venv/bin/python main.py &

# Restart frontend
cd ../frontend
npm run dev
```

2. **Check file changes were saved:**
```bash
# Verify purchase button code exists
grep -n "Buy Now" frontend/src/app/results/page.tsx

# Should show line with: Buy Now - {rec.price}
```

3. **Check browser:**
- Open incognito window
- Try a different browser
- Disable browser extensions

---

## 📞 Need More Help?

**Check these logs:**

1. Backend terminal output (should show StoreInventoryAgent messages)
2. Frontend terminal output (should show no TypeScript errors)
3. Browser DevTools Console (should show recommendation objects)
4. Browser DevTools Network tab (check /api/recommend response)

**Files to verify:**
- `frontend/src/app/results/page.tsx` (has purchase button component)
- `frontend/src/lib/api.ts` (has updated interface)
- `backend/routes/recommendations.py` (returns purchase_url)
- `backend/agents/store_inventory_agent.py` (searches for products)

---

**Status:** Integration is complete, just needs frontend restart!  
**Next Step:** Restart frontend → Clear cache → Test

