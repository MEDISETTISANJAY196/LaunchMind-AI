import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import { ThemeProvider } from "./context/ThemeContext";

import Landing from "./pages/Landing";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import StartupDetails from "./pages/StartupDetails";
import AISettings from "./pages/AISettings";
import AIMentor from "./pages/AIMentor";
import DashboardAnalytics from "./pages/DashboardAnalytics";
import Profile from "./pages/Profile";

function App() {
  return (
    <AuthProvider>
      <ThemeProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/startup/:id" element={<StartupDetails />} />
            <Route path="/settings" element={<AISettings />} />
            <Route path="/mentor/:id" element={<AIMentor />} />
            <Route path="/analytics" element={<DashboardAnalytics />} />
            <Route path="/profile" element={<Profile />} />
          </Routes>
        </BrowserRouter>
      </ThemeProvider>
    </AuthProvider>
  );
}

export default App;