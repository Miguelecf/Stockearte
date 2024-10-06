import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./ui/pages/Login";
import NotFound from "./ui/pages/NotFound";
import CentralDashboard from "./ui/pages/central/CentralDashboard";
import StoreDashboard from "./ui/pages/central/StoreDashboard";

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/central-dashboard/" element={<CentralDashboard />} />
        <Route path="/central-dashboard/stores" element={<StoreDashboard />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
};

export default App;
