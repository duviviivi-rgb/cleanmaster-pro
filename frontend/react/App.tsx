import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import HomePage from './pages/HomePage';
import ScanPage from './pages/ScanPage';
import CleanPage from './pages/CleanPage';
import SpacePage from './pages/SpacePage';
import RecoveryPage from './pages/RecoveryPage';
import OptimizationPage from './pages/OptimizationPage';
import AppPage from './pages/AppPage';
import GovernancePage from './pages/GovernancePage';
import HistoryPage from './pages/HistoryPage';
import SettingsPage from './pages/SettingsPage';
import Navbar from './components/Navbar';

function App() {
  return (
    <Router>
      <div className="flex h-screen bg-gray-50">
        <Navbar />
        <div className="flex-1 overflow-y-auto p-6">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/scan" element={<ScanPage />} />
            <Route path="/clean" element={<CleanPage />} />
            <Route path="/space" element={<SpacePage />} />
            <Route path="/recovery" element={<RecoveryPage />} />
            <Route path="/optimization" element={<OptimizationPage />} />
            <Route path="/apps" element={<AppPage />} />
            <Route path="/governance" element={<GovernancePage />} />
            <Route path="/history" element={<HistoryPage />} />
            <Route path="/settings" element={<SettingsPage />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;