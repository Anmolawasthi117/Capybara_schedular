// src/components/About.jsx
import React from "react";
import { motion } from "framer-motion";
import { CheckCircle } from "lucide-react";

const points = [
  "AI-driven timetable maker powered by Genetic Algorithms (GA).",
  "Automatically generates conflict-free, optimized timetables.",
  "Designed for ITEP, B.Ed., M.Ed., and FYUP programs.",
  "Incorporates course structures, credit hours, and constraints.",
  "Ensures compliance with academic policies.",
  "Meets the requirements of both faculty and students.",
];

const About = () => {
  return (
    <section className="py-20 px-6 bg-white text-gray-800">
      <div className="max-w-5xl mx-auto text-center">
        {/* Heading */}
        <motion.h2
          className="text-3xl md:text-4xl font-bold mb-6"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
        >
          About <span className="text-blue-600">PLANIT</span>
        </motion.h2>

        {/* Summary */}
        <motion.p
          className="text-lg text-gray-600 max-w-3xl mx-auto mb-12 leading-relaxed"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          viewport={{ once: true }}
        >
          PLANIT is your AI-driven scheduling partner — built with advanced
          Genetic Algorithms to generate conflict-free, policy-compliant,
          optimized timetables tailored for modern academic programs.
        </motion.p>

        {/* Points */}
        <div className="grid md:grid-cols-2 gap-6 text-left">
          {points.map((point, i) => (
            <motion.div
              key={i}
              className="flex items-start gap-3"
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: i * 0.1 }}
              viewport={{ once: true }}
            >
              <CheckCircle className="w-6 h-6 text-blue-600 shrink-0 mt-1" />
              <p className="text-gray-700">{point}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default About;
