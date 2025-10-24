import Link from "next/link";
import {
  ArrowRight,
  Upload,
  MessageSquare,
  Sparkles,
  TrendingUp,
  MapPin,
} from "lucide-react";

/**
 * Landing Page
 * Welcome page showcasing Art.Decor.AI features
 */
export default function Home() {
  const features = [
    {
      icon: <Sparkles className="h-8 w-8" />,
      title: "AI-Powered Analysis",
      description:
        "Advanced computer vision detects room style, colors, and lighting to find perfect matches",
    },
    {
      icon: <TrendingUp className="h-8 w-8" />,
      title: "Trend Intelligence",
      description:
        "Stay current with real-time trending décor styles and seasonal design insights",
    },
    {
      icon: <MapPin className="h-8 w-8" />,
      title: "Local Store Finder",
      description:
        "Discover nearby galleries and décor stores with your recommended items in stock",
    },
  ];

  return (
    <div className="flex flex-col">
      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="flex flex-col items-center text-center">
          <div className="inline-block rounded-full bg-purple-100 px-4 py-2 text-sm font-medium text-purple-700 dark:bg-purple-900/30 dark:text-purple-300">
            AI-Powered Interior Design
          </div>

          <h1 className="mt-6 max-w-4xl text-5xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-6xl">
            Transform Your Space with{" "}
            <span className="bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
              AI-Curated Décor
            </span>
          </h1>

          <p className="mt-6 max-w-2xl text-lg text-gray-600 dark:text-gray-400">
            Upload a photo of your room and let our AI find wall art and décor
            that perfectly matches your style, lighting, and color palette. Get
            personalized recommendations backed by trend intelligence.
          </p>

          <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
            <Link
              href="/upload"
              className="group inline-flex items-center gap-2 rounded-lg bg-purple-600 px-6 py-3 text-base font-semibold text-white transition-all hover:bg-purple-700 hover:shadow-lg dark:bg-purple-500 dark:hover:bg-purple-600"
            >
              <Upload className="h-5 w-5" />
              Upload Room Photo
              <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
            </Link>

            <Link
              href="/chat"
              className="inline-flex items-center gap-2 rounded-lg border border-gray-300 bg-white px-6 py-3 text-base font-semibold text-gray-900 transition-all hover:bg-gray-50 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:hover:bg-gray-800"
            >
              <MessageSquare className="h-5 w-5" />
              Start Chatting
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="border-t border-gray-200 bg-gray-50 py-20 dark:border-gray-800 dark:bg-gray-900">
        <div className="container mx-auto px-4">
          <h2 className="text-center text-3xl font-bold text-gray-900 dark:text-white">
            Intelligent Décor Discovery
          </h2>
          <p className="mt-4 text-center text-gray-600 dark:text-gray-400">
            Powered by cutting-edge AI models and real-time data
          </p>

          <div className="mt-16 grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
            {features.map((feature, index) => (
              <div
                key={index}
                className="rounded-xl border border-gray-200 bg-white p-8 shadow-sm transition-shadow hover:shadow-md dark:border-gray-800 dark:bg-gray-950"
              >
                <div className="flex h-16 w-16 items-center justify-center rounded-lg bg-purple-100 text-purple-600 dark:bg-purple-900/30 dark:text-purple-400">
                  {feature.icon}
                </div>
                <h3 className="mt-6 text-xl font-semibold text-gray-900 dark:text-white">
                  {feature.title}
                </h3>
                <p className="mt-3 text-gray-600 dark:text-gray-400">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="container mx-auto px-4 py-20">
        <h2 className="text-center text-3xl font-bold text-gray-900 dark:text-white">
          How It Works
        </h2>

        <div className="mt-16 grid gap-8 md:grid-cols-4">
          {[
            { step: "1", title: "Upload", desc: "Share a photo of your room" },
            { step: "2", title: "Analyze", desc: "AI detects style & colors" },
            {
              step: "3",
              title: "Discover",
              desc: "Get curated recommendations",
            },
            {
              step: "4",
              title: "Purchase",
              desc: "Find local stores near you",
            },
          ].map((item) => (
            <div
              key={item.step}
              className="flex flex-col items-center text-center"
            >
              <div className="flex h-12 w-12 items-center justify-center rounded-full bg-purple-600 text-xl font-bold text-white dark:bg-purple-500">
                {item.step}
              </div>
              <h3 className="mt-4 text-lg font-semibold text-gray-900 dark:text-white">
                {item.title}
              </h3>
              <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
                {item.desc}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA Section */}
      <section className="border-t border-gray-200 bg-gradient-to-br from-purple-600 to-pink-600 py-20 dark:border-gray-800">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-4xl font-bold text-white">
            Ready to Transform Your Space?
          </h2>
          <p className="mt-4 text-lg text-purple-100">
            Join thousands discovering their perfect décor with AI
          </p>
          <Link
            href="/upload"
            className="mt-8 inline-flex items-center gap-2 rounded-lg bg-white px-8 py-4 text-lg font-semibold text-purple-600 transition-all hover:shadow-xl"
          >
            Get Started Now
            <ArrowRight className="h-5 w-5" />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-gray-200 bg-white py-8 dark:border-gray-800 dark:bg-gray-950">
        <div className="container mx-auto px-4 text-center text-sm text-gray-600 dark:text-gray-400">
          <p>© 2025 Art.Decor.AI. Built with AI for creative spaces.</p>
        </div>
      </footer>
    </div>
  );
}
