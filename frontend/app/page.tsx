"use client";

import { useState, useEffect } from "react";
import SwipeCard from "../components/SwipeCard";
import { AnimatePresence } from "framer-motion";
import { RefreshCw } from "lucide-react";

// Mock data for initial testing
const MOCK_TWEETS = [
  {
    id: "1",
    text: "Just built a transformer from scratch. The attention mechanism is fascinating! #AI #DeepLearning",
    author_id: "user1",
    created_at: new Date().toISOString(),
  },
  {
    id: "2",
    text: "Why is Kubernetes so complicated? I just want to deploy my container! 😭 #DevOps",
    author_id: "user2",
    created_at: new Date().toISOString(),
  },
  {
    id: "3",
    text: "Rust is the future of systems programming. Memory safety without garbage collection is a game changer.",
    author_id: "user3",
    created_at: new Date().toISOString(),
  },
];

export default function Home() {
  const [tweets, setTweets] = useState(MOCK_TWEETS);
  const [history, setHistory] = useState<string[]>([]);

  const handleSwipe = (direction: "left" | "right") => {
    if (tweets.length === 0) return;

    const currentTweet = tweets[0];
    console.log(`Swiped ${direction} on tweet ${currentTweet.id}`);

    // TODO: Send to backend
    // await axios.post('http://localhost:8000/swipe', { 
    //   user_id: 1, 
    //   tweet_id: currentTweet.id, 
    //   action: direction === 'right' ? 'LIKE' : 'DISCARD' 
    // });

    setHistory((prev) => [...prev, `Swiped ${direction} on ${currentTweet.id}`]);
    setTweets((prev) => prev.slice(1));
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gray-50 p-4 overflow-hidden">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm lg:flex absolute top-4 px-8">
        <p className="fixed left-0 top-0 flex w-full justify-center border-b border-gray-300 bg-gradient-to-b from-zinc-200 pb-6 pt-8 backdrop-blur-2xl lg:static lg:w-auto lg:rounded-xl lg:border lg:bg-gray-200 lg:p-4">
          Tinder for X
        </p>
        <div className="fixed bottom-0 left-0 flex h-48 w-full items-end justify-center bg-gradient-to-t from-white via-white lg:static lg:h-auto lg:w-auto lg:bg-none">
          <button
            onClick={() => setTweets(MOCK_TWEETS)}
            className="flex items-center gap-2 pointer-events-auto lg:p-0"
          >
            <RefreshCw className="w-4 h-4" /> Reset Feed
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

        {tweets.length === 0 && (
          <div className="text-center text-gray-500">
            <p className="text-xl mb-4">No more tweets!</p>
            <button
              onClick={() => setTweets(MOCK_TWEETS)}
              className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
            >
              Refresh Feed
            </button>
          </div>
        )}
      </div>

      <div className="absolute bottom-8 text-xs text-gray-400">
        <p>Swipe Right to Like, Left to Discard</p>
      </div>
    </main>
  );
}
