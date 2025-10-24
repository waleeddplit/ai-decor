"use client";

import { useState } from "react";
import { Upload, Image as ImageIcon, X, Loader2 } from "lucide-react";
import { useRouter } from "next/navigation";

/**
 * Upload Page
 * Allows users to upload room images and provide text descriptions
 */
export default function UploadPage() {
  const router = useRouter();
  const [image, setImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [description, setDescription] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  // Handle image file selection
  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
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
  };

  // Submit for analysis
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!image && !description.trim()) {
      alert("Please provide either an image or description");
      return;
    }

    setIsAnalyzing(true);

    // TODO: Connect to backend API
    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 2000));

    // Navigate to results page with mock data
    router.push("/results");
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
                className="absolute right-2 top-2 rounded-full bg-red-500 p-2 text-white transition-colors hover:bg-red-600"
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
            placeholder="E.g., Modern living room with white walls, looking for abstract art in warm tones..."
            className="mt-3 w-full rounded-lg border border-gray-300 bg-white px-4 py-3 text-gray-900 placeholder-gray-500 focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-500/20 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:placeholder-gray-500"
          />
        </div>

        {/* Submit Button */}
        <div className="mt-8 flex justify-center">
          <button
            type="submit"
            disabled={isAnalyzing || (!image && !description.trim())}
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
    </div>
  );
}
