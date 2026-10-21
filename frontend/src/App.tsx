import { Navigate, Route, Routes } from 'react-router-dom';
import { Navbar } from './components/Navbar';
import { DashboardPage } from './pages/DashboardPage';
import { DetectionPage } from './pages/DetectionPage';
import { HomePage } from './pages/HomePage';
import { PredictionPage } from './pages/PredictionPage';
import { RecyclingPage } from './pages/RecyclingPage';
import { ResearchPage } from './pages/ResearchPage';

function App() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <Navbar />
      <main className="mx-auto max-w-7xl px-4 py-6">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/detection" element={<DetectionPage />} />
          <Route path="/prediction" element={<PredictionPage />} />
          <Route path="/recycling" element={<RecyclingPage />} />
          <Route path="/research" element={<ResearchPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
