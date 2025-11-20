"use client";

import { motion, useMotionValue, useTransform, PanInfo } from "framer-motion";
import { useState } from "react";
import { X, Heart } from "lucide-react";

interface Tweet {
  id: string;
  text: string;
  author_id: string;
  created_at: string;
}

interface SwipeCardProps {
  tweet: Tweet;
  onSwipe: (direction: "left" | "right") => void;
}

export default function SwipeCard({ tweet, onSwipe }: SwipeCardProps) {
  const x = useMotionValue(0);
  const rotate = useTransform(x, [-200, 200], [-25, 25]);
  const opacity = useTransform(x, [-200, -100, 0, 100, 200], [0, 1, 1, 1, 0]);
  
  const background = useTransform(
    x,
    [-200, -100, 0, 100, 200],
    [
      "rgba(239, 68, 68, 0.2)",
      "rgba(239, 68, 68, 0.1)",
      "rgba(255, 255, 255, 1)",
      "rgba(34, 197, 94, 0.1)",
      "rgba(34, 197, 94, 0.2)",
    ]
  );

  const handleDragEnd = (event: any, info: PanInfo) => {
    if (info.offset.x > 100) {
      onSwipe("right");
    } else if (info.offset.x < -100) {
      onSwipe("left");
    }
  };

  return (
    <motion.div
      style={{ x, rotate, opacity, background }}
      drag="x"
      dragConstraints={{ left: 0, right: 0 }}
      onDragEnd={handleDragEnd}
      className="absolute w-full max-w-md h-[60vh] bg-white rounded-3xl shadow-xl border border-gray-200 p-8 flex flex-col justify-between cursor-grab active:cursor-grabbing overflow-hidden"
      whileTap={{ scale: 1.05 }}
    >
      <div className="flex items-center space-x-3 mb-4">
        <div className="w-10 h-10 bg-gray-200 rounded-full" />
        <div>
          <h3 className="font-bold text-gray-900">User {tweet.author_id}</h3>
          <p className="text-sm text-gray-500">{new Date(tweet.created_at).toLocaleDateString()}</p>
        </div>
      </div>
      
      <p className="text-xl text-gray-800 font-medium leading-relaxed">
        {tweet.text}
      </p>

      <div className="flex justify-between items-center mt-8">
        <div className="flex items-center text-red-500 opacity-50">
          <X className="w-6 h-6 mr-2" />
          <span className="font-bold">DISCARD</span>
        </div>
        <div className="flex items-center text-green-500 opacity-50">
          <span className="font-bold mr-2">LIKE</span>
          <Heart className="w-6 h-6" />
        </div>
      </div>
    </motion.div>
  );
}
