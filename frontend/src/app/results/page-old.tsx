"use client";

import { useState } from "react";
import {
  MapPin,
  TrendingUp,
  Palette,
  Heart,
  ExternalLink,
  ChevronDown,
  ChevronUp,
} from "lucide-react";
import Link from "next/link";

/**
 * Results Page
 * Displays AI-generated décor recommendations with reasoning
 */

// Mock recommendation data
const mockRecommendations = [
  {
    id: 1,
    title: "Abstract Geometric Canvas",
    artist: "Modern Art Studio",
    price: "$249",
    image:
      "https://images.unsplash.com/photo-1541961017774-22349e4a1262?w=400&h=400&fit=crop",
    matchScore: 95,
    tags: ["Modern", "Abstract", "Geometric"],
    reasoning:
      "This piece complements your minimalist aesthetic with clean lines and neutral tones that match your existing color palette.",
    stores: ["Gallery Downtown", "Art House"],
  },
  {
    id: 2,
    title: "Botanical Line Art Print",
    artist: "Nature Studio",
    price: "$129",
    image:
      "https://images.unsplash.com/photo-1513519245088-0e12902e35ca?w=400&h=400&fit=crop",
    matchScore: 92,
    tags: ["Botanical", "Minimalist", "Line Art"],
    reasoning:
      "The organic shapes and muted green tones bring natural warmth to your space while maintaining the clean aesthetic.",
    stores: ["Green Gallery", "Urban Décor"],
  },
  {
    id: 3,
    title: "Sunset Watercolor",
    artist: "Color Waves",
    price: "$189",
    image:
      "https://images.unsplash.com/photo-1578926375605-eaf7559b0220?w=400&h=400&fit=crop",
    matchScore: 88,
    tags: ["Watercolor", "Warm Tones", "Abstract"],
    reasoning:
      "Warm sunset hues add a cozy atmosphere and work beautifully with your room's natural lighting.",
    stores: ["Sunset Art Co."],
  },
];

export default function ResultsPage() {
  const [expandedReasoning, setExpandedReasoning] = useState<number | null>(
    null
  );
  const [favorites, setFavorites] = useState<Set<number>>(new Set());

  const toggleFavorite = (id: number) => {
    const newFavorites = new Set(favorites);
    if (newFavorites.has(id)) {
      newFavorites.delete(id);
    } else {
      newFavorites.add(id);
    }
    setFavorites(newFavorites);
  };

  const toggleReasoning = (id: number) => {
    setExpandedReasoning(expandedReasoning === id ? null : id);
  };

  return (
    <div className="container mx-auto max-w-7xl px-4 py-12">
      {/* Header */}
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white">
          Your Personalized Recommendations
        </h1>
        <p className="mt-4 text-lg text-gray-600 dark:text-gray-400">
          AI-curated décor matched to your room's style and aesthetic
        </p>
      </div>

      {/* Room Analysis Summary */}
      <div className="mt-12 rounded-xl border border-gray-200 bg-gradient-to-br from-purple-50 to-pink-50 p-8 dark:border-gray-800 dark:from-purple-900/20 dark:to-pink-900/20">
        <h2 className="flex items-center gap-2 text-xl font-semibold text-gray-900 dark:text-white">
          <Palette className="h-6 w-6 text-purple-600 dark:text-purple-400" />
          Room Analysis
        </h2>

        <div className="mt-6 grid gap-6 sm:grid-cols-3">
          <div>
            <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">
              Detected Style
            </h3>
            <p className="mt-2 text-lg font-semibold text-gray-900 dark:text-white">
              Modern Minimalist
            </p>
          </div>

          <div>
            <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">
              Color Palette
            </h3>
            <div className="mt-2 flex gap-2">
              <div
                className="h-8 w-8 rounded-full bg-white ring-2 ring-gray-300"
                title="#FFFFFF"
              />
              <div
                className="h-8 w-8 rounded-full bg-gray-200 ring-2 ring-gray-300"
                title="#E5E7EB"
              />
              <div
                className="h-8 w-8 rounded-full bg-gray-800 ring-2 ring-gray-300"
                title="#1F2937"
              />
              <div
                className="h-8 w-8 rounded-full bg-amber-100 ring-2 ring-gray-300"
                title="#FEF3C7"
              />
            </div>
          </div>

          <div>
            <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">
              Lighting
            </h3>
            <p className="mt-2 text-lg font-semibold text-gray-900 dark:text-white">
              Natural, Bright
            </p>
          </div>
        </div>
      </div>

      {/* Recommendations Grid */}
      <div className="mt-12">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
          Recommended Pieces ({mockRecommendations.length})
        </h2>

        <div className="mt-8 grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
          {mockRecommendations.map((rec) => (
            <div
              key={rec.id}
              className="group overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm transition-shadow hover:shadow-lg dark:border-gray-800 dark:bg-gray-950"
            >
              {/* Image */}
              <div className="relative aspect-square overflow-hidden bg-gray-100 dark:bg-gray-900">
                <img
                  src={rec.image}
                  alt={rec.title}
                  className="h-full w-full object-cover transition-transform group-hover:scale-105"
                />

                {/* Match Score Badge */}
                <div className="absolute left-3 top-3 rounded-full bg-purple-600 px-3 py-1 text-sm font-semibold text-white">
                  {rec.matchScore}% Match
                </div>

                {/* Favorite Button */}
                <button
                  onClick={() => toggleFavorite(rec.id)}
                  className="absolute right-3 top-3 rounded-full bg-white/90 p-2 backdrop-blur-sm transition-colors hover:bg-white dark:bg-gray-900/90 dark:hover:bg-gray-900"
                >
                  <Heart
                    className={`h-5 w-5 ${
                      favorites.has(rec.id)
                        ? "fill-red-500 text-red-500"
                        : "text-gray-600 dark:text-gray-400"
                    }`}
                  />
                </button>
              </div>

              {/* Content */}
              <div className="p-6">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                  {rec.title}
                </h3>
                <p className="mt-1 text-sm text-gray-600 dark:text-gray-400">
                  {rec.artist}
                </p>

                <p className="mt-2 text-xl font-bold text-purple-600 dark:text-purple-400">
                  {rec.price}
                </p>

                {/* Tags */}
                <div className="mt-4 flex flex-wrap gap-2">
                  {rec.tags.map((tag) => (
                    <span
                      key={tag}
                      className="rounded-full bg-gray-100 px-3 py-1 text-xs font-medium text-gray-700 dark:bg-gray-800 dark:text-gray-300"
                    >
                      {tag}
                    </span>
                  ))}
                </div>

                {/* AI Reasoning */}
                <div className="mt-4">
                  <button
                    onClick={() => toggleReasoning(rec.id)}
                    className="flex w-full items-center justify-between text-sm font-medium text-purple-600 dark:text-purple-400"
                  >
                    <span className="flex items-center gap-2">
                      <TrendingUp className="h-4 w-4" />
                      Why this matches
                    </span>
                    {expandedReasoning === rec.id ? (
                      <ChevronUp className="h-4 w-4" />
                    ) : (
                      <ChevronDown className="h-4 w-4" />
                    )}
                  </button>

                  {expandedReasoning === rec.id && (
                    <p className="mt-3 text-sm text-gray-600 dark:text-gray-400">
                      {rec.reasoning}
                    </p>
                  )}
                </div>

                {/* Local Stores */}
                <div className="mt-4 border-t border-gray-200 pt-4 dark:border-gray-800">
                  <div className="flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400">
                    <MapPin className="h-4 w-4" />
                    <span>Available at {rec.stores.length} nearby stores</span>
                  </div>

                  <button className="mt-3 flex w-full items-center justify-center gap-2 rounded-lg bg-purple-600 px-4 py-2 text-sm font-semibold text-white transition-colors hover:bg-purple-700 dark:bg-purple-500 dark:hover:bg-purple-600">
                    <ExternalLink className="h-4 w-4" />
                    View Stores
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Actions */}
      <div className="mt-12 flex flex-wrap justify-center gap-4">
        <Link
          href="/upload"
          className="inline-flex items-center gap-2 rounded-lg border border-gray-300 bg-white px-6 py-3 text-base font-semibold text-gray-900 transition-colors hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:hover:bg-gray-800"
        >
          Try Another Room
        </Link>

        <Link
          href="/chat"
          className="inline-flex items-center gap-2 rounded-lg bg-purple-600 px-6 py-3 text-base font-semibold text-white transition-colors hover:bg-purple-700 dark:bg-purple-500 dark:hover:bg-purple-600"
        >
          Refine with Chat
        </Link>
      </div>
    </div>
  );
}
