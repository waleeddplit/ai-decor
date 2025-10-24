"use client";

import { useState } from "react";
import {
  Upload,
  Image as ImageIcon,
  X,
  Loader2,
  AlertCircle,
} from "lucide-react";
import { useRouter } from "next/navigation";
import { analyzeRoom, type RoomAnalysisResponse } from "@/lib/api";

/**
 * Upload Page - Connected to Backend
 * Allows users to upload room images and get AI analysis
 */
export default function UploadPage() {
  const router = useRouter();
  const [image, setImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [description, setDescription] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [progress, setProgress] = useState<string>("");

  // Handle image file selection
  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      // Validate file size (max 10MB)
      if (file.size > 10 * 1024 * 1024) {
        setError("Image size must be less than 10MB");
        return;
      }

      // Validate file type
      if (!file.type.startsWith("image/")) {
        setError("Please upload a valid image file");
        return;
      }

      setError(null);
      setImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  // Handle drag and drop
  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const file = e.dataTransfer.files?.[0];
    if (file && file.type.startsWith("image/")) {
      // Validate file size
      if (file.size > 10 * 1024 * 1024) {
        setError("Image size must be less than 10MB");
        return;
      }

      setError(null);
      setImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  // Remove selected image
  const handleRemoveImage = () => {
    setImage(null);
    setImagePreview(null);
    setError(null);
  };

  // Submit for analysis
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!image) {
      setError("Please upload an image");
      return;
    }

    setIsAnalyzing(true);
    setError(null);
    setProgress("Uploading image...");

    try {
      // Call backend API
      setProgress("Analyzing room...");
      const analysis: RoomAnalysisResponse = await analyzeRoom(
        image,
        description
      );

      setProgress("Generating recommendations...");

      // Try to get user location (optional - doesn't block if denied)
      let userLocation = null;
      try {
        setProgress("Getting your location for nearby stores...");
        const { getUserLocation } = await import("@/lib/api");
        userLocation = await getUserLocation();
        console.log("📍 Got user location:", userLocation);
      } catch (locError) {
        console.log("Location not available (user may have denied permission)");
        // Continue without location - nearby stores just won't be shown
      }

      // Store analysis in sessionStorage for results page
      sessionStorage.setItem("roomAnalysis", JSON.stringify(analysis));
      sessionStorage.setItem("roomImage", imagePreview || "");
      sessionStorage.setItem("roomDescription", description);

      // Store user location if available
      if (userLocation) {
        sessionStorage.setItem("userLocation", JSON.stringify(userLocation));
      }

      // Navigate to results page
      setTimeout(() => {
        router.push("/results");
      }, 500);
    } catch (err) {
      console.error("Analysis error:", err);
      setError(
        err instanceof Error
          ? err.message
          : "Failed to analyze room. Please make sure the backend server is running."
      );
      setIsAnalyzing(false);
      setProgress("");
    }
  };

  return (
    <div className="container mx-auto max-w-4xl px-4 py-12">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white">
          Upload Your Room
        </h1>
        <p className="mt-4 text-lg text-gray-600 dark:text-gray-400">
          Share a photo of your space and let AI find the perfect décor
        </p>
      </div>

      {/* Error Message */}
      {error && (
        <div className="mt-6 rounded-lg bg-red-50 border border-red-200 p-4 dark:bg-red-900/20 dark:border-red-800">
          <div className="flex items-start gap-3">
            <AlertCircle className="h-5 w-5 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="text-sm font-semibold text-red-800 dark:text-red-200">
                Error
              </h3>
              <p className="mt-1 text-sm text-red-700 dark:text-red-300">
                {error}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Progress Indicator */}
      {isAnalyzing && progress && (
        <div className="mt-6 rounded-lg bg-purple-50 border border-purple-200 p-4 dark:bg-purple-900/20 dark:border-purple-800">
          <div className="flex items-center gap-3">
            <Loader2 className="h-5 w-5 text-purple-600 dark:text-purple-400 animate-spin" />
            <p className="text-sm font-medium text-purple-900 dark:text-purple-100">
              {progress}
            </p>
          </div>
        </div>
      )}

      <form onSubmit={handleSubmit} className="mt-12">
        {/* Image Upload Area */}
        <div className="rounded-xl border-2 border-dashed border-gray-300 bg-gray-50 p-8 transition-colors dark:border-gray-700 dark:bg-gray-900">
          {!imagePreview ? (
            <div
              className="flex flex-col items-center justify-center py-12"
              onDragOver={handleDragOver}
              onDrop={handleDrop}
            >
              <div className="flex h-20 w-20 items-center justify-center rounded-full bg-purple-100 dark:bg-purple-900/30">
                <Upload className="h-10 w-10 text-purple-600 dark:text-purple-400" />
              </div>

              <h3 className="mt-6 text-lg font-semibold text-gray-900 dark:text-white">
                Upload a room photo
              </h3>
              <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
                Drag and drop or click to browse
              </p>

              <label className="mt-6 cursor-pointer">
                <span className="inline-flex items-center gap-2 rounded-lg bg-purple-600 px-6 py-3 text-sm font-semibold text-white transition-colors hover:bg-purple-700 dark:bg-purple-500 dark:hover:bg-purple-600">
                  <ImageIcon className="h-5 w-5" />
                  Choose File
                </span>
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleImageChange}
                  className="hidden"
                  disabled={isAnalyzing}
                />
              </label>

              <p className="mt-4 text-xs text-gray-500 dark:text-gray-500">
                Supports: JPG, PNG, WEBP (max 10MB)
              </p>
            </div>
          ) : (
            <div className="relative">
              <button
                type="button"
                onClick={handleRemoveImage}
                disabled={isAnalyzing}
                className="absolute right-2 top-2 rounded-full bg-red-500 p-2 text-white transition-colors hover:bg-red-600 disabled:opacity-50 disabled:cursor-not-allowed z-10"
              >
                <X className="h-5 w-5" />
              </button>
              <img
                src={imagePreview}
                alt="Room preview"
                className="h-auto w-full rounded-lg object-cover"
              />
            </div>
          )}
        </div>

        {/* Text Description */}
        <div className="mt-8">
          <label
            htmlFor="description"
            className="block text-sm font-medium text-gray-900 dark:text-white"
          >
            Additional Details (Optional)
          </label>
          <p className="mt-1 text-sm text-gray-600 dark:text-gray-400">
            Describe your room style, preferences, or any specific requirements
          </p>
          <textarea
            id="description"
            rows={4}
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            disabled={isAnalyzing}
            placeholder="E.g., Modern living room with white walls, looking for abstract art in warm tones..."
            className="mt-3 w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 placeholder-gray-500 focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-500/20 disabled:opacity-50 disabled:cursor-not-allowed dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:placeholder-gray-500"
          />
        </div>

        {/* Submit Button */}
        <div className="mt-8 flex justify-center">
          <button
            type="submit"
            disabled={isAnalyzing || !image}
            className="inline-flex items-center gap-2 rounded-lg bg-purple-600 px-8 py-3 text-base font-semibold text-white transition-colors hover:bg-purple-700 disabled:cursor-not-allowed disabled:opacity-50 dark:bg-purple-500 dark:hover:bg-purple-600"
          >
            {isAnalyzing ? (
              <>
                <Loader2 className="h-5 w-5 animate-spin" />
                Analyzing Room...
              </>
            ) : (
              <>
                <Upload className="h-5 w-5" />
                Analyze & Get Recommendations
              </>
            )}
          </button>
        </div>
      </form>

      {/* Tips Section */}
      <div className="mt-16 rounded-xl bg-purple-50 p-8 dark:bg-purple-900/20">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
          💡 Tips for Best Results
        </h3>
        <ul className="mt-4 space-y-2 text-sm text-gray-700 dark:text-gray-300">
          <li>• Use well-lit photos that show the entire wall space</li>
          <li>• Include existing furniture and décor in the frame</li>
          <li>• Try to capture the room from a straight angle</li>
          <li>• Add details about your style preferences in the description</li>
        </ul>
      </div>

      {/* Backend Status Indicator */}
      <div className="mt-8 text-center">
        <p className="text-xs text-gray-500 dark:text-gray-500">
          💡 Make sure the backend server is running on http://localhost:8000
        </p>
      </div>
    </div>
  );
}
