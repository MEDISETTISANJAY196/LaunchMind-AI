import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { api } from "../services/api";
import StartupCard from "../components/StartupCard";
import CreateStartupModal from "../components/CreateStartupModal";
import { useTheme } from "../context/ThemeContext";


export default function Dashboard() {
    const navigate = useNavigate();
    const { user, logout } = useAuth();
    const { theme, toggleTheme } = useTheme();

    const [showModal, setShowModal] = useState(false);
    const [startups, setStartups] = useState([]);
    const [loading, setLoading] = useState(true);


    const loadStartups = async () => {
        try {
            setLoading(true);

            const data = await api.startups.list();

            setStartups(data);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadStartups();
    }, []);

    const handleCreateStartup = async (form) => {
        try {
            await api.startups.create(form);

            alert("Startup Created Successfully!");

            setShowModal(false);

            await loadStartups();
        } catch (err) {
            alert(err.message);
        }
    };

    const handleDeleteStartup = async (id) => {
        const confirmDelete = window.confirm(
            "Are you sure you want to delete this startup?"
        );

        if (!confirmDelete) return;

        try {
            await api.startups.delete(id);

            alert("Startup Deleted Successfully!");

            await loadStartups();
        } catch (err) {
            alert(err.message);
        }
    };

    return (
        <div
            className={`min-h-screen flex ${theme === "dark"
                ? "bg-slate-950 text-white"
                : "bg-gray-100 text-black"
                }`}
        >

            {/* Sidebar */}
            <aside
                className={`w-full md:w-64 p-6 ${theme === "dark"
                        ? "bg-slate-900"
                        : "bg-white shadow-lg"
                    }`}
            >

                <h1 className="text-2xl font-bold text-indigo-400">
                    🚀 LaunchMind
                </h1>

                <nav className="mt-10 space-y-4">

                    <button className="block w-full text-left hover:text-indigo-400">
                        🏠 Dashboard
                    </button>

                    <button className="block w-full text-left hover:text-indigo-400">
                        💡 My Startups
                    </button>

                    <button className="block w-full text-left hover:text-indigo-400">
                        📊 AI Analysis
                    </button>

                    <button className="block w-full text-left hover:text-indigo-400">
                        📈 Market Research
                    </button>

                    <button className="block w-full text-left hover:text-indigo-400">
                        📄 Reports
                    </button>
                    <button
                        onClick={() => navigate("/analytics")}
                        className="bg-cyan-600 hover:bg-cyan-500 px-6 py-3 rounded-lg font-semibold transition"
                    >
                        📊 Dashboard Analytics
                    </button>
                    <button
                        onClick={() => navigate("/profile")}
                        className="block w-full text-left hover:text-cyan-400"
                    >
                        👤 Profile
                    </button>
                    <button
                        onClick={toggleTheme}
                        className="block w-full text-left hover:text-cyan-400"
                    >
                        {theme === "dark"
                            ? "☀ Switch to Light Mode"
                            : "🌙 Switch to Dark Mode"}
                    </button>
                </nav>

            </aside>

            {/* Main Content */}
            <main
                className={`flex-1 p-8 ${theme === "dark"
                    ? "bg-slate-950"
                    : "bg-gray-100"
                    }`}
            >

                <div className="flex justify-between items-center">

                    <div>
                        <h2 className="text-3xl font-bold">
                            Welcome, {user?.full_name}
                        </h2>

                        <p
                            className={
                                theme === "dark"
                                    ? "text-slate-400"
                                    : "text-gray-600"
                            }
                        >
                            {user?.email}
                        </p>
                    </div>

                    <button
                        onClick={logout}
                        className="bg-red-600 px-4 py-2 rounded-lg hover:bg-red-500"
                    >
                        Logout
                    </button>

                </div>

                <div className="mt-10 flex justify-between items-center">

                    <h3 className="text-2xl font-semibold">
                        My Startups
                    </h3>

                    <button
                        onClick={() => setShowModal(true)}
                        className="bg-indigo-600 px-5 py-2 rounded-lg hover:bg-indigo-500"
                    >
                        + Create Startup
                    </button>

                </div>

                <div className="mt-8">

                    {loading ? (

                        <div className="text-center text-lg">
                            Loading...
                        </div>

                    ) : startups.length === 0 ? (

                        <div
                            className={`rounded-xl p-10 text-center ${theme === "dark"
                                ? "border border-slate-800"
                                : "bg-white shadow-lg"
                                }`}
                        >

                            <h3 className="text-xl font-semibold">
                                No startups yet
                            </h3>

                            <p className="text-slate-400 mt-2">
                                Click "Create Startup" to add your first startup.
                            </p>

                        </div>

                    ) : (

                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

                            {startups.map((startup) => (
                                <StartupCard
                                    key={startup.id}
                                    startup={startup}
                                    onDelete={handleDeleteStartup}
                                />
                            ))}

                        </div>

                    )}

                </div>

            </main>

            <CreateStartupModal
                open={showModal}
                onClose={() => setShowModal(false)}
                onSave={handleCreateStartup}
            />

        </div >
    );
}