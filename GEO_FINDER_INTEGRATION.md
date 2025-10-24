# 🗺️ Geo-Finder Agent Integration Guide

## Overview

The **Geo-Finder Agent** finds nearby art galleries, décor stores, and furniture shops based on user location. It uses Google Maps API for real store data or provides mock data when the API is not configured.

### Features:
✅ **Find nearby art galleries** within customizable radius  
✅ **Google Maps integration** for real store data  
✅ **Distance calculation** using Haversine formula  
✅ **Store details**: address, phone, website, hours, ratings  
✅ **Directions** from user location to store  
✅ **Automatic integration** with recommendations  
✅ **Mock data fallback** when API not configured

---

## 🚀 Quick Start (Without API)

The Geo-Finder works **immediately with mock data**—no API key required for testing!

### Test It Now:

```bash
# 1. Backend should be running
cd backend
./venv/bin/python main.py

# 2. Get nearby stores (mock data)
curl -X POST "http://localhost:8000/api/nearby-stores?latitude=37.7749&longitude=-122.4194&radius=10000" \
  -H "Content-Type: application/json"
```

**Response:**
```json
{
  "stores": [
    {
      "id": "mock_1",
      "name": "Gallery Downtown",
      "address": "123 Art Street, Downtown",
      "location": {"lat": 37.7849, "lng": -122.4094},
      "rating": 4.5,
      "distance": 1.2,
      "phone": "(555) 123-4567",
      "website": "https://gallerydowntown.com",
      "is_open": true,
      "opening_hours": [...]
    },
    ...
  ],
  "total": 3,
  "search_location": {"latitude": 37.7749, "longitude": -122.4194},
  "radius_km": 10
}
```

---

## 🔑 Setup Google Maps API (Optional, Recommended)

### Why Use Google Maps API?
- ✅ **Real store data** (not mock)
- ✅ **Accurate distances** and directions
- ✅ **Current store hours** and ratings
- ✅ **Phone numbers** and websites
- ✅ **Up-to-date** store information

### Step 1: Get API Key (5 minutes, FREE)

1. **Go to Google Cloud Console**
   https://console.cloud.google.com/

2. **Create a project** (or select existing)
   - Click "Select a project" → "New Project"
   - Name: `Art-Decor-AI`
   - Click "Create"

3. **Enable APIs**
   - Go to "APIs & Services" → "Library"
   - Search for and enable:
     - **Places API**
     - **Geocoding API**
     - **Directions API**

4. **Create API Key**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "API Key"
   - Copy the generated key

5. **Restrict API Key** (Recommended)
   - Click on your key → "Edit"
   - Application restrictions: HTTP referrers or IP addresses
   - API restrictions: Select only the 3 APIs above
   - Save

### Step 2: Add to Your Project

```bash
cd /Users/waleedali/Documents/DPLProjects/ai-decorator/backend
echo 'GOOGLE_MAPS_API_KEY="your_api_key_here"' >> .env
```

### Step 3: Restart Backend

```bash
# Backend auto-reloads, or restart:
pkill -f "python.*main.py"
./venv/bin/python main.py
```

**You should see:**
```
GeoFinderAgent initialized with Google Maps API ← Real API active!
```

---

## 📊 API Endpoints

### 1. Get Nearby Stores

**Endpoint:** `POST /api/nearby-stores`

**Parameters:**
- `latitude` (required): User's latitude
- `longitude` (required): User's longitude
- `radius` (optional): Search radius in meters (default: 10000 = 10km)
- `store_type` (optional): Type of store (default: "art_gallery")

**Store Types:**
- `art_gallery` - Art galleries and fine art shops
- `home_goods_store` - Home décor and furniture
- `furniture_store` - Furniture retailers
- `department_store` - Large retailers with art sections

**Example Request:**

```bash
curl -X POST "http://localhost:8000/api/nearby-stores?latitude=40.7128&longitude=-74.0060&radius=5000&store_type=art_gallery" \
  -H "Content-Type: application/json"
```

**Example Response:**

```json
{
  "stores": [
    {
      "id": "ChIJxxxxx",
      "name": "MoMA Design Store",
      "address": "11 W 53rd St, New York",
      "location": {"lat": 40.7614, "lng": -73.9776},
      "rating": 4.6,
      "distance": 4.2,
      "phone": "(212) 767-1050",
      "website": "https://store.moma.org",
      "is_open": true,
      "opening_hours": [
        "Monday: 10:00 AM – 6:00 PM",
        ...
      ]
    }
  ],
  "total": 5,
  "search_location": {"latitude": 40.7128, "longitude": -74.0060},
  "radius_km": 5
}
```

---

### 2. Get Directions to Store

**Endpoint:** `POST /api/directions`

**Parameters:**
- `origin_lat` (required): User's latitude
- `origin_lng` (required): User's longitude
- `dest_lat` (required): Store's latitude
- `dest_lng` (required): Store's longitude

**Example Request:**

```bash
curl -X POST "http://localhost:8000/api/directions?origin_lat=40.7128&origin_lng=-74.0060&dest_lat=40.7614&dest_lng=-73.9776" \
  -H "Content-Type: application/json"
```

**Example Response:**

```json
{
  "directions": {
    "distance": "7.2 km",
    "duration": "18 mins",
    "steps": [
      "Head north on Broadway",
      "Turn right onto W 53rd St",
      "Destination will be on the right"
    ]
  },
  "origin": {"lat": 40.7128, "lng": -74.0060},
  "destination": {"lat": 40.7614, "lng": -73.9776}
}
```

---

### 3. Recommendations with Location

**Endpoint:** `POST /api/recommend` (enhanced)

**Now includes automatic nearby stores when `user_location` is provided!**

**Example Request:**

```bash
curl -X POST "http://localhost:8000/api/recommend" \
  -H "Content-Type: application/json" \
  -d '{
    "style_vector": [0.1, 0.2, 0.3, ...],
    "user_style": "Modern",
    "color_preferences": ["#E8E8E8"],
    "user_location": {
      "latitude": 40.7128,
      "longitude": -74.0060,
      "radius": 10000
    },
    "limit": 3
  }'
```

**Response includes `stores` for each recommendation:**

```json
{
  "recommendations": [
    {
      "id": "artwork_001",
      "title": "Abstract Geometric Canvas",
      "artist": "Modern Art Studio",
      "price": "$249",
      "image_url": "...",
      "match_score": 95.0,
      "reasoning": "...",
      "stores": [
        {
          "name": "MoMA Design Store",
          "address": "11 W 53rd St, New York",
          "distance": "4.2 km",
          "rating": 4.6,
          "phone": "(212) 767-1050",
          "website": "https://store.moma.org",
          "is_open": true,
          "lat": 40.7614,
          "lng": -73.9776
        },
        ...
      ]
    }
  ],
  "trends": [...]
}
```

---

## 🎨 Frontend Integration

### 1. Get User Location

```typescript
// In frontend/src/app/upload/page.tsx

const getUserLocation = (): Promise<{latitude: number, longitude: number}> => {
  return new Promise((resolve, reject) => {
    if ('geolocation' in navigator) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          resolve({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
          });
        },
        (error) => {
          console.error('Error getting location:', error);
          reject(error);
        }
      );
    } else {
      reject(new Error('Geolocation not supported'));
    }
  });
};
```

### 2. Send Location with Recommendations Request

```typescript
// When analyzing room
const analysis = await analyzeRoom(imageFile);

// Get user location
let userLocation = null;
try {
  userLocation = await getUserLocation();
} catch (error) {
  console.log('Location not available, continuing without nearby stores');
}

// Get recommendations with location
const recommendations = await getRecommendations({
  style_vector: analysis.style_vector,
  user_style: analysis.style,
  color_preferences: analysis.palette.map(c => c.hex),
  user_location: userLocation ? {
    latitude: userLocation.latitude,
    longitude: userLocation.longitude,
    radius: 10000  // 10km
  } : null
});
```

### 3. Display Nearby Stores

```typescript
// In frontend/src/app/results/page.tsx

{rec.stores && rec.stores.length > 0 && (
  <div className="mt-4 border-t pt-4">
    <h4 className="font-semibold mb-2">📍 Available Nearby</h4>
    {rec.stores.slice(0, 3).map((store, idx) => (
      <div key={idx} className="p-2 border rounded mb-2">
        <div className="flex justify-between items-start">
          <div>
            <p className="font-medium">{store.name}</p>
            <p className="text-sm text-gray-600">{store.address}</p>
            <p className="text-sm">
              <span className="text-green-600">
                {store.is_open ? '🟢 Open' : '🔴 Closed'}
              </span>
              {' • '}
              {store.distance}
              {' • '}
              ⭐ {store.rating}
            </p>
          </div>
          <div className="flex gap-2">
            {store.phone && store.phone !== 'N/A' && (
              <a href={`tel:${store.phone}`} className="text-blue-600">
                📞
              </a>
            )}
            {store.website && store.website !== 'N/A' && (
              <a href={store.website} target="_blank" className="text-blue-600">
                🌐
              </a>
            )}
            <button
              onClick={() => getDirections(store.lat, store.lng)}
              className="text-blue-600"
            >
              🗺️
            </button>
          </div>
        </div>
      </div>
    ))}
  </div>
)}
```

### 4. Get Directions

```typescript
const getDirections = async (destLat: number, destLng: number) => {
  try {
    const userLocation = await getUserLocation();
    
    const response = await fetch(
      `http://localhost:8000/api/directions?` +
      `origin_lat=${userLocation.latitude}&` +
      `origin_lng=${userLocation.longitude}&` +
      `dest_lat=${destLat}&dest_lng=${destLng}`,
      { method: 'POST' }
    );
    
    const data = await response.json();
    
    // Show directions in modal or open Google Maps
    window.open(
      `https://www.google.com/maps/dir/?api=1&` +
      `origin=${userLocation.latitude},${userLocation.longitude}&` +
      `destination=${destLat},${destLng}`,
      '_blank'
    );
  } catch (error) {
    console.error('Error getting directions:', error);
  }
};
```

---

## 💰 Google Maps API Pricing

### Free Tier (Monthly):
- **Places API**: $200 free credit = ~40,000 requests
- **Geocoding API**: $200 free credit = ~40,000 requests  
- **Directions API**: $200 free credit = ~40,000 requests

### Costs After Free Tier:
- Places Nearby Search: $0.032 per request
- Place Details: $0.017 per request
- Directions: $0.005 per request

### For 1,000 users/month:
- Assume 50% provide location = 500 requests
- Places Nearby: 500 × $0.032 = **$16/month**
- Place Details: 500 × $0.017 = **$8.50/month**
- Total: **~$25/month** (well within free tier!)

### For 10,000 users/month:
- 5,000 location requests
- Total cost: **~$250/month**
- Still mostly covered by $200 free credit!

**Recommendation:** Start with free tier, add billing only when needed.

---

## 🧪 Testing

### Test 1: Mock Data (No API Key)

```bash
curl -X POST "http://localhost:8000/api/nearby-stores?latitude=37.7749&longitude=-122.4194" \
  -H "Content-Type: application/json" | python3 -m json.tool
```

**Should return 3 mock stores**

### Test 2: Real API (With API Key)

```bash
# Set API key first
export GOOGLE_MAPS_API_KEY="your_key"

# Test NYC
curl -X POST "http://localhost:8000/api/nearby-stores?latitude=40.7128&longitude=-74.0060" \
  -H "Content-Type: application/json" | python3 -m json.tool
```

**Should return real art galleries in NYC**

### Test 3: Recommendations with Location

```bash
curl -X POST "http://localhost:8000/api/recommend" \
  -H "Content-Type: application/json" \
  -d '{
    "style_vector": [0.1, 0.2, 0.3],
    "user_style": "Modern",
    "user_location": {
      "latitude": 40.7128,
      "longitude": -74.0060
    }
  }' | python3 -c "import json, sys; data = json.load(sys.stdin); print(f\"Stores: {len(data['recommendations'][0].get('stores', []))}\")"
```

**Should show nearby stores count**

---

## 🎯 User Experience

### Without Location:
```
[Artwork Image]
Abstract Geometric Canvas
$249

🛒 Buy on Art.com
From Tavily Search
```

### With Location:
```
[Artwork Image]
Abstract Geometric Canvas
$249

🛒 Buy on Art.com
From Tavily Search

📍 Available Nearby:
• MoMA Design Store - 4.2 km away ⭐ 4.6
  11 W 53rd St, New York
  🟢 Open • 📞 Call • 🗺️ Directions

• Chelsea Gallery - 6.1 km away ⭐ 4.8
  465 W 25th St, New York  
  🟢 Open • 📞 Call • 🗺️ Directions
```

---

## ✨ Summary

### What You Have Now:
✅ **Automatic nearby store detection** when user provides location  
✅ **Google Maps integration** (optional, works with mock data)  
✅ **Distance calculation** using Haversine formula  
✅ **Store details** with ratings, hours, contact info  
✅ **Directions API** integrated  
✅ **Two dedicated endpoints** for stores and directions  
✅ **Enhanced recommendations** with local availability

### Cost:
- **Without API:** $0 (uses mock data)
- **With API (1,000 users):** $0 (free tier)
- **With API (10,000 users):** ~$50/month

### Setup Time:
- **Mock data:** 0 minutes (already working!)
- **Real API:** 5 minutes (optional)

---

**The Geo-Finder Agent is now fully integrated! 🗺️✨**

Test it: Upload a room image and allow location access to see nearby stores!

