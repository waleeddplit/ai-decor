"use client";

import { useState, useRef, useEffect } from "react";
import {
  Send,
  Bot,
  User,
  Loader2,
  Mic,
  MicOff,
  Image as ImageIcon,
  X,
  Volume2,
  VolumeX,
} from "lucide-react";
import { sendChatMessage, ChatMessage as APIMessage } from "@/lib/api";

/**
 * Chat Page
 * Interactive chat interface for conversing with AI about décor
 */

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
  recommendations?: any[]; // Artwork recommendations from API
}

const initialMessages: Message[] = [
  {
    id: "1",
    role: "assistant",
    content:
      "Hi! I'm your AI décor assistant. I can help you find the perfect wall art and décor for your space. You can describe your room, share your style preferences, or ask me anything about interior design trends!",
    timestamp: new Date(),
  },
];

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [uploadedImage, setUploadedImage] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isMounted, setIsMounted] = useState(false);
  const [isPlayingAudio, setIsPlayingAudio] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const recognitionRef = useRef<any>(null);
  const synthesisRef = useRef<SpeechSynthesis | null>(null);

  // Track when component is mounted (client-side only)
  useEffect(() => {
    setIsMounted(true);

    // Initialize speech synthesis
    if (typeof window !== "undefined" && window.speechSynthesis) {
      synthesisRef.current = window.speechSynthesis;
    }

    // Initialize speech recognition
    if (typeof window !== "undefined") {
      const SpeechRecognition =
        (window as any).SpeechRecognition ||
        (window as any).webkitSpeechRecognition;
      if (SpeechRecognition) {
        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = "en-US";

        recognition.onresult = (event: any) => {
          const transcript = event.results[0][0].transcript;
          setInput(transcript);
          setIsListening(false);
        };

        recognition.onerror = (event: any) => {
          console.error("Speech recognition error:", event.error);
          setIsListening(false);
          if (event.error === "not-allowed") {
            setError(
              "Microphone access denied. Please enable it in your browser settings."
            );
          }
        };

        recognition.onend = () => {
          setIsListening(false);
        };

        recognitionRef.current = recognition;
      }
    }
  }, []);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Handle sending messages
  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input.trim(),
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    const currentInput = input.trim();
    setInput("");
    setIsLoading(true);
    setError(null);

    try {
      // Get context from previous room analysis if available
      const roomAnalysisStr = sessionStorage.getItem("roomAnalysis");
      let context = undefined;

      if (roomAnalysisStr) {
        try {
          const roomAnalysis = JSON.parse(roomAnalysisStr);
          context = {
            style: roomAnalysis.style,
            style_vector: roomAnalysis.style_vector,
            colors: roomAnalysis.palette?.map((c: any) => c.hex),
          };
        } catch (e) {
          console.error("Failed to parse room analysis:", e);
        }
      }

      // Convert image to base64 if present
      let imageBase64 = undefined;
      if (uploadedImage) {
        imageBase64 = await fileToBase64(uploadedImage);
      }

      // Call backend API
      const response = await sendChatMessage({
        message: currentInput,
        conversation_id: conversationId || undefined,
        image: imageBase64,
        context,
      });

      // Update conversation ID
      if (!conversationId) {
        setConversationId(response.conversation_id);
      }

      // Add assistant response with recommendations
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: response.message,
        timestamp: new Date(),
        recommendations: response.recommendations || undefined,
      };

      setMessages((prev) => [...prev, assistantMessage]);

      // Update suggestions
      if (response.suggestions) {
        setSuggestions(response.suggestions);
      }

      // Log if recommendations were received
      if (response.recommendations && response.recommendations.length > 0) {
        console.log(
          `✅ Received ${response.recommendations.length} artwork recommendations`
        );
      }

      // Clear uploaded image after sending
      if (uploadedImage) {
        setUploadedImage(null);
        setImagePreview(null);
      }
    } catch (err) {
      console.error("Chat error:", err);
      setError(
        err instanceof Error
          ? err.message
          : "Failed to send message. Please check your connection."
      );

      // Add error message
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content:
          "I'm sorry, I'm having trouble connecting right now. Please try again in a moment.",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      inputRef.current?.focus();
    }
  };

  // Convert file to base64
  const fileToBase64 = (file: File): Promise<string> => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => {
        const result = reader.result as string;
        // Remove data:image/...;base64, prefix
        const base64 = result.split(",")[1];
        resolve(base64);
      };
      reader.onerror = (error) => reject(error);
    });
  };

  // Handle image upload
  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Validate file type
    if (!file.type.startsWith("image/")) {
      setError("Please upload an image file");
      return;
    }

    // Validate file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
      setError("Image size must be less than 5MB");
      return;
    }

    setUploadedImage(file);

    // Create preview
    const reader = new FileReader();
    reader.onload = (e) => {
      setImagePreview(e.target?.result as string);
    };
    reader.readAsDataURL(file);
  };

  // Remove uploaded image
  const removeImage = () => {
    setUploadedImage(null);
    setImagePreview(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  // Handle suggestion click
  const handleSuggestionClick = (suggestion: string) => {
    setInput(suggestion);
    inputRef.current?.focus();
  };

  // Handle voice input (Speech-to-Text)
  const toggleVoiceInput = () => {
    if (!recognitionRef.current) {
      setError(
        "Speech recognition is not supported in your browser. Try Chrome or Edge."
      );
      return;
    }

    if (isListening) {
      // Stop listening
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      // Start listening
      setError(null);
      try {
        recognitionRef.current.start();
        setIsListening(true);
      } catch (error) {
        console.error("Failed to start recognition:", error);
        setError("Failed to start microphone. Please try again.");
        setIsListening(false);
      }
    }
  };

  // Handle text-to-speech for AI responses
  const speakMessage = (text: string, messageId: string) => {
    if (!synthesisRef.current) {
      setError("Text-to-speech is not supported in your browser.");
      return;
    }

    // Stop any currently playing speech
    if (isPlayingAudio) {
      synthesisRef.current.cancel();
      setIsPlayingAudio(null);
      return;
    }

    // Create speech utterance
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.9; // Slightly slower for clarity
    utterance.pitch = 1.0;
    utterance.volume = 1.0;

    utterance.onstart = () => {
      setIsPlayingAudio(messageId);
    };

    utterance.onend = () => {
      setIsPlayingAudio(null);
    };

    utterance.onerror = () => {
      setIsPlayingAudio(null);
      setError("Failed to play audio. Please try again.");
    };

    // Speak
    synthesisRef.current.speak(utterance);
  };

  // Handle Enter key
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex h-[calc(100vh-4rem)] flex-col">
      <div className="container mx-auto flex h-full max-w-4xl flex-col px-4 py-6">
        {/* Header */}
        <div className="border-b border-gray-200 pb-4 dark:border-gray-800">
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
            Chat with AI Designer
          </h1>
          <p className="mt-1 text-sm text-gray-600 dark:text-gray-400">
            Get personalized décor advice and recommendations
          </p>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto py-6">
          <div className="space-y-6">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex gap-4 ${
                  message.role === "user" ? "justify-end" : "justify-start"
                }`}
              >
                {/* Avatar */}
                {message.role === "assistant" && (
                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-purple-100 dark:bg-purple-900/30">
                    <Bot className="h-5 w-5 text-purple-600 dark:text-purple-400" />
                  </div>
                )}

                {/* Message Bubble */}
                <div
                  className={`max-w-[80%] ${
                    message.recommendations &&
                    message.recommendations.length > 0
                      ? "max-w-full"
                      : ""
                  }`}
                >
                  <div
                    className={`rounded-2xl px-4 py-3 ${
                      message.role === "user"
                        ? "bg-purple-600 text-white dark:bg-purple-500"
                        : "bg-gray-100 text-gray-900 dark:bg-gray-800 dark:text-white"
                    }`}
                  >
                    <div className="flex items-start justify-between gap-2">
                      <p className="flex-1 text-sm leading-relaxed">
                        {message.content}
                      </p>
                      {/* Text-to-Speech button for assistant messages */}
                      {message.role === "assistant" && (
                        <button
                          onClick={() =>
                            speakMessage(message.content, message.id)
                          }
                          className="flex-shrink-0 rounded-lg p-1 transition-colors hover:bg-gray-200 dark:hover:bg-gray-700"
                          title={
                            isPlayingAudio === message.id ? "Stop" : "Listen"
                          }
                        >
                          {isPlayingAudio === message.id ? (
                            <VolumeX className="h-4 w-4 text-purple-600 dark:text-purple-400" />
                          ) : (
                            <Volume2 className="h-4 w-4 text-gray-600 dark:text-gray-400" />
                          )}
                        </button>
                      )}
                    </div>
                    {isMounted && (
                      <p
                        className={`mt-2 text-xs ${
                          message.role === "user"
                            ? "text-purple-200 dark:text-purple-300"
                            : "text-gray-500 dark:text-gray-400"
                        }`}
                      >
                        {message.timestamp.toLocaleTimeString([], {
                          hour: "2-digit",
                          minute: "2-digit",
                        })}
                      </p>
                    )}
                  </div>

                  {/* Artwork Recommendations */}
                  {message.recommendations &&
                    message.recommendations.length > 0 && (
                      <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                        {message.recommendations.map(
                          (rec: any, idx: number) => (
                            <div
                              key={idx}
                              className="overflow-hidden rounded-lg border border-gray-200 bg-white shadow-sm transition-shadow hover:shadow-md dark:border-gray-700 dark:bg-gray-900"
                            >
                              <img
                                src={rec.image_url}
                                alt={rec.title}
                                className="h-48 w-full object-cover"
                              />
                              <div className="p-4">
                                <h4 className="font-semibold text-gray-900 dark:text-white">
                                  {rec.title}
                                </h4>
                                <p className="text-sm text-gray-600 dark:text-gray-400">
                                  {rec.artist}
                                </p>
                                <p className="mt-2 text-lg font-bold text-purple-600 dark:text-purple-400">
                                  {rec.price}
                                </p>
                                <div className="mt-2 flex items-center gap-2">
                                  <span className="text-xs text-gray-500 dark:text-gray-400">
                                    {Math.round(rec.match_score)}% match
                                  </span>
                                  {rec.source && (
                                    <span className="text-xs text-gray-500 dark:text-gray-400">
                                      • {rec.source}
                                    </span>
                                  )}
                                </div>
                                {rec.purchase_url && (
                                  <a
                                    href={rec.purchase_url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="mt-3 block w-full rounded-lg bg-purple-600 px-4 py-2 text-center text-sm font-medium text-white transition-colors hover:bg-purple-700"
                                  >
                                    Buy Now
                                  </a>
                                )}
                                {rec.download_url && !rec.purchase_url && (
                                  <a
                                    href={rec.download_url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="mt-3 block w-full rounded-lg border border-purple-600 px-4 py-2 text-center text-sm font-medium text-purple-600 transition-colors hover:bg-purple-50 dark:hover:bg-purple-900/20"
                                  >
                                    Download Free
                                  </a>
                                )}
                              </div>
                            </div>
                          )
                        )}
                      </div>
                    )}
                </div>

                {/* User Avatar */}
                {message.role === "user" && (
                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-gray-200 dark:bg-gray-700">
                    <User className="h-5 w-5 text-gray-600 dark:text-gray-300" />
                  </div>
                )}
              </div>
            ))}

            {/* Loading Indicator */}
            {isLoading && (
              <div className="flex gap-4">
                <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-purple-100 dark:bg-purple-900/30">
                  <Bot className="h-5 w-5 text-purple-600 dark:text-purple-400" />
                </div>
                <div className="flex items-center gap-2 rounded-2xl bg-gray-100 px-4 py-3 dark:bg-gray-800">
                  <Loader2 className="h-4 w-4 animate-spin text-gray-600 dark:text-gray-400" />
                  <span className="text-sm text-gray-600 dark:text-gray-400">
                    Thinking...
                  </span>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-4 rounded-lg bg-red-50 p-3 text-sm text-red-600 dark:bg-red-900/20 dark:text-red-400">
            {error}
          </div>
        )}

        {/* Suggestions */}
        {suggestions.length > 0 && !isLoading && (
          <div className="mb-4">
            <p className="mb-2 text-xs font-medium text-gray-600 dark:text-gray-400">
              Suggested questions:
            </p>
            <div className="flex flex-wrap gap-2">
              {suggestions.map((suggestion, idx) => (
                <button
                  key={idx}
                  onClick={() => handleSuggestionClick(suggestion)}
                  className="rounded-full border border-gray-300 bg-white px-3 py-1.5 text-sm text-gray-700 transition-colors hover:border-purple-500 hover:bg-purple-50 hover:text-purple-700 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-300 dark:hover:border-purple-500 dark:hover:bg-purple-900/30 dark:hover:text-purple-300"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Input Area */}
        <div className="border-t border-gray-200 pt-4 dark:border-gray-800">
          {/* Image Preview */}
          {imagePreview && (
            <div className="mb-3 relative inline-block">
              <img
                src={imagePreview}
                alt="Upload preview"
                className="h-20 w-20 rounded-lg object-cover"
              />
              <button
                onClick={removeImage}
                className="absolute -right-2 -top-2 rounded-full bg-red-500 p-1 text-white hover:bg-red-600"
              >
                <X className="h-3 w-3" />
              </button>
            </div>
          )}

          <div className="flex gap-3">
            {/* Image Upload Button */}
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleImageUpload}
              className="hidden"
            />
            <button
              onClick={() => fileInputRef.current?.click()}
              className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl border border-gray-300 bg-white text-gray-600 transition-colors hover:border-purple-500 hover:bg-purple-50 hover:text-purple-600 dark:border-gray-700 dark:bg-gray-800 dark:text-gray-400 dark:hover:border-purple-500 dark:hover:bg-purple-900/30 dark:hover:text-purple-400"
              aria-label="Upload image"
              title="Upload room image"
            >
              <ImageIcon className="h-5 w-5" />
            </button>

            {/* Text Input */}
            <div className="relative flex-1">
              <textarea
                ref={inputRef}
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask about décor styles, colors, or upload a room photo..."
                rows={1}
                className="w-full resize-none rounded-xl border border-gray-300 bg-white px-4 py-3 pr-24 text-sm text-gray-900 placeholder-gray-500 focus:border-purple-500 focus:outline-none focus:ring-2 focus:ring-purple-500/20 dark:border-gray-700 dark:bg-gray-900 dark:text-white dark:placeholder-gray-500"
                style={{ minHeight: "48px", maxHeight: "120px" }}
              />

              {/* Action Buttons */}
              <div className="absolute bottom-2 right-2 flex gap-1">
                {/* Voice Input Button */}
                <button
                  onClick={toggleVoiceInput}
                  className={`rounded-lg p-2 transition-colors ${
                    isListening
                      ? "bg-red-500 text-white hover:bg-red-600"
                      : "bg-gray-100 text-gray-600 hover:bg-gray-200 dark:bg-gray-800 dark:text-gray-400 dark:hover:bg-gray-700"
                  }`}
                  aria-label="Voice input"
                  title="Voice input (coming soon)"
                >
                  {isListening ? (
                    <MicOff className="h-4 w-4" />
                  ) : (
                    <Mic className="h-4 w-4" />
                  )}
                </button>
              </div>
            </div>

            {/* Send Button */}
            <button
              onClick={handleSend}
              disabled={(!input.trim() && !uploadedImage) || isLoading}
              className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-purple-600 text-white transition-colors hover:bg-purple-700 disabled:cursor-not-allowed disabled:opacity-50 dark:bg-purple-500 dark:hover:bg-purple-600"
              aria-label="Send message"
            >
              {isLoading ? (
                <Loader2 className="h-5 w-5 animate-spin" />
              ) : (
                <Send className="h-5 w-5" />
              )}
            </button>
          </div>

          <p className="mt-2 text-center text-xs text-gray-500 dark:text-gray-500">
            Press Enter to send, Shift+Enter for new line
          </p>
        </div>
      </div>
    </div>
  );
}
