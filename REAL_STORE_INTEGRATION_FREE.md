# 🛍️ Real Store Integration - FREE APIs Guide

## Overview

Your Art.Decor.AI now includes **StoreInventoryAgent** that fetches **real purchasable artwork** from online marketplaces using **100% FREE APIs** and curated links.

---

## 🎯 Available FREE Sources

| Source | Type | Cost | Rate Limit | Quality |
|--------|------|------|------------|---------|
| **Tavily API** | Product Search | FREE (Already configured!) | Per your plan | ⭐⭐⭐⭐⭐ |
| **Unsplash** | Free Images + Print-on-Demand | FREE | Unlimited with key | ⭐⭐⭐⭐⭐ |
| **Pexels** | Free Stock Photos | FREE | 200 requests/hour | ⭐⭐⭐⭐ |
| **Pixabay** | Free Images | FREE | 100 requests/min | ⭐⭐⭐⭐ |
| **Google Custom Search** | Shopping Results | FREE tier: 100/day | 100 queries/day | ⭐⭐⭐⭐ |
| **Curated Links** | Real Stores | FREE | Unlimited | ⭐⭐⭐⭐ |

---

## 🔧 Setup Instructions

### 1. Tavily API (Already Configured! ✅)

**Status**: You already have this for trend intelligence  
**Cost**: FREE  
**What it does**: Searches the web for real artwork products with prices and purchase links

```bash
# Already in your .env:
TAVILY_API_KEY="tvly-xxx..."
```

**No additional setup needed!** Your TrendIntelAgent already uses Tavily.

---

### 2. Unsplash API (Recommended)

**Cost**: FREE  
**Rate Limit**: Unlimited with access key  
**What you get**: High-quality artwork images + Print-on-demand suggestions

#### Setup:
1. Go to: https://unsplash.com/developers
2. Create a free account
3. Create a new application
4. Copy your **Access Key**

#### Add to `.env`:
```bash
UNSPLASH_ACCESS_KEY="your_unsplash_access_key_here"
```

#### Example API Response:
```json
{
  "id": "unsplash_abc123",
  "title": "Abstract Geometric Art",
  "price": "FREE Download + Print from $25",
  "image_url": "https://images.unsplash.com/...",
  "purchase_url": "https://unsplash.com/photos/...",
  "download_url": "https://unsplash.com/photos/.../download",
  "print_on_demand": [
    {
      "service": "Printful",
      "url": "https://www.printful.com/",
      "price_range": "$25-$150",
      "products": ["Canvas", "Framed Poster", "Metal Print"]
    }
  ],
  "source": "Unsplash"
}
```

---

### 3. Pexels API

**Cost**: FREE  
**Rate Limit**: 200 requests/hour  
**What you get**: Free stock photos with commercial use

#### Setup:
1. Go to: https://www.pexels.com/api/
2. Sign up for free API key
3. Copy your **API Key**

#### Add to `.env`:
```bash
PEXELS_API_KEY="your_pexels_api_key_here"
```

---

### 4. Pixabay API

**Cost**: FREE  
**Rate Limit**: 100 requests/minute  
**What you get**: Free images, no attribution required

#### Setup:
1. Go to: https://pixabay.com/api/docs/
2. Create free account
3. Get your **API Key**

#### Add to `.env`:
```bash
PIXABAY_API_KEY="your_pixabay_api_key_here"
```

---

### 5. Google Custom Search API (Optional)

**Cost**: FREE (100 queries/day)  
**What you get**: Google Shopping results for real products

#### Setup:
1. Go to: https://developers.google.com/custom-search/v1/overview
2. Create a project in Google Cloud Console
3. Enable Custom Search API
4. Create API credentials (API Key)
5. Create a Custom Search Engine at: https://programmablesearchengine.google.com/
   - Configure it to search shopping sites or the entire web
   - Copy your **Search Engine ID**

#### Add to `.env`:
```bash
GOOGLE_API_KEY="your_google_api_key_here"
GOOGLE_SEARCH_ENGINE_ID="your_search_engine_id_here"
```

---

## 📦 What's Already Included (No API Keys Needed!)

### Curated Real Store Links

If no APIs are configured, the system automatically provides **curated links to real stores**:

1. **Society6** - Independent artist marketplace
2. **Redbubble** - Print-on-demand platform  
3. **Artfinder** - Original artwork marketplace
4. **Minted** - Designer art prints
5. **iCanvas** - Canvas art specialists

**These links work without ANY API keys!**

---

## 🚀 Quick Start (Easiest Option)

### Option 1: Use Tavily Only (Already Working!)

```bash
# You already have this configured
TAVILY_API_KEY="tvly-xxx..."
```

**That's it!** Your app will:
- Search for real artwork products
- Extract prices from search results
- Provide direct purchase links

### Option 2: Add Unsplash (5 minutes setup)

```bash
# Add just one more line to .env:
UNSPLASH_ACCESS_KEY="your_key_here"
```

**Benefits:**
- High-quality artwork images
- Print-on-demand suggestions (Printful, Printify, Redbubble)
- FREE unlimited requests

### Option 3: Use Curated Links (0 minutes setup)

**No API keys needed!** The system provides:
- Real purchase links to Society6, Redbubble, etc.
- Search URLs customized to user's query
- Works offline/no API limits

---

## 💻 How to Use in Your Backend

### Search for Artwork

```python
from agents.store_inventory_agent import get_store_inventory_agent

# Initialize agent
store_agent = get_store_inventory_agent()

# Search for artwork
results = await store_agent.search_artwork(
    query="abstract art",
    style="Modern",
    color="blue",
    min_price=20.0,
    max_price=200.0,
    limit=10
)

# Results contain:
for artwork in results:
    print(f"Title: {artwork['title']}")
    print(f"Price: {artwork['price']}")
    print(f"Purchase URL: {artwork['purchase_url']}")
    print(f"Source: {artwork['source']}")
```

### Integration Priority

The agent searches sources in this order:

1. **Tavily** (if `TAVILY_API_KEY` set) - Real products
2. **Google Shopping** (if `GOOGLE_API_KEY` set) - Shopping results
3. **Unsplash** (if `UNSPLASH_ACCESS_KEY` set) - High-quality images
4. **Pixabay** (if `PIXABAY_API_KEY` set) - Free images
5. **Pexels** (if `PEXELS_API_KEY` set) - Stock photos
6. **Curated Links** (always available) - Real store links

---

## 🎨 API Comparison

### For Real Purchasable Products:

**Best Option: Tavily + Curated Links**
- ✅ Already configured
- ✅ Finds real products with prices
- ✅ Direct purchase links
- ✅ No additional setup

### For High-Quality Images + Print Options:

**Best Option: Unsplash**
- ✅ FREE unlimited requests
- ✅ Professional photography
- ✅ Print-on-demand integration
- ✅ 5-minute setup

### For Free Stock Images:

**Best Options: Pixabay or Pexels**
- ✅ No attribution required (Pixabay)
- ✅ Commercial use allowed
- ✅ Good rate limits
- ✅ Easy setup

---

## 📊 Example API Responses

### Tavily Product Search

```json
{
  "id": "tavily_1",
  "title": "Modern Abstract Canvas Wall Art - 24x36",
  "artist": "Society6",
  "price": "$89.99",
  "purchase_url": "https://society6.com/product/...",
  "description": "Contemporary abstract artwork...",
  "source": "Tavily Search",
  "in_stock": true
}
```

### Unsplash with Print-on-Demand

```json
{
  "id": "unsplash_xyz789",
  "title": "Minimalist Line Art",
  "artist": "John Doe",
  "price": "FREE Download + Print from $25",
  "download_url": "https://unsplash.com/.../download",
  "purchase_url": "https://unsplash.com/photos/...",
  "print_on_demand": [
    {
      "service": "Printful",
      "url": "https://www.printful.com/",
      "price_range": "$25-$150",
      "products": ["Canvas", "Framed Poster", "Metal Print"]
    }
  ],
  "source": "Unsplash"
}
```

### Curated Store Link

```json
{
  "id": "mock_society6_001",
  "title": "Abstract Art Canvas Print",
  "artist": "Society6 Artists",
  "price": "$89.99",
  "purchase_url": "https://society6.com/s?q=abstract+art+wall+art",
  "description": "Beautiful abstract artwork from Society6",
  "source": "Society6 (Curated)",
  "store_info": {
    "name": "Society6",
    "url": "https://society6.com",
    "description": "Marketplace for independent artists"
  }
}
```

---

## 🔌 Integration with Recommendations

To integrate with your existing recommendation system:

### Update `recommendations.py`:

```python
from agents.store_inventory_agent import get_store_inventory_agent

store_agent = get_store_inventory_agent()

@router.post("/recommend")
async def get_recommendations(request: RecommendationRequest):
    # ... existing FAISS search ...
    
    for recommendation in recommendations:
        # Search for real purchasable versions
        store_results = await store_agent.search_artwork(
            query=recommendation["title"],
            style=recommendation["style"],
            limit=3
        )
        
        # Add purchase options to recommendation
        recommendation["purchase_options"] = store_results
    
    return recommendations
```

---

## 💡 Monetization Options

### 1. Affiliate Links

Add affiliate IDs to store links:

```python
# Society6 Affiliate
f"https://society6.com/s?q={query}&aff={your_affiliate_id}"

# Redbubble Affiliate Program
f"https://www.redbubble.com/shop/?query={query}&aff={your_id}"
```

### 2. Print-on-Demand Integration

Partner with:
- **Printful API** (FREE) - Full e-commerce integration
- **Printify API** (FREE) - Product catalog and ordering
- Create your own print store with user's room-matched designs

### 3. Commission-Based Partnerships

Partner with:
- Artfinder
- Saatchi Art
- Minted

They offer affiliate/partner programs for art sales.

---

## 🎯 Recommended Setup for Production

### Minimum (Already Working!):
```bash
TAVILY_API_KEY="your_key_here"  # ✅ Already have this
```

### Recommended (Best Quality):
```bash
TAVILY_API_KEY="your_key_here"       # ✅ Already have this
UNSPLASH_ACCESS_KEY="your_key_here"  # Add this (5 min setup)
```

### Maximum (All Options):
```bash
TAVILY_API_KEY="your_key_here"           # Product search
UNSPLASH_ACCESS_KEY="your_key_here"      # High-quality images
PEXELS_API_KEY="your_key_here"           # Stock photos
PIXABAY_API_KEY="your_key_here"          # Free images
GOOGLE_API_KEY="your_key_here"           # Google Shopping (optional)
GOOGLE_SEARCH_ENGINE_ID="your_cse_id"    # Google Shopping (optional)
```

---

## 📈 Rate Limits & Costs Summary

| API | Cost | Rate Limit | Recommended For |
|-----|------|------------|-----------------|
| Tavily | FREE | Per plan | ⭐ Real products |
| Unsplash | FREE | Unlimited | ⭐ High-quality art |
| Pexels | FREE | 200/hour | Stock photos |
| Pixabay | FREE | 100/min | Free downloads |
| Google | FREE | 100/day | Shopping search |
| Curated | FREE | Unlimited | Always works |

---

## 🔥 Quick Test

### Test Tavily Integration (Already Working):

```python
cd backend
./venv/bin/python << 'EOF'
import asyncio
from agents.store_inventory_agent import get_store_inventory_agent

async def test():
    agent = get_store_inventory_agent()
    results = await agent.search_artwork("modern abstract art", limit=3)
    
    for r in results:
        print(f"✅ {r['title']}")
        print(f"   Price: {r['price']}")
        print(f"   Source: {r['source']}")
        print(f"   URL: {r['purchase_url']}\n")
    
    await agent.close()

asyncio.run(test())
EOF
```

---

## 📝 Next Steps

1. **Test with Tavily** (already configured!) ✅
2. **Add Unsplash** for high-quality images (5 min) 
3. **Test the integration** with your recommendations
4. **Optional**: Add more sources (Pexels, Pixabay, Google)
5. **Optional**: Set up affiliate links for monetization

---

## 🎉 Summary

You now have:

✅ **FREE** real store integration  
✅ **Multiple** API sources  
✅ **Curated** fallback links that always work  
✅ **Print-on-demand** suggestions  
✅ **Monetization** ready (affiliate links)  
✅ **No paid APIs** required (Etsy removed!)  

**Minimum setup time**: 0 minutes (use Tavily + Curated links)  
**Recommended setup time**: 5 minutes (add Unsplash)  
**Maximum setup time**: 15 minutes (all APIs)  

**All APIs are 100% FREE!** 🎊

---

## 📚 Resources

- Tavily Docs: https://docs.tavily.com/
- Unsplash API: https://unsplash.com/developers
- Pexels API: https://www.pexels.com/api/documentation/
- Pixabay API: https://pixabay.com/api/docs/
- Google Custom Search: https://developers.google.com/custom-search/v1/overview

---

**File**: `backend/agents/store_inventory_agent.py`  
**Status**: ✅ Ready to use  
**APIs**: 100% FREE  
**Setup Required**: Optional (works without any)

