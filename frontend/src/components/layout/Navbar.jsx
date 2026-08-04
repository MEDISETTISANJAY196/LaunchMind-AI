import React, { useState, useEffect } from "react";
import { useAuth } from "../../context/AuthContext";
import { api } from "../../services/api";
import { LogOut, ChevronDown, User, Layers, Plus } from "lucide-react";

export default function Navbar() {
  const { user, logout, currentStartup, selectStartup } = useAuth();
  const [startups, setStartups] = useState([]);
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    if (user) {
      api.startups.list()
        .then(setStartups)
        .catch(console.error);
    }
  }, [user, currentStartup]);

  return (
    <nav className="glass sticky top-0 z-50 flex items-center justify-between px-6 py-4 border-b border-slate-800">
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-500 to-purple-600 flex items-center justify-center font-bold text-white shadow-lg shadow-indigo-500/20">
          LM
        </div>
        <div>
          <h1 className="text-xl font-bold tracking-wide text-transparent bg-clip-text bg-gradient-to-r from-white to-slate-400">
            LaunchMind AI
          </h1>
          <p className="text-xs text-indigo-400 font-medium">Founder Co-pilot</p>
        </div>
      </div>

      <div className="flex items-center gap-6">
        {user && (
          <>
            {/* Startup Selector */}
            <div className="relative">
              <button
                onClick={() => setIsOpen(!isOpen)}
                className="flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 border border-slate-700/80 text-sm font-medium text-slate-200 transition-all duration-200"
              >
                <Layers className="w-4 h-4 text-indigo-400" />
                <span>{currentStartup ? currentStartup.name : "Select Startup"}</span>
                <ChevronDown className={`w-4 h-4 text-slate-400 transition-transform ${isOpen ? "rotate-180" : ""}`} />
              </button>

              {isOpen && (
                <div className="absolute right-0 mt-2 w-56 rounded-xl bg-slate-800 border border-slate-700 shadow-xl overflow-hidden z-50">
                  <div className="px-3 py-2 text-xs font-semibold text-slate-400 border-b border-slate-700">
                    Switch Startup
                  </div>
                  <div className="max-h-60 overflow-y-auto">
                    {startups.map((s) => (
                      <button
                        key={s.id}
                        onClick={() => {
                          selectStartup(s);
                          setIsOpen(false);
                        }}
                        className={`w-full text-left px-4 py-2.5 text-sm hover:bg-slate-700/50 transition-colors flex items-center justify-between ${
                          currentStartup?.id === s.id ? "text-indigo-400 font-semibold bg-indigo-500/5" : "text-slate-300"
                        }`}
                      >
                        {s.name}
                      </button>
                    ))}
                    {startups.length === 0 && (
                      <div className="px-4 py-3 text-xs text-slate-500 italic">No startups created yet</div>
                    )}
                  </div>
                </div>
              )}
            </div>

            {/* Profile Dropdown */}
            <div className="flex items-center gap-3 border-l border-slate-800 pl-6">
              <div className="flex flex-col items-end">
                <span className="text-sm font-semibold text-slate-200">{user.full_name || user.email}</span>
                <span className="text-xs text-slate-400">{user.is_admin ? "Administrator" : "Founder"}</span>
              </div>
              
              <button
                onClick={logout}
                title="Log Out"
                className="w-10 h-10 rounded-xl bg-slate-800 hover:bg-red-950/20 hover:text-red-400 border border-slate-700 hover:border-red-900/50 flex items-center justify-center text-slate-300 transition-all duration-200"
              >
                <LogOut className="w-5 h-5" />
              </button>
            </div>
          </>
        )}
      </div>
    </nav>
  );
}
