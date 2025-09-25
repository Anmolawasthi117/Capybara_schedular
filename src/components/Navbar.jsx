import React from "react";
import { Link } from "react-router-dom";
const Navbar = () => {
  return (
    <nav className="flex items-center justify-between px-6 py-4 shadow-sm sticky top-0 bg-white z-50">
      <div className="text-2xl font-bold">Schedulify</div>
      <Link to="/admin" className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition">
        Get started
      </Link>
    </nav>
  );
};

export default Navbar;
