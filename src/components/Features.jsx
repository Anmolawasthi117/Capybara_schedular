// src/components/Features.jsx
import React from "react";
import { motion } from "framer-motion";
import {
  Database,
  Ban,
  CalendarDays,
  FileDown,
  BookOpen,
  Link,
} from "lucide-react";

const features = [
  {
    title: "Database Input",
    desc: "Collects input directly from faculty with ease.",
    icon: <Database className="w-8 h-8 text-blue-600" />,
  },
  {
    title: "Clash Avoidance",
    desc: "Avoid faculty, classroom, and time slot conflicts effectively.",
    icon: <Ban className="w-8 h-8 text-blue-600" />,
  },
  {
    title: "Timetable Generation",
    desc: "Automatically generates semester-wise timetables for all programs.",
    icon: <CalendarDays className="w-8 h-8 text-blue-600" />,
  },
  {
    title: "Export Options",
    desc: "Easily export timetables in PDF and Excel formats.",
    icon: <FileDown className="w-8 h-8 text-blue-600" />,
  },
  {
    title: "Curriculum Support",
    desc: "Seamlessly adapts to new courses and NEP updates.",
    icon: <BookOpen className="w-8 h-8 text-blue-600" />,
  },
  {
    title: "System Integration",
    desc: "Integrates smoothly with academic management systems.",
    icon: <Link className="w-8 h-8 text-blue-600" />,
  },
];

const Features = () => {
  return (
    <section className="py-20 px-6 bg-gray-50">
      <div className="max-w-6xl mx-auto text-center">
        {/* Section Heading */}
        <motion.h2
          className="text-3xl md:text-4xl font-bold mb-6"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
        >
          Features that make scheduling effortless
        </motion.h2>

        <motion.p
          className="text-lg text-gray-600 mb-12 max-w-3xl mx-auto"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          viewport={{ once: true }}
        >
          PLANIT takes care of every detail — from faculty inputs to clash
          management, generation, and export.
        </motion.p>

        {/* Features Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((f, i) => (
            <motion.div
              key={i}
              className="p-6 bg-white rounded-xl shadow-md hover:shadow-lg transition flex flex-col items-center text-center"
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.5, delay: i * 0.1 }}
              viewport={{ once: true }}
            >
              <div className="mb-4">{f.icon}</div>
              <h3 className="text-xl font-semibold mb-2">{f.title}</h3>
              <p className="text-gray-600 text-sm">{f.desc}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features;
