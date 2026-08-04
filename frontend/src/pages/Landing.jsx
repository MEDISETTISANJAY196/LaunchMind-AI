import React from "react";
import { Link } from "react-router-dom";
import { ArrowRight, Sparkles, Shield, Compass, BookOpen } from "lucide-react";

export default function Landing() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col justify-between">
      {/* Navbar */}
      <header className="px-6 py-5 flex items-center justify-between border-b border-slate-900/60 max-w-7xl mx-auto w-full">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-500 to-purple-600 flex items-center justify-center font-bold text-white shadow-lg shadow-indigo-500/20">
            LM
          </div>
          <span className="text-xl font-bold tracking-wide">LaunchMind AI</span>
        </div>
        <div className="flex items-center gap-4">
          <Link to="/login" className="px-4 py-2 text-sm font-semibold text-slate-300 hover:text-white transition-colors">
            Log In
          </Link>
          <Link to="/register" className="px-5 py-2.5 text-sm font-semibold bg-indigo-600 hover:bg-indigo-500 rounded-xl transition-all shadow-lg shadow-indigo-600/20 text-white">
            Get Started
          </Link>
        </div>
      </header>

      {/* Hero Section */}
      <main className="max-w-7xl mx-auto px-6 py-20 flex flex-col items-center text-center flex-1 justify-center">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/30 text-indigo-400 text-xs font-semibold mb-8 animate-pulse">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Empowering Founders with Local Knowledge RAG</span>
        </div>

        <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight mb-6 max-w-4xl leading-tight">
          Launch Your Startup Idea With{" "}
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-500">
            AI Precision
          </span>
        </h1>

        <p className="text-lg md:text-xl text-slate-400 max-w-2xl mb-10 leading-relaxed">
          The all-in-one founder's dashboard. Automate SWOT analysis, construct Business Model Canvases, design brand guides, and chat with AI mentors grounded in expert materials.
        </p>

        <div className="flex flex-col sm:flex-row items-center gap-4 mb-16">
          <Link
            to="/register"
            className="w-full sm:w-auto px-8 py-4 bg-indigo-600 hover:bg-indigo-500 rounded-2xl font-bold transition-all shadow-xl shadow-indigo-600/30 text-white flex items-center justify-center gap-2 text-base group"
          >
            <span>Launch My Startup</span>
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </Link>
          <Link
            to="/login"
            className="w-full sm:w-auto px-8 py-4 bg-slate-900 hover:bg-slate-800 border border-slate-800 rounded-2xl font-bold transition-colors text-slate-300 flex items-center justify-center"
          >
            Founder Login
          </Link>
        </div>

        {/* Feature Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 w-full mt-8">
          <div className="p-6 rounded-2xl bg-slate-900/50 border border-slate-800/80 text-left">
            <div className="w-12 h-12 rounded-xl bg-indigo-500/10 flex items-center justify-center mb-4 text-indigo-400">
              <Shield className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold mb-2">SWOT Analysis</h3>
            <p className="text-slate-400 text-sm leading-relaxed">
              Generate full SWOT matrices with immediate structural and competitive feedback.
            </p>
          </div>

          <div className="p-6 rounded-2xl bg-slate-900/50 border border-slate-800/80 text-left">
            <div className="w-12 h-12 rounded-xl bg-indigo-500/10 flex items-center justify-center mb-4 text-indigo-400">
              <Compass className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold mb-2">Business Canvas</h3>
            <p className="text-slate-400 text-sm leading-relaxed">
              Osterwalder-based interactive board auto-completed by AI for target niches.
            </p>
          </div>

          <div className="p-6 rounded-2xl bg-slate-900/50 border border-slate-800/80 text-left">
            <div className="w-12 h-12 rounded-xl bg-indigo-500/10 flex items-center justify-center mb-4 text-indigo-400">
              <BookOpen className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold mb-2">Expert RAG Mentor</h3>
            <p className="text-slate-400 text-sm leading-relaxed">
              Chat with Paul Graham or Steve Jobs, with advice grounded in local guides.
            </p>
          </div>

          <div className="p-6 rounded-2xl bg-slate-900/50 border border-slate-800/80 text-left">
            <div className="w-12 h-12 rounded-xl bg-indigo-500/10 flex items-center justify-center mb-4 text-indigo-400">
              <Sparkles className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold mb-2">Branding Studio</h3>
            <p className="text-slate-400 text-sm leading-relaxed">
              Receive smart naming suggestions, slogans, logo prompts, and hex code palettes.
            </p>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-900 py-8 px-6 text-center text-sm text-slate-500 max-w-7xl mx-auto w-full">
        <p>&copy; {new Date().getFullYear()} LaunchMind-AI. Powered by Google Gemini and FAISS.</p>
      </footer>
    </div>
  );
}
