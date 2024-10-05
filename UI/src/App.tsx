import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./ui/pages/Login";
import Dashboard from "./ui/pages/Dashboard";
import NotFound from "./ui/pages/NotFound";

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  );
};

export default App;
