// src/components/Hero.jsx
import React from "react";
import { motion } from "framer-motion";

const Hero = () => {
  return (
    <section className="relative flex flex-col items-center justify-center text-center py-24 px-6 bg-gradient-to-b from-blue-600 via-blue-500 to-blue-400 text-white overflow-hidden">
      {/* Background glow */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,rgba(255,255,255,0.15),transparent)] pointer-events-none"></div>

      {/* Title */}
      <motion.h1
        className="text-5xl md:text-6xl font-extrabold mb-6 drop-shadow-lg"
        initial={{ opacity: 0, y: -40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: "easeOut" }}
      >
        Schedulify
      </motion.h1>

      {/* Tagline */}
      <motion.p
        className="text-lg md:text-2xl max-w-2xl mb-8 opacity-90 leading-relaxed"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.9, delay: 0.2, ease: "easeOut" }}
      >
        Smarter schedules. Zero conflicts. Maximum productivity.
      </motion.p>

      {/* CTA buttons */}
      <motion.div
        className="flex gap-4"
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.7, delay: 0.4, ease: "easeOut" }}
      >
        <button className="px-6 py-3 bg-white text-blue-600 rounded-lg font-semibold hover:bg-gray-100 transition shadow-md">
          Get Started
        </button>
        <button className="px-6 py-3 bg-blue-800 rounded-lg font-semibold hover:bg-blue-900 transition shadow-md">
          Learn More
        </button>
      </motion.div>

      {/* Animated floating shapes for extra vibe */}
      <motion.div
        className="absolute top-10 left-10 w-16 h-16 bg-white/10 rounded-full"
        animate={{ y: [0, -20, 0] }}
        transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
      />
      <motion.div
        className="absolute bottom-20 right-20 w-24 h-24 bg-white/10 rounded-full"
        animate={{ y: [0, 30, 0] }}
        transition={{ duration: 6, repeat: Infinity, ease: "easeInOut" }}
      />
    </section>
  );
};

export default Hero;
