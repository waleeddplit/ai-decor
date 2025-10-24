# 🎨 Art.com Affiliate Integration Guide

## Overview

Your platform now shows **LOCAL CATALOG artworks** (curated by you) with **REAL Art.com purchase links** (affiliate tracked for monetization)!

### What This Gives You:

✅ **YOUR curated artwork images** (local catalog - best matches)  
✅ **Art.com purchase links** (real products, affiliate commissions)  
✅ **10-15% commission** on every sale  
✅ **No API required** (works with just affiliate ID)  
✅ **Optional CJ/Rakuten API** (for specific products)

---

## 🚀 Quick Start (Works Without API!)

### Option 1: Simple Affiliate Links (No API Needed)

**Step 1: Join Art.com Affiliate Program**

Art.com partners with multiple affiliate networks:

**A) Commission Junction (CJ Affiliate)** - Recommended
1. Go to: https://www.cj.com/
2. Sign up as publisher (FREE)
3. Search for "Art.com" advertiser
4. Apply to their program
5. Get your affiliate ID (e.g., `1234567`)

**B) Rakuten Advertising**
1. Go to: https://rakutenadvertising.com/
2. Sign up as publisher
3. Search for "Art.com"
4. Apply and get tracking ID

**Step 2: Add Affiliate ID to Your Project**

```bash
cd /Users/waleedali/Documents/DPLProjects/ai-decorator/backend
echo 'ARTCOM_AFFILIATE_ID="your_affiliate_id_here"' >> .env
```

**Step 3: Restart Backend**

```bash
# Backend auto-reloads, or restart manually:
pkill -f "python.*main.py"
./venv/bin/python main.py
```

**Step 4: Test It!**

```bash
curl -X POST http://localhost:8000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{"style_vector":[0.1,0.2],"user_style":"Modern","limit":3}' \
  | grep -i "art.com"
```

Look for:
```json
{
  "source": "Art.com",
  "purchase_url": "https://www.art.com/...&aid=YOUR_ID",
  "affiliate": {
    "program": "Art.com Affiliate",
    "commission": "10-15%",
    "tracking_id": "YOUR_ID"
  }
}
```

---

## 💰 How You Make Money

### Commission Structure:

| Product Type | Commission Rate | Example Sale | Your Earnings |
|-------------|-----------------|--------------|---------------|
| Art Prints | 10% | $50 | $5 |
| Canvas Prints | 12% | $120 | $14.40 |
| Framed Art | 15% | $200 | $30 |

### Revenue Calculation:

If you have **1,000 users/month** and:
- 10% click "Buy Now" → 100 clicks
- 5% complete purchase → 5 sales
- Average sale: $100
- Average commission: 12%

**Monthly Revenue: $60** (5 × $100 × 12%)  
**Yearly Revenue: $720**

Scale to 10,000 users → **$7,200/year** passive income!

---

## 🎯 How It Works

### User Experience:

**Before (Without Affiliate):**
```
[Your Artwork Image]
Abstract Blue Waves
$199

[No purchase button]
```

**After (With Art.com Affiliate):**
```
[Your Artwork Image] ← Local catalog (your curated match)
Abstract Blue Waves  ← Your artwork title
$199                ← Your pricing

🛒 Buy Similar on Art.com ← Real purchase link with YOUR affiliate ID!
From Art.com        ← Shows source
```

### Backend Flow:

1. **FAISS** finds best matching artwork from YOUR catalog
2. **Art.com API** searches for similar products
3. **Backend** keeps YOUR image, adds Art.com purchase link
4. **User sees** YOUR curated artwork
5. **User clicks** "Buy on Art.com" (with YOUR affiliate ID)
6. **You earn** commission on completed sales!

---

## 🔧 Advanced: CJ Affiliate API Integration

For **specific product recommendations** instead of search pages:

### Step 1: Get CJ API Access

1. Log into CJ Account: https://members.cj.com/
2. Go to "Account" → "Web Services"
3. Request API access (usually approved instantly)
4. Copy your **Personal Access Token**

### Step 2: Add to Environment

```bash
echo 'CJ_API_KEY="your_cj_api_token"' >> backend/.env
echo 'CJ_WEBSITE_ID="your_website_id"' >> backend/.env
```

### Step 3: Find Art.com Advertiser ID

1. In CJ dashboard, search for "Art.com"
2. Note their **Advertiser ID** (e.g., `4123456`)
3. Update `store_inventory_agent.py` line 562:
   ```python
   "advertiser-ids": "4123456",  # Art.com advertiser ID
   ```

### Benefits:

✅ **Specific product data** (exact titles, prices, images)  
✅ **Real-time inventory** (in-stock status)  
✅ **Deep linking** (direct product pages, not search)  
✅ **Better conversion** (users see exact product)

---

## 📊 Tracking Your Earnings

### CJ Dashboard

1. Log into: https://members.cj.com/
2. Go to "Reports" → "Performance"
3. View:
   - Click-through rate
   - Sales conversions
   - Commission earned
   - Top-performing products

### Your Backend Logs

```
✅ Found 3 Art.com products for 'modern abstract'
✅ Added Art.com purchase link to local artwork: 'Abstract Blue Waves'
```

### Frontend Analytics

Add Google Analytics tracking to "Buy Now" button:

```typescript
<a
  href={rec.purchase_url}
  onClick={() => gtag('event', 'purchase_click', {
    'artwork_id': rec.id,
    'source': rec.source,
    'affiliate_program': 'art.com'
  })}
>
  Buy on Art.com
</a>
```

---

## 🎨 Customization Options

### 1. Use Art.com Images Instead of Local Catalog

In `backend/routes/recommendations.py`, uncomment lines 128-130:

```python
# HYBRID APPROACH: Keep local catalog image, add Art.com purchase link
title = real_item.get('title', title)  # Use Art.com title
artist = real_item.get('artist', artist)  # Use Art.com artist
price = real_item.get('price', price)  # Use Art.com price
```

**Result:** Shows Art.com product data instead of your catalog

### 2. Show Both Options (Recommended!)

Keep YOUR artwork as primary, add Art.com as alternative:

```json
{
  "title": "Abstract Blue Waves",
  "artist": "Ocean Art Collective",
  "price": "$199",
  "image_url": "http://localhost:8000/uploads/artworks/xxx.jpg",
  "purchase_url": null,
  "purchase_options": [
    {
      "source": "Art.com",
      "title": "Similar Abstract Art",
      "price": "From $15.99",
      "url": "https://www.art.com/...&aid=YOUR_ID"
    }
  ]
}
```

Users see:
- **Primary:** Your curated artwork
- **Alternative:** "Or buy similar on Art.com"

### 3. Mix Multiple Affiliates

Combine Art.com + Society6 + Redbubble:

```python
# In store_inventory_agent.py
results = []
results.extend(await self._search_artcom(query, 1))
results.extend(await self._search_society6(query, 1))
results.extend(await self._search_redbubble(query, 1))
```

Users get 3 purchase options per artwork!

---

## 🔍 Testing Your Integration

### Test 1: Check Art.com Priority

```bash
curl -s http://localhost:8000/api/recommend \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"style_vector":[0.1],"user_style":"Modern","limit":3}' \
  | python3 -c "import json, sys; data = json.load(sys.stdin); \
    [print(f\"{r['title'][:40]} -> {r.get('source', 'N/A')}\") for r in data['recommendations']]"
```

Expected output:
```
Abstract Blue Waves -> Art.com
Modern Geometric Canvas -> Art.com
Minimalist Line Art -> Art.com
```

### Test 2: Verify Affiliate Tracking

```bash
curl -s http://localhost:8000/api/recommend \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"style_vector":[0.1],"user_style":"Modern","limit":1}' \
  | python3 -c "import json, sys; data = json.load(sys.stdin); \
    print(data['recommendations'][0].get('purchase_url', 'NO URL'))"
```

Should contain `&aid=YOUR_AFFILIATE_ID` or `?sid=YOUR_ID`

### Test 3: Frontend Display

1. Go to: http://localhost:3000/upload
2. Upload a room image
3. Check results page for:
   - ✅ Your local catalog images
   - ✅ "Buy on Art.com" buttons
   - ✅ "From Art.com" badges
   - ✅ Click opens Art.com with your affiliate ID

---

## 💡 Optimization Tips

### 1. Improve Match Quality

Use better search queries based on artwork metadata:

```python
# In recommendations.py
if tags and "abstract" in tags:
    search_query = f"abstract {style} wall art canvas"
elif tags and "botanical" in tags:
    search_query = f"botanical {style} print framed"
```

### 2. Category-Specific Links

Different Art.com categories for different artwork styles:

```python
style_to_category = {
    "Modern": "contemporary-art",
    "Abstract": "abstract-art",
    "Botanical": "floral-botanical-art",
    "Landscape": "landscape-art"
}
category = style_to_category.get(style, "wall-art")
url = f"https://www.art.com/gallery/{category}/?q={query}&aid={aid}"
```

### 3. Price-Based Routing

Show Art.com for budget-conscious users:

```python
if user_budget < 100:
    # Prioritize Art.com (affordable prints)
elif user_budget < 500:
    # Mix Art.com + Society6
else:
    # Show premium galleries (Artfinder)
```

---

## 🆘 Troubleshooting

### "I don't see Art.com in results"

**Check 1:** Is `ARTCOM_AFFILIATE_ID` set in `.env`?
```bash
cd backend
grep ARTCOM .env
```

**Check 2:** Backend logs show Art.com initialization?
```
✅ StoreInventoryAgent initialized with sources:
   - Art.com (Affiliate ID: xxx)
```

**Check 3:** Search is returning results?
```bash
# Check backend logs for:
✅ Found 3 Art.com products for 'modern abstract'
```

### "Affiliate links don't have my ID"

Update the URL format in `_search_artcom()`:

CJ Affiliate uses: `?aid=YOUR_ID`  
Rakuten uses: `?sid=YOUR_ID`  
ShareASale uses: `?affid=YOUR_ID`

Check your network's documentation for the correct parameter name.

### "CJ API returns 401 Unauthorized"

1. Verify your API key is correct
2. Check you've enabled API access in CJ dashboard
3. Ensure you're approved for Art.com advertiser

---

## 📈 Next Steps

1. ✅ Join Art.com affiliate program (CJ or Rakuten)
2. ✅ Add `ARTCOM_AFFILIATE_ID` to `.env`
3. ✅ Test integration
4. ✅ Monitor earnings in CJ dashboard
5. 🎯 Scale to 10,000+ users
6. 💰 Watch passive income grow!

**Estimated Setup Time:** 10-15 minutes  
**Estimated Monthly Revenue (1,000 users):** $50-100  
**Estimated Monthly Revenue (10,000 users):** $500-1,000

---

## 🎊 What You Have Now

✅ **Hybrid recommendation system**  
   - YOUR curated images (best AI matching)
   - Art.com purchase links (real products)

✅ **Monetization ready**  
   - 10-15% commission per sale
   - Passive income stream
   - No inventory needed

✅ **Professional platform**  
   - AI-powered matching
   - Real purchase options
   - Artist attribution
   - Multiple price points

✅ **Scalable revenue**  
   - More users = more clicks = more sales
   - Automated affiliate tracking
   - CJ handles payments

---

**Ready to earn commissions? Get your Art.com affiliate ID now!** 🎨💰

**Join Here:**
- CJ Affiliate: https://www.cj.com/
- Rakuten: https://rakutenadvertising.com/
- ShareASale: https://www.shareasale.com/

*Takes 10 minutes, lasts forever!*

