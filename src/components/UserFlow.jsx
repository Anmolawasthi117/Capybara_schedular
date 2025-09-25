// src/components/UserFlow.jsx
import React from "react";
import { motion } from "framer-motion";
import {
  LogIn,
  LayoutDashboard,
  Upload,
  FileCheck,
  CalendarDays,
  FileDown,
  ArrowRight,
} from "lucide-react";

const steps = [
  {
    title: "Login",
    desc: "Sign in with your admin ID to access the dashboard.",
    icon: <LogIn className="w-8 h-8 text-blue-600" />,
  },
  {
    title: "Admin Panel",
    desc: "Access the control panel and choose your program.",
    icon: <LayoutDashboard className="w-8 h-8 text-blue-600" />,
  },
  {
    title: "Upload Data",
    desc: "Upload faculty and student details seamlessly.",
    icon: <Upload className="w-8 h-8 text-blue-600" />,
  },
  {
    title: "Review & Generate",
    desc: "Review the details and generate your timetable.",
    icon: <CalendarDays className="w-8 h-8 text-blue-600" />,
  },
  {
    title: "Export",
    desc: "Download the timetable in PDF or Excel formats.",
    icon: <FileDown className="w-8 h-8 text-blue-600" />,
  },
];

const UserFlow = () => {
  return (
    <section className="py-20 px-6 bg-white">
      <div className="max-w-6xl mx-auto text-center">
        {/* Heading */}
        <motion.h2
          className="text-3xl md:text-4xl font-bold mb-6"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
        >
          How <span className="text-blue-600">Schedulify</span> Works
        </motion.h2>

        <motion.p
          className="text-lg text-gray-600 mb-12 max-w-3xl mx-auto"
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          viewport={{ once: true }}
        >
          A simple, streamlined process that takes you from login to timetable
          in just a few clicks.
        </motion.p>

        {/* Steps */}
        <div className="flex flex-col md:flex-row items-center justify-center gap-8">
          {steps.map((step, i) => (
            <motion.div
              key={i}
              className="flex flex-col items-center text-center max-w-xs"
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: i * 0.2 }}
              viewport={{ once: true }}
            >
              {/* Icon container */}
              <div className="w-16 h-16 flex items-center justify-center rounded-full bg-blue-100 mb-4">
                {step.icon}
              </div>

              {/* Text */}
              <h3 className="text-xl font-semibold mb-2">{step.title}</h3>
              <p className="text-gray-600 text-sm">{step.desc}</p>

              
                <ArrowRight className="hidden md:block w-6 h-6 text-gray-400 absolute md:relative md:mt-10" />
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default UserFlow;
