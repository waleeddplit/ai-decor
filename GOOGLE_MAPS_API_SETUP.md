# 🗺️ Google Maps API Setup Guide (Step-by-Step)

## Overview

This guide will help you get a **FREE** Google Maps API key for the Geo-Finder Agent in 5-10 minutes.

### What You'll Get:
✅ **$200 FREE credits per month** (enough for ~40,000 requests)  
✅ **Places API** - Find nearby art galleries and stores  
✅ **Geocoding API** - Convert addresses to coordinates  
✅ **Directions API** - Get turn-by-turn directions  
✅ **No credit card required** for getting started (though recommended for production)

---

## 📋 Prerequisites

- Google Account (Gmail)
- Web browser
- 10 minutes of time

---

## 🚀 Step-by-Step Instructions

### Step 1: Go to Google Cloud Console

**Open this URL in your browser:**
```
https://console.cloud.google.com/
```

- Sign in with your Google account
- Accept the Terms of Service if prompted

---

### Step 2: Create a New Project

1. **Click** the project dropdown at the top (says "Select a project")
   
   ![Project Dropdown Location](top of page, next to "Google Cloud")

2. **Click** "NEW PROJECT" button (top right of the modal)

3. **Fill in project details:**
   - **Project name:** `Art-Decor-AI` (or any name you prefer)
   - **Organization:** Leave as default (usually "No organization")
   - **Location:** Leave as default

4. **Click** "CREATE"

5. **Wait** 10-20 seconds for project creation

6. **Select** your new project from the dropdown

---

### Step 3: Enable Required APIs

You need to enable 3 APIs for full functionality:

#### 3a. Enable Places API

1. **Go to:** https://console.cloud.google.com/apis/library/places-backend.googleapis.com

   OR

   - Click "☰" menu (top left)
   - Go to "APIs & Services" → "Library"
   - Search for "Places API"

2. **Click** on "Places API" card

3. **Click** blue "ENABLE" button

4. **Wait** for confirmation (5-10 seconds)

#### 3b. Enable Geocoding API

1. **Go to:** https://console.cloud.google.com/apis/library/geocoding-backend.googleapis.com

   OR

   - In the API Library, search for "Geocoding API"

2. **Click** on "Geocoding API" card

3. **Click** "ENABLE" button

4. **Wait** for confirmation

#### 3c. Enable Directions API

1. **Go to:** https://console.cloud.google.com/apis/library/directions-backend.googleapis.com

   OR

   - In the API Library, search for "Directions API"

2. **Click** on "Directions API" card

3. **Click** "ENABLE" button

4. **Wait** for confirmation

---

### Step 4: Create API Key

1. **Go to:** https://console.cloud.google.com/apis/credentials

   OR

   - Click "☰" menu (top left)
   - Go to "APIs & Services" → "Credentials"

2. **Click** "CREATE CREDENTIALS" (top of page)

3. **Select** "API key" from dropdown

4. **Wait** for key generation (5 seconds)

5. **A modal appears with your API key** - it looks like:
   ```
   AIzaSyB-xxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

6. **COPY** the API key to a safe place

7. **Click** "CLOSE" (we'll restrict it in the next step)

---

### Step 5: Restrict API Key (Recommended for Security)

1. **Click** on the key name you just created (in the credentials list)

2. **Scroll down** to "API restrictions"

3. **Select** "Restrict key"

4. **Check** these APIs:
   - ☑ Places API
   - ☑ Geocoding API
   - ☑ Directions API

5. **Scroll down** to "Application restrictions" (optional but recommended)

   **For development (localhost):**
   - Select "HTTP referrers (web sites)"
   - Click "ADD AN ITEM"
   - Enter: `http://localhost:*`
   - Enter: `http://127.0.0.1:*`

   **For production (later):**
   - Add your actual domain: `https://your-domain.com/*`

6. **Click** "SAVE" at the bottom

---

### Step 6: Add API Key to Your Project

1. **Open terminal** and navigate to your project:

```bash
cd /Users/waleedali/Documents/DPLProjects/ai-decorator/backend
```

2. **Add the API key** to your `.env` file:

```bash
echo 'GOOGLE_MAPS_API_KEY="AIzaSyB-xxxxxxxxxxxxxxxxxxxxxxxxxxx"' >> .env
```

**Or manually edit** `backend/.env` and add this line:
```
GOOGLE_MAPS_API_KEY="AIzaSyB-xxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

Replace `AIzaSyB-xxxxxxxxxxxxxxxxxxxxxxxxxxx` with your actual API key!

3. **Restart your backend:**

```bash
# Kill the running backend
pkill -f "python.*main.py"

# Start it again
./venv/bin/python main.py
```

4. **Check backend logs** - you should see:

```
GeoFinderAgent initialized with Google Maps API ✅
```

Instead of:
```
Warning: GOOGLE_MAPS_API_KEY not set. Using mock data.
```

---

### Step 7: Test Your API Key

```bash
# Test nearby stores (should return REAL stores now!)
curl -X POST "http://localhost:8000/api/nearby-stores?latitude=40.7128&longitude=-74.0060&radius=5000" \
  -H "Content-Type: application/json" | python3 -m json.tool
```

**Expected result:** Real art galleries in New York City (not mock data)

Example:
```json
{
  "stores": [
    {
      "id": "ChIJKxDbe_lYwokRVf__s8UBsFg",
      "name": "MoMA Design Store",
      "address": "11 W 53rd St, New York",
      "rating": 4.6,
      "distance": 7.2,
      "phone": "(212) 767-1050",
      "website": "https://store.moma.org",
      "is_open": true
    }
  ]
}
```

---

## 💰 Pricing & Free Tier

### Free Tier (Monthly):
- **$200 in free credits** every month
- **No credit card required** to get started
- **No automatic charges** after free tier ends (billing must be enabled manually)

### What $200 Gets You:

| API | Cost per Request | Free Tier Requests |
|-----|------------------|-------------------|
| Places Nearby | $0.032 | 6,250 |
| Place Details | $0.017 | 11,764 |
| Geocoding | $0.005 | 40,000 |
| Directions | $0.005 | 40,000 |

### Example Usage Calculations:

**For 1,000 users/month:**
- Assume 50% provide location = 500 requests
- Places Nearby: 500 × $0.032 = $16
- Place Details: 500 × $0.017 = $8.50
- **Total: $24.50/month** ✅ FREE (within $200 credit)

**For 10,000 users/month:**
- 5,000 location requests
- **Total: ~$245/month** 
- **Cost: $45/month** (after $200 credit)

**For 100,000 users/month:**
- 50,000 location requests
- **Total: ~$2,450/month**
- **Cost: $2,250/month** (after $200 credit)

### Recommendation:
Start without credit card. Add billing only when you exceed free tier (Google will notify you).

---

## 🔒 Security Best Practices

### 1. Restrict Your API Key

✅ **DO:**
- Restrict to specific APIs (Places, Geocoding, Directions only)
- Add HTTP referrer restrictions for web apps
- Use separate keys for development and production
- Rotate keys every 90 days

❌ **DON'T:**
- Commit API keys to GitHub (use `.env` files)
- Use unrestricted keys
- Share keys publicly
- Use the same key for multiple projects

### 2. Monitor Usage

**Set up budget alerts:**

1. Go to: https://console.cloud.google.com/billing/
2. Click "Budgets & alerts"
3. Click "CREATE BUDGET"
4. Set alert at: $10, $50, $100, $150
5. Add your email for notifications

This way you'll know if usage spikes unexpectedly!

### 3. Keep `.env` File Safe

Add to `.gitignore`:
```
backend/.env
*.env
```

Never commit `.env` to Git!

---

## 🧪 Verification Checklist

After setup, verify everything works:

### ✅ Checklist:

- [ ] API key created in Google Cloud Console
- [ ] 3 APIs enabled (Places, Geocoding, Directions)
- [ ] API key restrictions applied
- [ ] API key added to `backend/.env`
- [ ] Backend restarted
- [ ] Backend logs show "GeoFinderAgent initialized with Google Maps API"
- [ ] Test endpoint returns real stores (not mock)
- [ ] Budget alerts configured (optional but recommended)

---

## ❗ Troubleshooting

### Issue 1: "This API project is not authorized to use this API"

**Solution:**
- Make sure you enabled all 3 APIs (Places, Geocoding, Directions)
- Wait 1-2 minutes for API enablement to propagate
- Try again

### Issue 2: "API key not valid"

**Solution:**
- Check API key is copied correctly (no extra spaces)
- Verify API restrictions include your APIs
- Check HTTP referrer restrictions allow localhost
- Try creating a new unrestricted key for testing

### Issue 3: "You have exceeded your request quota"

**Solution:**
- You've used your free $200 credit
- Add billing to continue (or wait until next month)
- Check usage at: https://console.cloud.google.com/apis/dashboard

### Issue 4: Backend still shows "Using mock data"

**Solution:**
```bash
# 1. Check .env file has the key
cat backend/.env | grep GOOGLE_MAPS_API_KEY

# 2. Make sure no spaces around =
# Correct:   GOOGLE_MAPS_API_KEY="AIzaSyB..."
# Wrong:     GOOGLE_MAPS_API_KEY = "AIzaSyB..."

# 3. Restart backend properly
pkill -f "python.*main.py"
cd backend
./venv/bin/python main.py
```

### Issue 5: "REQUEST_DENIED" in API response

**Solution:**
- Check API restrictions - make sure Places API is allowed
- Verify billing is enabled (required for some API features)
- Wait a few minutes for settings to propagate

---

## 🎓 Additional Resources

### Official Documentation:
- **Google Maps Platform:** https://developers.google.com/maps
- **Places API:** https://developers.google.com/maps/documentation/places/web-service
- **Pricing:** https://developers.google.com/maps/billing/gmp-billing

### Your Project URLs:
- **Cloud Console:** https://console.cloud.google.com/
- **API Dashboard:** https://console.cloud.google.com/apis/dashboard
- **Credentials:** https://console.cloud.google.com/apis/credentials
- **Billing:** https://console.cloud.google.com/billing/

---

## 🎯 Quick Reference

### URLs to Bookmark:

```
Google Cloud Console:
https://console.cloud.google.com/

Enable APIs:
https://console.cloud.google.com/apis/library

Manage Credentials:
https://console.cloud.google.com/apis/credentials

View Usage:
https://console.cloud.google.com/apis/dashboard

Billing & Alerts:
https://console.cloud.google.com/billing/
```

### Commands:

```bash
# Add API key to .env
echo 'GOOGLE_MAPS_API_KEY="YOUR_KEY_HERE"' >> backend/.env

# Restart backend
pkill -f "python.*main.py" && cd backend && ./venv/bin/python main.py

# Test API
curl -X POST "http://localhost:8000/api/nearby-stores?latitude=40.7128&longitude=-74.0060" \
  -H "Content-Type: application/json"
```

---

## ✨ Summary

### What You Need to Do:

1. ✅ Go to https://console.cloud.google.com/
2. ✅ Create project "Art-Decor-AI"
3. ✅ Enable 3 APIs (Places, Geocoding, Directions)
4. ✅ Create API key
5. ✅ Restrict API key (security)
6. ✅ Add to `backend/.env`
7. ✅ Restart backend
8. ✅ Test with real location

### Time Required: **10 minutes**

### Cost: **$0/month** (free tier covers most usage)

### Result:
- ✅ Real nearby stores instead of mock data
- ✅ Accurate distances and directions
- ✅ Current store hours and ratings
- ✅ Professional location features

---

**Need help? Check the troubleshooting section or refer to Google's official documentation!**

Good luck! 🗺️✨

