
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
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

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Sidebar />
        <div className="ml-64">
          <Navbar />
          <div className="p-6">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/scan" element={<ScanPage />} />
              <Route path="/clean" element={<CleanPage />} />
              <Route path="/space" element={<SpacePage />} />
              <Route path="/recovery" element={<RecoveryPage />} />
              <Route path="/optimization" element={<OptimizationPage />} />
              <Route path="/app" element={<AppPage />} />
              <Route path="/governance" element={<GovernancePage />} />
              <Route path="/history" element={<HistoryPage />} />
              <Route path="/settings" element={<SettingsPage />} />
            </Routes>
          </div>
        </div>
      </div>
    </Router>
  );
}

export default App;