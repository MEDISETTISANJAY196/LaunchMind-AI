import React from "react";
import { NavLink } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { 
  LayoutDashboard, 
  BarChart3, 
  FileSpreadsheet, 
  Target, 
  ShieldAlert, 
  Sparkles, 
  MessageSquareCode, 
  Download 
} from "lucide-react";

export default function Sidebar() {
  const { currentStartup } = useAuth();

  const menuItems = [
    { name: "Dashboard", path: "/dashboard", icon: LayoutDashboard },
    { name: "SWOT Matrix", path: "/swot", icon: ShieldAlert },
    { name: "Business Canvas", path: "/canvas", icon: FileSpreadsheet },
    { name: "Market Research", path: "/market", icon: Target },
    { name: "Competitors", path: "/competitors", icon: BarChart3 },
    { name: "Branding Studio", path: "/branding", icon: Sparkles },
    { name: "AI Mentor Chat", path: "/mentor", icon: MessageSquareCode },
    { name: "Reports Center", path: "/reports", icon: Download },
  ];

  if (!currentStartup) return null;

  return (
    <aside className="w-64 border-r border-slate-800 bg-slate-950/40 min-h-[calc(100vh-73px)] flex flex-col p-4">
      <div className="mb-6 px-3 py-2.5 rounded-xl bg-slate-900/50 border border-slate-800/80">
        <p className="text-[10px] uppercase font-bold text-slate-500 tracking-wider">Active Startup</p>
        <h3 className="text-sm font-bold text-indigo-400 truncate mt-0.5">{currentStartup.name}</h3>
        <p className="text-xs text-slate-400 truncate mt-0.5">{currentStartup.industry || "General Industry"}</p>
      </div>

      <nav className="flex-1 space-y-1">
        {menuItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 ${
                  isActive
                    ? "bg-indigo-600 text-white shadow-lg shadow-indigo-600/10 font-semibold"
                    : "text-slate-400 hover:text-slate-200 hover:bg-slate-900/50"
                }`
              }
            >
              <Icon className="w-5 h-5" />
              <span>{item.name}</span>
            </NavLink>
          );
        })}
      </nav>
    </aside>
  );
}
