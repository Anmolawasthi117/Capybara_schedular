// src/components/AdminPanel.jsx
import React, { useState } from "react";
import { motion } from "framer-motion";
import { Upload } from "lucide-react";
import { Link } from "react-router-dom";

const AdminPanel = () => {
  const [program, setProgram] = useState("");
  const [itepIntegrated, setItepIntegrated] = useState("");
  const [itepStage, setItepStage] = useState("");
  const [creditScheme, setCreditScheme] = useState("ltp");
  const [semester, setSemester] = useState("");
  const [uploadedFiles, setUploadedFiles] = useState({});

  const getSemesterOptions = () => {
    if (program === "B.Ed" || program === "M.Ed") {
      return Array.from({ length: 4 }, (_, i) => i + 1);
    } else if (program === "ITEP") {
      return Array.from({ length: 8 }, (_, i) => i + 1);
    }
    return [];
  };

  const handleFileUpload = (e, type) => {
    const file = e.target.files[0];
    setUploadedFiles((prev) => ({ ...prev, [type]: file?.name }));
    console.log(`${type} file uploaded:`, file);
  };

  const handleOverview = () => {
    alert(`
📋 Final Overview:
Program: ${program}
Integrated: ${itepIntegrated || "-"}
Stage: ${itepStage || "-"}
Credit Scheme: ${creditScheme === "tp" ? "Theory + Practical" : "Lecture + Tutorial + Practical"}
Semester: ${semester || "-"}
Uploads:
- Student: ${uploadedFiles["Student Details"] || "Not uploaded"}
- Faculty: ${uploadedFiles["Faculty Details"] || "Not uploaded"}
- Infrastructure: ${uploadedFiles["Infrastructure Details"] || "Not uploaded"}
    `);
  };

  return (
    <section className="py-12 px-6 bg-gray-100 min-h-screen">
      <motion.div
        className="max-w-5xl mx-auto bg-white rounded-2xl shadow-xl p-10 border border-gray-200"
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        {/* Header */}
        <div className="mb-10 border-b pb-6">
          <h2 className="text-3xl font-bold text-gray-800">Admin Configuration</h2>
          <p className="text-gray-500 mt-2">
            Setup your program, upload institute data, and prepare to generate timetables.
          </p>
        </div>

        {/* Program Selection */}
        <div className="mb-8">
          <h3 className="text-lg font-semibold mb-3 text-gray-700">Select Program</h3>
          <select
            value={program}
            onChange={(e) => {
              setProgram(e.target.value);
              setItepIntegrated("");
              setItepStage("");
              setSemester("");
            }}
            className="w-full border rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500"
          >
            <option value="">-- Choose a Program --</option>
            <option value="B.Ed">B.Ed</option>
            <option value="M.Ed">M.Ed</option>
            <option value="ITEP">ITEP</option>
          </select>
        </div>

        {/* ITEP Sub-dropdowns */}
        {program === "ITEP" && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5 }}>
            {/* Integrated */}
            <div className="mb-8">
              <h3 className="text-lg font-semibold mb-3 text-gray-700">Select Integrated Program</h3>
              <select
                value={itepIntegrated}
                onChange={(e) => setItepIntegrated(e.target.value)}
                className="w-full border rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500"
              >
                <option value="">-- Choose --</option>
                <option value="BA B.Ed">B.A. B.Ed</option>
                <option value="B.Com B.Ed">B.Com B.Ed</option>
                <option value="B.Sc B.Ed">B.Sc B.Ed</option>
              </select>
            </div>

            {/* Stage */}
            <div className="mb-8">
              <h3 className="text-lg font-semibold mb-3 text-gray-700">Select Education Stage</h3>
              <select
                value={itepStage}
                onChange={(e) => setItepStage(e.target.value)}
                className="w-full border rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500"
              >
                <option value="">-- Choose --</option>
                <option value="Foundation">Foundation</option>
                <option value="Preparatory">Preparatory</option>
                <option value="Middle">Middle</option>
                <option value="Secondary">Secondary</option>
              </select>
            </div>
          </motion.div>
        )}

        {/* Credit Scheme */}
        <div className="mb-8">
          <h3 className="text-lg font-semibold mb-3 text-gray-700">Credit Scheme</h3>
          <div className="flex gap-8">
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                name="creditScheme"
                value="tp"
                checked={creditScheme === "tp"}
                onChange={() => setCreditScheme("tp")}
              />
              Theory + Practical
            </label>
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                name="creditScheme"
                value="ltp"
                checked={creditScheme === "ltp"}
                onChange={() => setCreditScheme("ltp")}
              />
              Lecture + Tutorial + Practical
            </label>
          </div>
        </div>

        {/* File Uploads */}
        <div className="mb-8">
          <h3 className="text-lg font-semibold mb-3 text-gray-700">Upload Data</h3>
          <div className="grid md:grid-cols-3 gap-6">
            {["Student Details", "Faculty Details", "Infrastructure Details"].map((label) => (
              <label
                key={label}
                className="flex flex-col items-center justify-center border-2 border-dashed border-gray-300 rounded-lg p-6 cursor-pointer hover:border-blue-500 transition"
              >
                <Upload className="w-8 h-8 text-blue-500 mb-2" />
                <span className="text-gray-600 text-sm mb-2">{label}</span>
                <input
                  type="file"
                  className="hidden"
                  onChange={(e) => handleFileUpload(e, label)}
                />
                <span className="px-3 py-1 text-xs bg-blue-100 text-blue-600 rounded">
                  {uploadedFiles[label] ? "Uploaded" : "Upload"}
                </span>
              </label>
            ))}
          </div>
        </div>

        {/* Semester Dropdown */}
        {program && (
          <div className="mb-8">
            <h3 className="text-lg font-semibold mb-3 text-gray-700">Select Semester</h3>
            <select
              value={semester}
              onChange={(e) => setSemester(e.target.value)}
              className="w-full border rounded-lg px-4 py-2 focus:ring-2 focus:ring-blue-500"
            >
              <option value="">-- Choose Semester --</option>
              {getSemesterOptions().map((sem) => (
                <option key={sem} value={sem}>
                  Semester {sem}
                </option>
              ))}
            </select>
          </div>
        )}

        {/* Actions */}
          <Link to="/overview">
        <div className="mt-10 flex flex-col md:flex-row gap-4">
          <button
            className="w-full bg-blue-600 text-white font-semibold py-3 rounded-lg hover:bg-blue-700 transition"
            onClick={() => console.log("Saved config")}
          >
            Save & Continue
          </button>
        </div>
          </Link>
      </motion.div>
    </section>
  );
};

export default AdminPanel;
