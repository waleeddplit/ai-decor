-- Art.Decor.AI Database Schema
-- PostgreSQL with Supabase
-- Run this in your Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enable pgvector extension for embeddings (if available)
-- CREATE EXTENSION IF NOT EXISTS vector;

-- ============================================
-- 1. User Profiles Table
-- ============================================
CREATE TABLE IF NOT EXISTS profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE,
    name TEXT,
    favorite_styles TEXT[] DEFAULT '{}',
    favorite_artworks TEXT[] DEFAULT '{}',
    budget_range JSONB DEFAULT '{"min": 0, "max": 1000}',
    location JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index for faster lookups
CREATE INDEX IF NOT EXISTS idx_profiles_email ON profiles(email);
CREATE INDEX IF NOT EXISTS idx_profiles_created_at ON profiles(created_at DESC);

-- ============================================
-- 2. Artworks Table
-- ============================================
CREATE TABLE IF NOT EXISTS artworks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    artist TEXT NOT NULL,
    description TEXT,
    price NUMERIC(10, 2),
    image_url TEXT NOT NULL,
    thumbnail_url TEXT,
    style TEXT,
    tags TEXT[] DEFAULT '{}',
    dimensions TEXT,
    medium TEXT,
    -- Embedding stored as JSON array (512 dimensions)
    -- If pgvector available, use: embedding VECTOR(512)
    embedding JSONB,
    metadata JSONB DEFAULT '{}',
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for search and filtering
CREATE INDEX IF NOT EXISTS idx_artworks_style ON artworks(style);
CREATE INDEX IF NOT EXISTS idx_artworks_price ON artworks(price);
CREATE INDEX IF NOT EXISTS idx_artworks_tags ON artworks USING GIN(tags);
CREATE INDEX IF NOT EXISTS idx_artworks_available ON artworks(is_available);
CREATE INDEX IF NOT EXISTS idx_artworks_created_at ON artworks(created_at DESC);

-- Full-text search index
CREATE INDEX IF NOT EXISTS idx_artworks_search ON artworks USING GIN(
    to_tsvector('english', COALESCE(title, '') || ' ' || COALESCE(artist, '') || ' ' || COALESCE(description, ''))
);

-- ============================================
-- 3. Room Analyses Table
-- ============================================
CREATE TABLE IF NOT EXISTS room_analyses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
    image_url TEXT,
    style TEXT,
    colors JSONB DEFAULT '[]',
    lighting JSONB DEFAULT '{}',
    detected_objects JSONB DEFAULT '[]',
    wall_spaces JSONB DEFAULT '[]',
    style_embedding JSONB,
    confidence_score NUMERIC(3, 2),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_room_analyses_user_id ON room_analyses(user_id);
CREATE INDEX IF NOT EXISTS idx_room_analyses_created_at ON room_analyses(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_room_analyses_style ON room_analyses(style);

-- ============================================
-- 4. Favorites Table
-- ============================================
CREATE TABLE IF NOT EXISTS favorites (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    artwork_id UUID NOT NULL REFERENCES artworks(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(user_id, artwork_id)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_favorites_user_id ON favorites(user_id);
CREATE INDEX IF NOT EXISTS idx_favorites_artwork_id ON favorites(artwork_id);
CREATE INDEX IF NOT EXISTS idx_favorites_created_at ON favorites(created_at DESC);

-- ============================================
-- 5. Stores Table (Local décor stores)
-- ============================================
CREATE TABLE IF NOT EXISTS stores (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    address TEXT,
    city TEXT,
    state TEXT,
    zipcode TEXT,
    latitude NUMERIC(10, 7),
    longitude NUMERIC(10, 7),
    phone TEXT,
    website TEXT,
    rating NUMERIC(2, 1),
    opening_hours JSONB DEFAULT '{}',
    categories TEXT[] DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Spatial index for location queries
CREATE INDEX IF NOT EXISTS idx_stores_location ON stores(latitude, longitude);
CREATE INDEX IF NOT EXISTS idx_stores_city ON stores(city);

-- ============================================
-- 6. Store Inventory Table (Artwork availability)
-- ============================================
CREATE TABLE IF NOT EXISTS store_inventory (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    store_id UUID NOT NULL REFERENCES stores(id) ON DELETE CASCADE,
    artwork_id UUID NOT NULL REFERENCES artworks(id) ON DELETE CASCADE,
    in_stock BOOLEAN DEFAULT TRUE,
    quantity INTEGER DEFAULT 1,
    price NUMERIC(10, 2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(store_id, artwork_id)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_store_inventory_store_id ON store_inventory(store_id);
CREATE INDEX IF NOT EXISTS idx_store_inventory_artwork_id ON store_inventory(artwork_id);
CREATE INDEX IF NOT EXISTS idx_store_inventory_in_stock ON store_inventory(in_stock);

-- ============================================
-- 7. Recommendations Log (Track recommendations)
-- ============================================
CREATE TABLE IF NOT EXISTS recommendations_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES profiles(id) ON DELETE SET NULL,
    room_analysis_id UUID REFERENCES room_analyses(id) ON DELETE CASCADE,
    artwork_ids UUID[] DEFAULT '{}',
    match_scores JSONB DEFAULT '{}',
    trends JSONB DEFAULT '[]',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_recommendations_log_user_id ON recommendations_log(user_id);
CREATE INDEX IF NOT EXISTS idx_recommendations_log_created_at ON recommendations_log(created_at DESC);

-- ============================================
-- Functions and Triggers
-- ============================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers for updated_at
CREATE TRIGGER update_profiles_updated_at BEFORE UPDATE ON profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_artworks_updated_at BEFORE UPDATE ON artworks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_stores_updated_at BEFORE UPDATE ON stores
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_store_inventory_updated_at BEFORE UPDATE ON store_inventory
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- Row Level Security (RLS) - Optional
-- ============================================

-- Enable RLS on profiles
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- Users can read their own profile
CREATE POLICY "Users can view own profile" ON profiles
    FOR SELECT USING (auth.uid() = id);

-- Users can update their own profile
CREATE POLICY "Users can update own profile" ON profiles
    FOR UPDATE USING (auth.uid() = id);

-- Enable RLS on favorites
ALTER TABLE favorites ENABLE ROW LEVEL SECURITY;

-- Users can manage their own favorites
CREATE POLICY "Users can view own favorites" ON favorites
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own favorites" ON favorites
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can delete own favorites" ON favorites
    FOR DELETE USING (auth.uid() = user_id);

-- Public read access for artworks and stores
ALTER TABLE artworks ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Anyone can view artworks" ON artworks
    FOR SELECT USING (TRUE);

ALTER TABLE stores ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Anyone can view stores" ON stores
    FOR SELECT USING (TRUE);

-- ============================================
-- Sample Data (Optional)
-- ============================================

-- Insert sample profile
INSERT INTO profiles (id, email, name, favorite_styles)
VALUES 
    ('00000000-0000-0000-0000-000000000001', 'demo@artdecor.ai', 'Demo User', ARRAY['Modern', 'Minimalist'])
ON CONFLICT (email) DO NOTHING;

-- Grant permissions (if needed)
-- GRANT ALL ON ALL TABLES IN SCHEMA public TO authenticated;
-- GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO authenticated;

-- ============================================
-- Views for Common Queries
-- ============================================

-- View: User favorites with artwork details
CREATE OR REPLACE VIEW user_favorites_with_artworks AS
SELECT 
    f.id,
    f.user_id,
    f.created_at,
    a.*
FROM favorites f
JOIN artworks a ON f.artwork_id = a.id
WHERE a.is_available = TRUE;

-- View: Store inventory with full details
CREATE OR REPLACE VIEW store_inventory_details AS
SELECT 
    si.id,
    si.store_id,
    si.artwork_id,
    si.in_stock,
    si.quantity,
    si.price,
    s.name as store_name,
    s.city,
    s.latitude,
    s.longitude,
    a.title as artwork_title,
    a.artist,
    a.style
FROM store_inventory si
JOIN stores s ON si.store_id = s.id
JOIN artworks a ON si.artwork_id = a.id
WHERE si.in_stock = TRUE AND a.is_available = TRUE;

-- ============================================
-- Database Stats Query
-- ============================================

-- Run this to check your data:
-- SELECT 
--     (SELECT COUNT(*) FROM profiles) as profiles_count,
--     (SELECT COUNT(*) FROM artworks) as artworks_count,
--     (SELECT COUNT(*) FROM room_analyses) as analyses_count,
--     (SELECT COUNT(*) FROM favorites) as favorites_count,
--     (SELECT COUNT(*) FROM stores) as stores_count;

