// src/components/Footer.jsx
import React from "react";

const Footer = () => {
  return (
    <footer className="py-6 bg-gray-100 text-center text-gray-600 text-sm">
      <p>© {new Date().getFullYear()} Schedulr. Built by team capybara </p>
    </footer>
  );
};

export default Footer;
