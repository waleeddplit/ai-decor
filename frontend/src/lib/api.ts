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
 * Get artwork recommendations
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
 * Get nearby stores
 */
export async function getNearbyStores(
  latitude: number,
  longitude: number,
  radius: number = 10000
): Promise<StoreInfo[]> {
  const params = new URLSearchParams({
    latitude: latitude.toString(),
    longitude: longitude.toString(),
    radius: radius.toString(),
  });

  const response = await fetch(`${API_BASE_URL}/api/stores/nearby?${params}`);

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Unknown error' }));
    throw new Error(error.detail || `HTTP ${response.status}: ${response.statusText}`);
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

