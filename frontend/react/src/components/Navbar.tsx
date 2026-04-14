import React from 'react';
import { Link } from 'react-router-dom';

const Navbar: React.FC = () => {
  return (
    <nav className="sticky top-0 z-10 bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-6 py-3 flex items-center justify-between">
        <div className="flex items-center">
          <Link to="/" className="text-xl font-bold text-primary">
            CleanMaster Pro
          </Link>
        </div>
        <div className="flex items-center space-x-4">
          <button className="px-4 py-2 rounded-lg border border-gray-300 text-gray-700 hover:bg-gray-50 transition-colors duration-200">
            帮助
          </button>
          <button className="px-4 py-2 rounded-lg bg-primary text-white hover:bg-blue-600 transition-colors duration-200 font-medium">
            立即扫描
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;