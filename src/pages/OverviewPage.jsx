// src/pages/OverviewPage.jsx
import React, { useState } from "react";
import { motion } from "framer-motion";
import { Loader2, Sparkles, X, Download } from "lucide-react";

// Dummy B.Ed course data (simplified for demo)
const courses = [
  { sno: 1, name: "Childhood and Growing up", code: "BED 101", type: "Theory", credit: 4, practical: 0, theory: 4, students: 60 },
  { sno: 2, name: "Philosophical Foundations of Education", code: "BED 103", type: "Theory", credit: 4, practical: 0, theory: 4, students: 60 },
  { sno: 3, name: "Language Across the Curriculum", code: "BED 105", type: "Theory", credit: 2, practical: 0, theory: 2, students: 60 },
  { sno: 4, name: "Understanding Disciplines and Subjects", code: "BED 107", type: "Theory", credit: 4, practical: 0, theory: 4, students: 60 },
  { sno: 5, name: "Critical Understanding of ICT", code: "BED 109", type: "Theory", credit: 4, practical: 0, theory: 4, students: 60 },
  { sno: 6, name: "School Organisation and Management", code: "BED 111", type: "Theory", credit: 4, practical: 0, theory: 4, students: 60 },
  { sno: 7, name: "Understanding the Self", code: "BED 151", type: "Practical", credit: 2, practical: 2, theory: 0, students: 60 },
  { sno: 8, name: "PSE-1 (Preliminary School Engagement)", code: "BED 153", type: "Practical", credit: 2, practical: 2, theory: 0, students: 60 },
  { sno: 9, name: "MOOC", code: "-", type: "Elective", credit: 4, practical: 0, theory: 4, students: 60 },
];

// Dummy faculty data
const faculty = [
  { course: "Childhood and Growing up", faculty: "Dr. Meera Sharma" },
  { course: "Philosophical Foundations of Education", faculty: "Dr. Rajesh Verma" },
  { course: "Language Across the Curriculum", faculty: "Prof. Ananya Gupta" },
  { course: "Understanding Disciplines and Subjects", faculty: "Dr. Karan Malhotra" },
];

// Dummy timetable (Mon–Fri, 5 periods)
const timetable = [
  ["BED 101", "BED 103", "BED 105", "BED 107", "BED 109"],
  ["BED 111", "BED 151", "BED 153", "MOOC", "BED 101"],
  ["BED 103", "BED 105", "BED 107", "BED 109", "BED 111"],
  ["BED 151", "BED 153", "MOOC", "BED 101", "BED 103"],
  ["BED 105", "BED 107", "BED 109", "BED 111", "BED 151"],
];

const OverviewPage = () => {
  const [loading, setLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);

  const handleGenerateTimetable = () => {
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      setShowModal(true);
    }, 2500);
  };

  const handleExport = () => {
    alert("✅ Exported timetable as PDF/Excel (dummy action).");
  };

  return (
    <section className="py-12 px-6 bg-gray-50 min-h-screen">
      <motion.div
        className="max-w-6xl mx-auto bg-white shadow-lg rounded-2xl p-8"
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <div className="mb-8 border-b pb-4">
          <h2 className="text-3xl font-bold text-gray-800 flex items-center gap-2">
            📊 Program Overview
          </h2>
          <p className="text-gray-500 mt-2">
            Consolidated view of selected courses and faculty details.
          </p>
        </div>

        {/* Course Table */}
        <h3 className="text-xl font-semibold mb-4 text-gray-700">Course Details</h3>
        <div className="overflow-x-auto mb-10">
          <table className="w-full border-collapse rounded-lg overflow-hidden shadow-sm">
            <thead className="bg-blue-100 text-gray-700">
              <tr>
                <th className="px-4 py-2 border">Sub.No</th>
                <th className="px-4 py-2 border">S.Name</th>
                <th className="px-4 py-2 border">S.Code</th>
                <th className="px-4 py-2 border">S.Type</th>
                <th className="px-4 py-2 border">Credit</th>
                <th className="px-4 py-2 border">Practical</th>
                <th className="px-4 py-2 border">Theory</th>
                <th className="px-4 py-2 border">No. of Students</th>
              </tr>
            </thead>
            <tbody>
              {courses.map((c) => (
                <tr key={c.sno} className="hover:bg-gray-50 text-sm">
                  <td className="px-4 py-2 border text-center">{c.sno}</td>
                  <td className="px-4 py-2 border">{c.name}</td>
                  <td className="px-4 py-2 border text-center">{c.code}</td>
                  <td className="px-4 py-2 border text-center">{c.type}</td>
                  <td className="px-4 py-2 border text-center">{c.credit}</td>
                  <td className="px-4 py-2 border text-center">{c.practical}</td>
                  <td className="px-4 py-2 border text-center">{c.theory}</td>
                  <td className="px-4 py-2 border text-center">{c.students}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Faculty Table */}
        <h3 className="text-xl font-semibold mb-4 text-gray-700">Faculty Assignments</h3>
        <div className="overflow-x-auto mb-10">
          <table className="w-full border-collapse rounded-lg overflow-hidden shadow-sm">
            <thead className="bg-green-100 text-gray-700">
              <tr>
                <th className="px-4 py-2 border">Course</th>
                <th className="px-4 py-2 border">Assigned Faculty</th>
              </tr>
            </thead>
            <tbody>
              {faculty.map((f, idx) => (
                <tr key={idx} className="hover:bg-gray-50 text-sm">
                  <td className="px-4 py-2 border">{f.course}</td>
                  <td className="px-4 py-2 border">{f.faculty}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Generate Timetable Button */}
        <div className="flex justify-center">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            disabled={loading}
            onClick={handleGenerateTimetable}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg flex items-center gap-2 shadow-md hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <>
                <Loader2 className="animate-spin w-5 h-5" />
                <span>Generating with AI...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-5 h-5" />
                <span>Generate Timetable</span>
              </>
            )}
          </motion.button>
        </div>
      </motion.div>

      {/* Timetable Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex items-center justify-center z-50">
          <motion.div
            className="bg-white rounded-xl shadow-2xl p-6 w-full max-w-4xl"
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
          >
            <div className="flex justify-between items-center border-b pb-3 mb-4">
              <h3 className="text-xl font-semibold">📅 Generated Timetable</h3>
              <button onClick={() => setShowModal(false)}>
                <X className="w-6 h-6 text-gray-500 hover:text-gray-700" />
              </button>
            </div>

            {/* Timetable */}
            <div className="overflow-x-auto">
              <table className="w-full border-collapse text-sm shadow">
                <thead className="bg-blue-100 text-gray-700">
                  <tr>
                    <th className="px-4 py-2 border">Day</th>
                    <th className="px-4 py-2 border">Period 1</th>
                    <th className="px-4 py-2 border">Period 2</th>
                    <th className="px-4 py-2 border">Period 3</th>
                    <th className="px-4 py-2 border">Period 4</th>
                    <th className="px-4 py-2 border">Period 5</th>
                  </tr>
                </thead>
                <tbody>
                  {["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"].map(
                    (day, i) => (
                      <tr key={day} className="hover:bg-gray-50">
                        <td className="px-4 py-2 border font-medium">{day}</td>
                        {timetable[i].map((slot, j) => (
                          <td key={j} className="px-4 py-2 border text-center">
                            {slot}
                          </td>
                        ))}
                      </tr>
                    )
                  )}
                </tbody>
              </table>
            </div>

            <div className="flex justify-end mt-6">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => alert("✅ Exported timetable (dummy action)")}
                className="px-5 py-2 bg-green-600 text-white rounded-lg flex items-center gap-2 shadow-md hover:bg-green-700 transition"
              >
                <Download className="w-5 h-5" />
                Export Timetable
              </motion.button>
            </div>
          </motion.div>
        </div>
      )}
    </section>
  );
};

export default OverviewPage;
