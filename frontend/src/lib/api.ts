/**
 * API Client for Art.Decor.AI Backend
 * Handles all communication with the FastAPI backend
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface RoomAnalysisRequest {
  description?: string;
}

export interface ColorInfo {
  name: string;
  hex: string;
  rgb: [number, number, number];
  percentage: number;
}

export interface LightingInfo {
  type?: string;
  quality?: string;
  brightness?: number | string;
  contrast?: number;
  temperature?: string;
  [key: string]: any; // Allow additional properties from backend
}

export interface DetectedObject {
  category?: string;
  class?: string;
  confidence: number;
  bbox?: [number, number, number, number];
  area?: number;
  [key: string]: any; // Allow additional properties from backend
}

export interface RoomAnalysisResponse {
  palette: ColorInfo[];
  lighting: LightingInfo | string; // Backend might return string or object
  style_vector: number[];
  detected_objects?: DetectedObject[];
  wall_spaces?: any[];
  style: string;
  confidence_score: number;
  processing_time: number;
  [key: string]: any; // Allow additional properties from backend
}

export interface RecommendationRequest {
  style_vector: number[];
  user_style?: string;
  room_type?: string;
  color_preferences?: string[];
  budget?: {
    min: number;
    max: number;
  };
  user_location?: {
    latitude: number;
    longitude: number;
  };
}

export interface ArtworkRecommendation {
  id: string;
  title: string;
  artist: string;
  style: string;
  colors?: string[];
  price: string | number;
  dimensions: string;
  image_url?: string;
  match_score: number;
  reasoning: string;
  availability?: {
    in_stock: boolean;
    stores: StoreInfo[];
  };
  stores?: any[];
  tags?: string[];
  medium?: string;
  // Real store integration fields
  purchase_url?: string;
  download_url?: string;
  source?: string;
  purchase_options?: any[];
  print_on_demand?: any[];
  attribution?: {
    photographer?: string;
    photographer_url?: string;
    required?: boolean;
  };
}

export interface StoreInfo {
  id: string;
  name: string;
  address: string;
  distance: number;
  rating: number;
  is_open: boolean;
  phone?: string;
  website?: string;
}

export interface RecommendationResponse {
  recommendations: ArtworkRecommendation[];
  trends: string[];
  nearby_stores: StoreInfo[];
}

/**
 * Analyze a room image
 */
export async function analyzeRoom(
  imageFile: File,
  description?: string
): Promise<RoomAnalysisResponse> {
  const formData = new FormData();
  formData.append('image', imageFile);
  if (description) {
    formData.append('description', description);
  }

  const response = await fetch(`${API_BASE_URL}/api/analyze_room`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `HTTP ${response.status}: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Get FAST artwork recommendations (2-3s)
 * FAISS + local catalog only, no external APIs
 */
export async function getFastRecommendations(
  request: RecommendationRequest
): Promise<RecommendationResponse> {
  const response = await fetch(`${API_BASE_URL}/api/recommend/fast`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `HTTP ${response.status}: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Get artwork recommendations (FULL with enrichment, 8-12s)
 */
export async function getRecommendations(
  request: RecommendationRequest
): Promise<RecommendationResponse> {
  const response = await fetch(`${API_BASE_URL}/api/recommend`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `HTTP ${response.status}: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Get trending styles
 */
export async function getTrendingStyles(limit: number = 10): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/api/recommend/trending?limit=${limit}`);

  if (!response.ok) {
    throw new Error('Failed to fetch trending styles');
  }

  return response.json();
}

/**
 * Enrich recommendations with AI reasoning (batch)
 * Call this in background after showing fast recommendations
 */
export async function enrichRecommendationsWithReasoning(
  artworks: Array<{
    id: string;
    title: string;
    style: string;
    match_score: number;
    tags?: string[];
  }>,
  roomStyle: string,
  colors: string[] = []
): Promise<{
  enriched_count: number;
  reasoning_list: Array<{ artwork_id: string; reasoning: string }>;
}> {
  const response = await fetch(`${API_BASE_URL}/api/recommend/enrich-reasoning`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      artworks,
      room_style: roomStyle,
      colors,
    }),
  });

  if (!response.ok) {
    throw new Error('Failed to enrich reasoning');
  }

  return response.json();
}

/**
 * Health check
 */
export async function checkHealth(): Promise<{ status: string; timestamp: string }> {
  const response = await fetch(`${API_BASE_URL}/health`);
  
  if (!response.ok) {
    throw new Error('Backend health check failed');
  }

  return response.json();
}

/**
 * Helper to check if backend is available
 */
export async function isBackendAvailable(): Promise<boolean> {
  try {
    await checkHealth();
    return true;
  } catch {
    return false;
  }
}

// ============================================
// Chat API
// ============================================

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
  image_url?: string;
}

export interface ChatRequest {
  message: string;
  conversation_id?: string;
  image?: string; // Base64 encoded image
  context?: {
    style?: string;
    style_vector?: number[];
    colors?: string[];
    preferences?: any;
  };
}

export interface ChatResponse {
  message: string;
  conversation_id: string;
  suggestions?: string[];
  recommendations?: any[];
  metadata?: {
    processing_time: number;
  };
}

export interface ConversationHistory {
  conversation_id: string;
  messages: ChatMessage[];
  message_count: number;
}

/**
 * Send a chat message
 */
export async function sendChatMessage(
  request: ChatRequest
): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE_URL}/api/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `HTTP ${response.status}: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Get chat history for a conversation
 */
export async function getChatHistory(
  conversationId: string
): Promise<ConversationHistory> {
  const response = await fetch(`${API_BASE_URL}/api/chat/history/${conversationId}`);

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `HTTP ${response.status}: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Clear chat history for a conversation
 */
export async function clearChatHistory(conversationId: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/api/chat/history/${conversationId}`, {
    method: 'DELETE',
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `HTTP ${response.status}: ${response.statusText}`);
  }
}

// ============================================================================
// Geo-Finder API Functions
// ============================================================================

export interface UserLocation {
  latitude: number;
  longitude: number;
  radius?: number;
}

export interface NearbyStore {
  id: string;
  name: string;
  address: string;
  location: {
    lat: number;
    lng: number;
  };
  rating: number;
  distance: number;
  phone?: string;
  website?: string;
  is_open?: boolean;
  opening_hours?: string[];
}

export interface NearbyStoresResponse {
  stores: NearbyStore[];
  total: number;
  search_location: {
    latitude: number;
    longitude: number;
  };
  radius_km: number;
}

export interface DirectionsResponse {
  directions: {
    distance: string;
    duration: string;
    steps: string[];
  };
  origin: {
    lat: number;
    lng: number;
  };
  destination: {
    lat: number;
    lng: number;
  };
}

/**
 * Get user's current location using browser geolocation API
 */
export function getUserLocation(): Promise<UserLocation> {
  return new Promise((resolve, reject) => {
    if (!('geolocation' in navigator)) {
      reject(new Error('Geolocation is not supported by your browser'));
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        resolve({
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
        });
      },
      (error) => {
        let errorMessage = 'Unable to retrieve location';
        switch (error.code) {
          case error.PERMISSION_DENIED:
            errorMessage = 'Location permission denied';
            break;
          case error.POSITION_UNAVAILABLE:
            errorMessage = 'Location information unavailable';
            break;
          case error.TIMEOUT:
            errorMessage = 'Location request timeout';
            break;
        }
        reject(new Error(errorMessage));
      },
      {
        enableHighAccuracy: true,
        timeout: 5000,
        maximumAge: 0,
      }
    );
  });
}

/**
 * Find nearby art stores and galleries
 */
export async function getNearbyStores(
  latitude: number,
  longitude: number,
  radius: number = 10000,
  storeType: string = 'art_gallery'
): Promise<NearbyStoresResponse> {
  const params = new URLSearchParams({
    latitude: latitude.toString(),
    longitude: longitude.toString(),
    radius: radius.toString(),
    store_type: storeType,
  });

  const response = await fetch(
    `${API_BASE_URL}/api/nearby-stores?${params}`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    }
  );

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `HTTP ${response.status}: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Get directions from user location to a store
 */
export async function getDirectionsToStore(
  originLat: number,
  originLng: number,
  destLat: number,
  destLng: number
): Promise<DirectionsResponse> {
  const params = new URLSearchParams({
    origin_lat: originLat.toString(),
    origin_lng: originLng.toString(),
    dest_lat: destLat.toString(),
    dest_lng: destLng.toString(),
  });

  const response = await fetch(
    `${API_BASE_URL}/api/directions?${params}`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    }
  );

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `HTTP ${response.status}: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Open Google Maps with directions
 */
export function openGoogleMapsDirections(
  originLat: number,
  originLng: number,
  destLat: number,
  destLng: number
): void {
  const url = `https://www.google.com/maps/dir/?api=1&origin=${originLat},${originLng}&destination=${destLat},${destLng}`;
  window.open(url, '_blank');
}

