"use client";

import { useState, useEffect } from "react";
import {
  MapPin,
  TrendingUp,
  Palette,
  Heart,
  ExternalLink,
  ChevronDown,
  ChevronUp,
  Loader2,
  AlertCircle,
  ArrowLeft,
  ShoppingCart,
  Download,
  Store,
  Navigation,
  X,
  Clock,
  Phone,
  Globe,
} from "lucide-react";
import Link from "next/link";
import {
  getFastRecommendations,
  getTrendingStyles,
  getNearbyStores,
  enrichRecommendationsWithReasoning,
  type RoomAnalysisResponse,
  type ArtworkRecommendation,
  type ColorInfo,
} from "@/lib/api";

/**
 * Results Page - Connected to Backend
 * Displays real AI-generated décor recommendations with reasoning
 */

export default function ResultsPage() {
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showDirections, setShowDirections] = useState(false);
  const [selectedStore, setSelectedStore] = useState<any>(null);
  const [directionsData, setDirectionsData] = useState<any>(null);
  const [loadingDirections, setLoadingDirections] = useState(false);
  const [roomAnalysis, setRoomAnalysis] = useState<RoomAnalysisResponse | null>(
    null
  );
  const [roomImage, setRoomImage] = useState<string>("");
  const [recommendations, setRecommendations] = useState<
    ArtworkRecommendation[]
  >([]);
  const [trendingStyles, setTrendingStyles] = useState<string[]>([]);
  const [expandedReasoning, setExpandedReasoning] = useState<string | null>(
    null
  );
  const [favorites, setFavorites] = useState<Set<string>>(new Set());
  const [nearbyStores, setNearbyStores] = useState<any[]>([]);
  const [isEnrichingReasoning, setIsEnrichingReasoning] = useState(false);

  useEffect(() => {
    loadResults();
  }, []);

  const loadResults = async () => {
    try {
      // Get room analysis from sessionStorage
      const analysisData = sessionStorage.getItem("roomAnalysis");
      const imageData = sessionStorage.getItem("roomImage");
      const locationData = sessionStorage.getItem("userLocation");

      if (!analysisData) {
        setError("No room analysis found. Please upload a room image first.");
        setIsLoading(false);
        return;
      }

      const analysis: RoomAnalysisResponse = JSON.parse(analysisData);
      setRoomAnalysis(analysis);
      setRoomImage(imageData || "");

      // Parse user location if available
      let userLocation = null;
      if (locationData) {
        try {
          userLocation = JSON.parse(locationData);
          console.log("📍 Using stored location:", userLocation);
        } catch (e) {
          console.error("Error parsing user location:", e);
        }
      }

      // PROGRESSIVE LOADING: Get fast recommendations first (2-3s)
      const fastData = await getFastRecommendations({
        style_vector: analysis.style_vector,
        user_style: analysis.style,
        color_preferences: analysis.palette.map((c) => c.hex),
      });

      // Show fast results immediately (without reasoning text)
      setRecommendations(
        fastData.recommendations.map((rec) => ({
          ...rec,
          reasoning: "", // Empty reasoning - will show skeleton loader
        }))
      );
      setIsLoading(false);
      setIsEnrichingReasoning(true);
      console.log(`⚡ Fast recommendations loaded`);

      // Enrich with AI reasoning in background (LLaVA/Ollama)
      if (fastData.recommendations.length > 0) {
        console.log(
          `🧠 Enriching ${fastData.recommendations.length} recommendations with AI reasoning...`
        );
        enrichRecommendationsWithReasoning(
          fastData.recommendations.map((rec) => ({
            id: rec.id,
            title: rec.title,
            style: rec.style,
            match_score: rec.match_score,
            tags: rec.tags,
          })),
          analysis.style,
          analysis.palette.map((c) => c.hex)
        )
          .then((enrichedData) => {
            console.log(
              `✅ AI reasoning loaded for ${enrichedData.enriched_count} items`
            );

            // Update recommendations with AI reasoning
            setRecommendations((prevRecs) =>
              prevRecs.map((rec) => {
                const enriched = enrichedData.reasoning_list.find(
                  (r) => r.artwork_id === rec.id
                );
                if (enriched) {
                  return { ...rec, reasoning: enriched.reasoning };
                }
                return rec;
              })
            );
            setIsEnrichingReasoning(false);
          })
          .catch((e) => {
            console.error("AI reasoning failed:", e);
            console.log("💡 Using fallback reasoning");
            // Fallback to original template reasoning
            setRecommendations((prevRecs) =>
              prevRecs.map((rec, idx) => {
                const original = fastData.recommendations[idx];
                return {
                  ...rec,
                  reasoning: original?.reasoning || rec.reasoning,
                };
              })
            );
            setIsEnrichingReasoning(false);
          });
      }

      // Load trending styles in background (no await - happens async)
      getTrendingStyles(5)
        .then((trendsData) => {
          setTrendingStyles(trendsData.trending_styles || []);
          console.log(`📈 Trends loaded`);
        })
        .catch((e) => console.error("Trends failed:", e));

      // Load nearby stores in background if location available
      if (userLocation?.latitude && userLocation?.longitude) {
        getNearbyStores(
          userLocation.latitude,
          userLocation.longitude,
          userLocation.radius || 10000
        )
          .then((storesData) => {
            setNearbyStores(storesData.stores || []);
            console.log(
              `📍 Loaded ${storesData.stores?.length || 0} nearby stores`
            );
          })
          .catch((e) => console.error("Stores failed:", e));
      }
    } catch (err) {
      console.error("Error loading results:", err);
      setError(
        err instanceof Error
          ? err.message
          : "Failed to load recommendations. Please try again."
      );
      setIsLoading(false);
    }
  };

  const toggleFavorite = (id: string) => {
    const newFavorites = new Set(favorites);
    if (newFavorites.has(id)) {
      newFavorites.delete(id);
    } else {
      newFavorites.add(id);
    }
    setFavorites(newFavorites);
  };

  const handleGetDirections = async (store: any) => {
    setSelectedStore(store);
    setShowDirections(true);
    setLoadingDirections(true);
    setDirectionsData(null);

    try {
      const locationData = sessionStorage.getItem("userLocation");
      if (!locationData) {
        setDirectionsData({
          error:
            "Your location is not available. Please enable location services.",
        });
        setLoadingDirections(false);
        return;
      }

      const userLocation = JSON.parse(locationData);
      const { getDirectionsToStore } = await import("@/lib/api");

      const directions = await getDirectionsToStore(
        userLocation.latitude,
        userLocation.longitude,
        store.lat,
        store.lng
      );

      setDirectionsData(directions);
      setLoadingDirections(false);
    } catch (error) {
      console.error("Error fetching directions:", error);
      setDirectionsData({
        error: "Failed to load directions. Please try again.",
      });
      setLoadingDirections(false);
    }
  };

  const toggleReasoning = (id: string) => {
    setExpandedReasoning(expandedReasoning === id ? null : id);
  };

  // Loading state
  if (isLoading) {
    return (
      <div className="container mx-auto max-w-7xl px-4 py-12">
        <div className="flex flex-col items-center justify-center py-20">
          <Loader2 className="h-12 w-12 animate-spin text-purple-600 dark:text-purple-400" />
          <p className="mt-4 text-lg text-gray-600 dark:text-gray-400">
            Generating personalized recommendations...
          </p>
        </div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="container mx-auto max-w-4xl px-4 py-12">
        <div className="rounded-lg bg-red-50 border border-red-200 p-6 dark:bg-red-900/20 dark:border-red-800">
          <div className="flex items-start gap-3">
            <AlertCircle className="h-6 w-6 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="text-lg font-semibold text-red-800 dark:text-red-200">
                Error Loading Results
              </h3>
              <p className="mt-2 text-sm text-red-700 dark:text-red-300">
                {error}
              </p>
              <div className="mt-4 flex gap-3">
                <Link
                  href="/upload"
                  className="inline-flex items-center gap-2 rounded-lg bg-red-600 px-4 py-2 text-sm font-semibold text-white transition-colors hover:bg-red-700"
                >
                  <ArrowLeft className="h-4 w-4" />
                  Upload New Image
                </Link>
                <button
                  onClick={loadResults}
                  className="inline-flex items-center gap-2 rounded-lg border border-red-300 px-4 py-2 text-sm font-semibold text-red-700 transition-colors hover:bg-red-100 dark:border-red-700 dark:text-red-300 dark:hover:bg-red-900/30"
                >
                  Try Again
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!roomAnalysis) return null;

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

      {/* Room Image Preview */}
      {roomImage && (
        <div className="mt-8 flex justify-center">
          <div className="relative max-w-md overflow-hidden rounded-xl border border-gray-200 dark:border-gray-800">
            <img
              src={roomImage}
              alt="Your room"
              className="h-auto w-full object-cover"
            />
            <div className="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/60 to-transparent p-4">
              <p className="text-sm font-medium text-white">Your Room</p>
            </div>
          </div>
        </div>
      )}

      {/* Room Analysis Summary */}
      <div className="mt-12 rounded-xl border border-gray-200 bg-gradient-to-br from-purple-50 to-pink-50 p-8 dark:border-gray-800 dark:from-purple-900/20 dark:to-pink-900/20">
        <h2 className="flex items-center gap-2 text-xl font-semibold text-gray-900 dark:text-white">
          <Palette className="h-6 w-6 text-purple-600 dark:text-purple-400" />
          Room Analysis
        </h2>

        <div className="mt-6 grid gap-6 sm:grid-cols-3">
          {/* Detected Style */}
          <div>
            <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">
              Detected Style
            </h3>
            <p className="mt-2 text-lg font-semibold text-gray-900 dark:text-white">
              {roomAnalysis.style}
            </p>
            <p className="mt-1 text-sm text-gray-500 dark:text-gray-500">
              {(roomAnalysis.confidence_score * 100).toFixed(0)}% confidence
            </p>
          </div>

          {/* Color Palette */}
          <div>
            <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">
              Color Palette
            </h3>
            <div className="mt-2 flex gap-2">
              {roomAnalysis.palette
                .slice(0, 5)
                .map((color: ColorInfo, idx: number) => (
                  <div
                    key={idx}
                    className="h-8 w-8 rounded-full ring-2 ring-gray-300 dark:ring-gray-600"
                    style={{ backgroundColor: color.hex }}
                    title={`${color.name} (${color.percentage.toFixed(1)}%)`}
                  />
                ))}
            </div>
            <div className="mt-2 flex flex-wrap gap-1">
              {roomAnalysis.palette
                .slice(0, 3)
                .map((color: ColorInfo, idx: number) => (
                  <span
                    key={idx}
                    className="text-xs text-gray-600 dark:text-gray-400"
                  >
                    {color.name}
                    {idx < 2 ? "," : ""}
                  </span>
                ))}
            </div>
          </div>

          {/* Lighting */}
          <div>
            <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">
              Lighting
            </h3>
            <p className="mt-2 text-lg font-semibold text-gray-900 dark:text-white">
              {typeof roomAnalysis.lighting === "string"
                ? roomAnalysis.lighting
                : `${roomAnalysis.lighting?.type || "Natural"}${
                    roomAnalysis.lighting?.quality
                      ? `, ${roomAnalysis.lighting.quality}`
                      : ""
                  }`}
            </p>
            <p className="mt-1 text-sm text-gray-500 dark:text-gray-500">
              Processing: {roomAnalysis.processing_time.toFixed(2)}s
            </p>
          </div>
        </div>

        {/* Detected Objects */}
        {roomAnalysis.detected_objects &&
          roomAnalysis.detected_objects.length > 0 && (
            <div className="mt-6 border-t border-gray-200 pt-6 dark:border-gray-700">
              <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">
                Detected Objects
              </h3>
              <div className="mt-2 flex flex-wrap gap-2">
                {roomAnalysis.detected_objects.slice(0, 5).map((obj, idx) => (
                  <span
                    key={idx}
                    className="rounded-full bg-purple-100 px-3 py-1 text-xs font-medium text-purple-700 dark:bg-purple-900/30 dark:text-purple-300"
                  >
                    {obj.label || obj.class || "Object"} (
                    {(obj.confidence * 100).toFixed(0)}%)
                  </span>
                ))}
              </div>
            </div>
          )}
      </div>

      {/* Trending Styles */}
      {trendingStyles && trendingStyles.length > 0 && (
        <div className="mt-12 rounded-xl border border-purple-200 bg-gradient-to-r from-purple-50 to-pink-50 p-6 dark:border-purple-800 dark:from-purple-900/20 dark:to-pink-900/20">
          <div className="flex items-center gap-2">
            <TrendingUp className="h-6 w-6 text-purple-600 dark:text-purple-400" />
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              Trending Now in Interior Design
            </h3>
          </div>
          <div className="mt-4 flex flex-wrap gap-2">
            {trendingStyles.map((trend, idx) => (
              <span
                key={idx}
                className="inline-flex items-center rounded-full bg-white px-4 py-2 text-sm font-medium text-purple-700 shadow-sm ring-1 ring-purple-200 dark:bg-gray-800 dark:text-purple-300 dark:ring-purple-700"
              >
                <TrendingUp className="mr-2 h-4 w-4" />
                {typeof trend === "string"
                  ? trend
                  : trend.style || trend.description || "Trending Style"}
              </span>
            ))}
          </div>
          <p className="mt-3 text-sm text-gray-600 dark:text-gray-400">
            These are the hottest styles in décor right now. Your
            recommendations align with current design trends!
          </p>
        </div>
      )}

      {/* Recommendations Grid */}
      <div className="mt-12">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
          Recommended Pieces ({recommendations.length})
        </h2>

        {recommendations.length === 0 ? (
          <div className="mt-8 rounded-lg bg-gray-50 border border-gray-200 p-8 text-center dark:bg-gray-900 dark:border-gray-800">
            <p className="text-gray-600 dark:text-gray-400">
              No recommendations available yet. The artwork database may need to
              be populated.
            </p>
            <p className="mt-2 text-sm text-gray-500 dark:text-gray-500">
              Run{" "}
              <code className="rounded bg-gray-200 px-2 py-1 dark:bg-gray-800">
                scripts/seed_artworks.py
              </code>{" "}
              in the backend to add sample artwork.
            </p>
          </div>
        ) : (
          <div className="mt-8 grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
            {recommendations.map((rec) => (
              <div
                key={rec.id}
                className="group overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm transition-shadow hover:shadow-lg dark:border-gray-800 dark:bg-gray-950"
              >
                {/* Image */}
                <div className="relative aspect-square overflow-hidden bg-gray-100 dark:bg-gray-900">
                  {rec.image_url ? (
                    <img
                      src={rec.image_url}
                      alt={rec.title}
                      className="h-full w-full object-cover transition-transform group-hover:scale-105"
                    />
                  ) : (
                    <div className="flex h-full w-full items-center justify-center">
                      <Palette className="h-16 w-16 text-gray-400" />
                    </div>
                  )}

                  {/* Match Score Badge */}
                  <div className="absolute left-3 top-3 rounded-full bg-purple-600 px-3 py-1 text-sm font-semibold text-white">
                    {rec.match_score.toFixed(0)}% Match
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
                    {typeof rec.price === "string" && rec.price.startsWith("$")
                      ? rec.price
                      : `$${rec.price}`}
                  </p>

                  {/* Tags */}
                  <div className="mt-4 flex flex-wrap gap-2">
                    <span className="rounded-full bg-gray-100 px-3 py-1 text-xs font-medium text-gray-700 dark:bg-gray-800 dark:text-gray-300">
                      {rec.style}
                    </span>
                    <span className="rounded-full bg-gray-100 px-3 py-1 text-xs font-medium text-gray-700 dark:bg-gray-800 dark:text-gray-300">
                      {rec.dimensions}
                    </span>
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
                      <div className="mt-3">
                        {!rec.reasoning && isEnrichingReasoning ? (
                          // Skeleton loader while AI reasoning is being generated
                          <div className="space-y-2 animate-pulse">
                            <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-full"></div>
                            <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-5/6"></div>
                            <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-4/6"></div>
                            <div className="flex items-center gap-2 mt-2 text-xs text-gray-500">
                              <Loader2 className="h-3 w-3 animate-spin" />
                              <span>AI generating reasoning...</span>
                            </div>
                          </div>
                        ) : (
                          <p className="text-sm text-gray-600 dark:text-gray-400">
                            {rec.reasoning || "No reasoning available."}
                          </p>
                        )}
                      </div>
                    )}
                  </div>

                  {/* Purchase Button */}
                  {rec.purchase_url && (
                    <div className="mt-4 border-t border-gray-200 pt-4 dark:border-gray-800">
                      <a
                        href={rec.purchase_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex w-full items-center justify-center gap-2 rounded-lg bg-gradient-to-r from-purple-600 to-pink-600 px-4 py-3 text-sm font-semibold text-white transition-all hover:from-purple-700 hover:to-pink-700 hover:shadow-lg"
                      >
                        <ShoppingCart className="h-4 w-4" />
                        Buy Now - {rec.price}
                      </a>

                      {/* Source Badge */}
                      {rec.source && (
                        <div className="mt-2 flex items-center justify-center gap-2 text-xs text-gray-600 dark:text-gray-400">
                          <Store className="h-3 w-3" />
                          <span>From {rec.source}</span>
                        </div>
                      )}
                    </div>
                  )}

                  {/* Download Button (for free images) */}
                  {rec.download_url && !rec.purchase_url && (
                    <div className="mt-4 border-t border-gray-200 pt-4 dark:border-gray-800">
                      <a
                        href={rec.download_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex w-full items-center justify-center gap-2 rounded-lg bg-green-600 px-4 py-3 text-sm font-semibold text-white transition-colors hover:bg-green-700"
                      >
                        <Download className="h-4 w-4" />
                        Free Download
                      </a>
                    </div>
                  )}

                  {/* Print-on-Demand Options */}
                  {rec.print_on_demand && rec.print_on_demand.length > 0 && (
                    <div className="mt-3">
                      <p className="text-xs font-medium text-gray-600 dark:text-gray-400 mb-2">
                        Print on Demand:
                      </p>
                      <div className="flex flex-wrap gap-2">
                        {rec.print_on_demand
                          .slice(0, 3)
                          .map((pod: any, idx: number) => (
                            <a
                              key={idx}
                              href={pod.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-xs text-purple-600 hover:text-purple-700 dark:text-purple-400 dark:hover:text-purple-300 flex items-center gap-1"
                            >
                              {pod.service}
                              <ExternalLink className="h-3 w-3" />
                            </a>
                          ))}
                      </div>
                    </div>
                  )}

                  {/* Multiple Purchase Options */}
                  {rec.purchase_options && rec.purchase_options.length > 0 && (
                    <div className="mt-3">
                      <p className="text-xs font-medium text-gray-600 dark:text-gray-400 mb-2">
                        Also available from:
                      </p>
                      {rec.purchase_options
                        .slice(0, 2)
                        .map((option: any, idx: number) => (
                          <a
                            key={idx}
                            href={option.purchase_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="flex items-center justify-between p-2 mt-1 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-900 transition-colors text-xs"
                          >
                            <div>
                              <div className="font-medium text-gray-900 dark:text-white">
                                {option.source}
                              </div>
                              <div className="text-gray-600 dark:text-gray-400">
                                {option.price}
                              </div>
                            </div>
                            <ExternalLink className="h-3 w-3 text-gray-400" />
                          </a>
                        ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Nearby Art Stores Section */}
      {nearbyStores.length > 0 && (
        <div className="mt-12">
          <div className="mb-6 text-center">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
              📍 Nearby Art Stores & Galleries
            </h2>
            <p className="text-gray-600 dark:text-gray-400">
              Find these artworks at local stores near you
            </p>
          </div>

          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {nearbyStores.map((store: any, idx: number) => (
              <div
                key={idx}
                className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm transition-shadow hover:shadow-md dark:border-gray-800 dark:bg-gray-900"
              >
                <div className="mb-3 flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-900 dark:text-white">
                      {store.name}
                    </h3>
                    <p className="mt-1 text-sm text-gray-600 dark:text-gray-400">
                      {store.address}
                    </p>
                  </div>
                  {store.is_open !== undefined && (
                    <span
                      className={`ml-2 flex-shrink-0 rounded-full px-2 py-1 text-xs font-medium ${
                        store.is_open
                          ? "bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400"
                          : "bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400"
                      }`}
                    >
                      {store.is_open ? "Open" : "Closed"}
                    </span>
                  )}
                </div>

                <div className="mb-4 flex flex-wrap gap-3 text-sm text-gray-600 dark:text-gray-400">
                  <span className="flex items-center gap-1">
                    📏 {store.distance}
                  </span>
                  {store.rating && store.rating !== "N/A" && (
                    <span className="flex items-center gap-1">
                      ⭐ {store.rating}
                    </span>
                  )}
                </div>

                <div className="flex gap-2">
                  {store.phone && store.phone !== "N/A" && (
                    <a
                      href={`tel:${store.phone}`}
                      className="flex-1 rounded-lg border border-gray-300 px-3 py-2 text-center text-sm font-medium text-gray-700 transition-colors hover:bg-gray-50 dark:border-gray-700 dark:text-gray-300 dark:hover:bg-gray-800"
                      title="Call store"
                    >
                      <Phone className="inline h-4 w-4 mr-1" />
                      Call
                    </a>
                  )}
                  {store.website && store.website !== "N/A" && (
                    <a
                      href={store.website}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex-1 rounded-lg border border-gray-300 px-3 py-2 text-center text-sm font-medium text-gray-700 transition-colors hover:bg-gray-50 dark:border-gray-700 dark:text-gray-300 dark:hover:bg-gray-800"
                      title="Visit website"
                    >
                      <Globe className="inline h-4 w-4 mr-1" />
                      Website
                    </a>
                  )}
                  {store.lat && store.lng && (
                    <button
                      onClick={() => handleGetDirections(store)}
                      className="flex-1 rounded-lg bg-blue-600 px-3 py-2 text-sm font-medium text-white transition-colors hover:bg-blue-700"
                      title="Get directions"
                    >
                      <Navigation className="inline h-4 w-4 mr-1" />
                      Directions
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Actions */}
      <div className="mt-12 flex flex-wrap justify-center gap-4">
        <Link
          href="/upload"
          className="inline-flex items-center gap-2 rounded-lg border border-gray-300 bg-white px-6 py-3 text-base font-semibold text-gray-900 transition-colors hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:hover:bg-gray-800"
        >
          <ArrowLeft className="h-4 w-4" />
          Try Another Room
        </Link>

        <Link
          href="/chat"
          className="inline-flex items-center gap-2 rounded-lg bg-purple-600 px-6 py-3 text-base font-semibold text-white transition-colors hover:bg-purple-700 dark:bg-purple-500 dark:hover:bg-purple-600"
        >
          Refine with Chat
        </Link>
      </div>

      {/* Directions Modal */}
      {showDirections && selectedStore && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
          <div className="max-h-[90vh] w-full max-w-2xl overflow-y-auto rounded-xl bg-white shadow-2xl dark:bg-gray-900">
            {/* Header */}
            <div className="sticky top-0 z-10 flex items-center justify-between border-b border-gray-200 bg-white p-6 dark:border-gray-800 dark:bg-gray-900">
              <div className="flex items-center gap-3">
                <Navigation className="h-6 w-6 text-blue-600" />
                <div>
                  <h2 className="text-xl font-bold text-gray-900 dark:text-white">
                    Directions
                  </h2>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    {selectedStore.name}
                  </p>
                </div>
              </div>
              <button
                onClick={() => setShowDirections(false)}
                className="rounded-lg p-2 text-gray-500 transition-colors hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-800"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            {/* Content */}
            <div className="p-6">
              {loadingDirections ? (
                <div className="flex flex-col items-center justify-center py-12">
                  <Loader2 className="mb-4 h-12 w-12 animate-spin text-blue-600" />
                  <p className="text-gray-600 dark:text-gray-400">
                    Loading directions...
                  </p>
                </div>
              ) : directionsData?.error ? (
                <div className="rounded-lg bg-red-50 p-4 text-red-700 dark:bg-red-900/20 dark:text-red-400">
                  <AlertCircle className="mb-2 h-6 w-6" />
                  <p>{directionsData.error}</p>
                </div>
              ) : directionsData ? (
                <div className="space-y-6">
                  {/* Store Info */}
                  <div className="rounded-lg border border-gray-200 bg-gray-50 p-4 dark:border-gray-800 dark:bg-gray-900">
                    <div className="mb-2 flex items-start justify-between">
                      <div>
                        <h3 className="font-semibold text-gray-900 dark:text-white">
                          {selectedStore.name}
                        </h3>
                        <p className="text-sm text-gray-600 dark:text-gray-400">
                          {selectedStore.address}
                        </p>
                      </div>
                      {selectedStore.is_open !== undefined && (
                        <span
                          className={`rounded-full px-3 py-1 text-xs font-medium ${
                            selectedStore.is_open
                              ? "bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400"
                              : "bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400"
                          }`}
                        >
                          {selectedStore.is_open ? "Open" : "Closed"}
                        </span>
                      )}
                    </div>
                    <div className="mt-3 flex flex-wrap gap-4 text-sm text-gray-600 dark:text-gray-400">
                      {selectedStore.phone && selectedStore.phone !== "N/A" && (
                        <a
                          href={`tel:${selectedStore.phone}`}
                          className="flex items-center gap-1 hover:text-blue-600"
                        >
                          <Phone className="h-4 w-4" />
                          {selectedStore.phone}
                        </a>
                      )}
                      {selectedStore.rating &&
                        selectedStore.rating !== "N/A" && (
                          <span className="flex items-center gap-1">
                            ⭐ {selectedStore.rating}
                          </span>
                        )}
                      {selectedStore.website &&
                        selectedStore.website !== "N/A" && (
                          <a
                            href={selectedStore.website}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="flex items-center gap-1 hover:text-blue-600"
                          >
                            <Globe className="h-4 w-4" />
                            Website
                          </a>
                        )}
                    </div>
                  </div>

                  {/* Action Buttons */}
                  <div className="flex gap-3">
                    <button
                      onClick={async () => {
                        const { openGoogleMapsDirections } = await import(
                          "@/lib/api"
                        );
                        const locationData =
                          sessionStorage.getItem("userLocation");
                        if (locationData) {
                          const userLoc = JSON.parse(locationData);
                          openGoogleMapsDirections(
                            userLoc.latitude,
                            userLoc.longitude,
                            selectedStore.lat,
                            selectedStore.lng
                          );
                        }
                      }}
                      className="flex-1 rounded-lg bg-blue-600 px-4 py-3 font-semibold text-white transition-colors hover:bg-blue-700"
                    >
                      Open in Google Maps
                    </button>
                    <button
                      onClick={() => setShowDirections(false)}
                      className="rounded-lg border border-gray-300 px-4 py-3 font-semibold text-gray-700 transition-colors hover:bg-gray-50 dark:border-gray-700 dark:text-gray-300 dark:hover:bg-gray-800"
                    >
                      Close
                    </button>
                  </div>
                </div>
              ) : null}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
