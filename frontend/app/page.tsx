"use client";

import { useState, useEffect } from "react";
import SwipeCard from "../components/SwipeCard";
import { AnimatePresence } from "framer-motion";
import { RefreshCw } from "lucide-react";

import axios from "axios";

// API Base URL
const API_URL = "http://localhost:8000";
const USER_ID = 1; // Hardcoded for now until Auth is implemented

export default function Home() {
  const [tweets, setTweets] = useState<any[]>([]);
  const [history, setHistory] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchFeed = async () => {
    setLoading(true);
    try {
      // For now, we might need to trigger ingestion if feed is empty
      // Or just get a random sample if ranking isn't ready
      // This endpoint needs to exist in backend
      const res = await axios.get(`${API_URL}/feed/${USER_ID}`);
      setTweets(res.data.feed || []);
    } catch (error) {
      console.error("Error fetching feed:", error);
      // Fallback to empty or error state
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFeed();
  }, []);

  const handleSwipe = async (direction: "left" | "right") => {
    if (tweets.length === 0) return;

    const currentTweet = tweets[0];
    const action = direction === "right" ? "LIKE" : "DISCARD";

    // Optimistic UI update
    setTweets((prev) => prev.slice(1));
    setHistory((prev) => [...prev, `Swiped ${direction} on ${currentTweet.id}`]);

    try {
      await axios.post(`${API_URL}/swipe`, {
        user_id: USER_ID,
        tweet_id: currentTweet.id,
        action: action,
      });
    } catch (error) {
      console.error("Error recording swipe:", error);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gray-50 p-4 overflow-hidden">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm lg:flex absolute top-4 px-8">
        <p className="fixed left-0 top-0 flex w-full justify-center border-b border-gray-300 bg-gradient-to-b from-zinc-200 pb-6 pt-8 backdrop-blur-2xl lg:static lg:w-auto lg:rounded-xl lg:border lg:bg-gray-200 lg:p-4">
          Tinder for X
        </p>
        <div className="fixed bottom-0 left-0 flex h-48 w-full items-end justify-center bg-gradient-to-t from-white via-white lg:static lg:h-auto lg:w-auto lg:bg-none">
          <button
            onClick={fetchFeed}
            className="flex items-center gap-2 pointer-events-auto lg:p-0"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} /> Refresh Feed
          </button>
        </div>
      </div>

      <div className="relative w-full max-w-md h-[60vh] flex items-center justify-center">
        <AnimatePresence>
          {tweets.map((tweet, index) => (
            index === 0 ? (
              <SwipeCard key={tweet.id} tweet={tweet} onSwipe={handleSwipe} />
            ) : null
          ))}
        </AnimatePresence>

        {tweets.length === 0 && !loading && (
          <div className="text-center text-gray-500">
            <p className="text-xl mb-4">No more tweets!</p>
            <button
              onClick={fetchFeed}
              className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
            >
              Refresh Feed
            </button>
          </div>
        )}

        {loading && tweets.length === 0 && (
          <div className="text-center text-gray-500">
            <RefreshCw className="w-8 h-8 animate-spin mx-auto mb-4" />
            <p>Loading tweets...</p>
          </div>
        )}
      </div>

      <div className="absolute bottom-8 text-xs text-gray-400">
        <p>Swipe Right to Like, Left to Discard</p>
      </div>
    </main>
  );
}
