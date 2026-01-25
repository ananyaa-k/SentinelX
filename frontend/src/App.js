import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';
import { Toaster } from 'sonner';
import Sidebar from './components/Sidebar';
import Header from './components/layout/Header';
import BriefingPage from './pages/BriefingPage';
import CommandCenterPage from './pages/CommandCenterPage';
import ThreatIntelPage from './pages/ThreatIntelPage';
import AiLogicPage from './pages/AiLogicPage';
import { ThemeProvider } from "./components/ThemeProvider";

const AppContent = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const location = useLocation();

  const toggleSidebar = () => setSidebarOpen(!sidebarOpen);

  return (
    <div className="flex min-h-screen bg-background text-foreground overflow-hidden font-sans">
      <Sidebar isOpen={sidebarOpen} toggleSidebar={toggleSidebar} />
      
      <main className="flex-1 lg:ml-64 relative min-h-screen flex flex-col transition-all duration-300">
        <Header toggleSidebar={toggleSidebar} />
        
        <div className="flex-1 relative z-10">
          <AnimatePresence mode="wait">
            <Routes location={location} key={location.pathname}>
              <Route path="/" element={<BriefingPage />} />
              <Route path="/command-center" element={<CommandCenterPage />} />
              <Route path="/threat-intel" element={<ThreatIntelPage />} />
              <Route path="/ai-logic" element={<AiLogicPage />} />
            </Routes>
          </AnimatePresence>
        </div>
      </main>
      
      <Toaster position="top-right" theme="system" />
    </div>
  );
};

function App() {
  return (
    <ThemeProvider defaultTheme="dark" storageKey="sentinelx-theme">
      <Router>
        <AppContent />
      </Router>
    </ThemeProvider>
  );
}

export default App;
