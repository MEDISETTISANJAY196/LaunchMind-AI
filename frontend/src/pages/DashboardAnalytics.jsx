import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../services/api";

import jsPDF from "jspdf";
import autoTable from "jspdf-autotable";

import {
    ResponsiveContainer,
    BarChart,
    Bar,
    PieChart,
    Pie,
    Cell,
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
} from "recharts";

export default function DashboardAnalytics() {
    const navigate = useNavigate();

    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [notifications, setNotifications] = useState([]);
    const [insights, setInsights] = useState(null);

    useEffect(() => {
        loadAnalytics();
    }, []);

    const loadAnalytics = async () => {
        try {
            const result = await api.analytics.dashboard();
            const notify = await api.notifications.list();
            const ai = await api.insights.get();

            setData(result);
            setNotifications(notify);
            setInsights(ai);

        } catch (err) {
            alert(err.message);
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-slate-950 text-white">
                Loading Analytics...
            </div>
        );
    }

    if (!data) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-slate-950 text-white">
                No analytics data found.
            </div>
        );
    }

    const chartData = [
        { name: "Startups", value: data.total_startups },
        { name: "AI", value: data.analyses },
        { name: "Mentor", value: data.mentor_chats },
        { name: "Reports", value: data.reports },
    ];

    const scoreData = [
        { name: "Completed", value: data.avg_score },
        { name: "Remaining", value: 100 - data.avg_score },
    ];

    const COLORS = [
        "#6366F1",
        "#10B981",
        "#F59E0B",
        "#EF4444",
    ];

    const growthData = [
        { month: "Jan", score: 10 },
        { month: "Feb", score: 20 },
        { month: "Mar", score: 35 },
        { month: "Apr", score: 50 },
        { month: "May", score: 65 },
        { month: "Jun", score: data.avg_score },
    ];

    const activities = [
        {
            icon: "🚀",
            title: "Startup Created",
            time: "Today",
        },
        {
            icon: "🤖",
            title: "AI Analysis Completed",
            time: "Today",
        },
        {
            icon: "💬",
            title: "Mentor Chat Finished",
            time: "Yesterday",
        },
        {
            icon: "📄",
            title: "Report Generated",
            time: "2 Days Ago",
        },
    ];

    const exportCSV = () => {
        const rows = [
            ["Metric", "Value"],
            ["Total Startups", data.total_startups],
            ["AI Analyses", data.analyses],
            ["Mentor Chats", data.mentor_chats],
            ["Reports", data.reports],
            ["Average Score", data.avg_score],
        ];

        const csv = rows.map((row) => row.join(",")).join("\n");

        const blob = new Blob([csv], {
            type: "text/csv;charset=utf-8;",
        });

        const url = URL.createObjectURL(blob);

        const link = document.createElement("a");

        link.href = url;
        link.download = "LaunchMind_Analytics.csv";
        link.click();
    };

    const exportPDF = () => {
        const doc = new jsPDF();

        doc.setFontSize(20);
        doc.text("LaunchMind AI - Analytics Report", 20, 20);

        autoTable(doc, {
            startY: 35,
            head: [["Metric", "Value"]],
            body: [
                ["Total Startups", data.total_startups],
                ["AI Analyses", data.analyses],
                ["Mentor Chats", data.mentor_chats],
                ["Reports", data.reports],
                ["Average Score", `${data.avg_score}%`],
            ],
        });

        doc.save("LaunchMind_Analytics_Report.pdf");
    };

    return (
        <div className="min-h-screen bg-slate-950 text-white p-8">

            {/* Header */}

            <div className="flex flex-col lg:flex-row justify-between items-center gap-4 mb-8">

                <h1 className="text-4xl font-bold text-cyan-400">
                    📊 Dashboard Analytics
                </h1>

                <div className="flex flex-wrap gap-3">

                    <button
                        onClick={exportCSV}
                        className="bg-green-600 hover:bg-green-500 px-5 py-3 rounded-lg"
                    >
                        📊 Export CSV
                    </button>

                    <button
                        onClick={exportPDF}
                        className="bg-red-600 hover:bg-red-500 px-5 py-3 rounded-lg"
                    >
                        📄 Export PDF
                    </button>

                    <button
                        onClick={() => navigate("/dashboard")}
                        className="bg-indigo-600 hover:bg-indigo-500 px-6 py-3 rounded-lg"
                    >
                        ← Dashboard
                    </button>

                </div>

            </div>

            {/* KPI Cards */}

            <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-5 gap-5">

                <div className="bg-slate-900 rounded-xl p-6 shadow-lg">
                    <p className="text-gray-400">🚀 Total Startups</p>
                    <h2 className="text-4xl font-bold mt-3">
                        {data.total_startups}
                    </h2>
                </div>

                <div className="bg-slate-900 rounded-xl p-6 shadow-lg">
                    <p className="text-gray-400">🤖 AI Analyses</p>
                    <h2 className="text-4xl font-bold mt-3">
                        {data.analyses}
                    </h2>
                </div>

                <div className="bg-slate-900 rounded-xl p-6 shadow-lg">
                    <p className="text-gray-400">💬 Mentor Chats</p>
                    <h2 className="text-4xl font-bold mt-3">
                        {data.mentor_chats}
                    </h2>
                </div>

                <div className="bg-slate-900 rounded-xl p-6 shadow-lg">
                    <p className="text-gray-400">📄 Reports</p>
                    <h2 className="text-4xl font-bold mt-3">
                        {data.reports}
                    </h2>
                </div>

                <div className="bg-slate-900 rounded-xl p-6 shadow-lg">
                    <p className="text-gray-400">⭐ Avg Score</p>
                    <h2 className="text-4xl font-bold mt-3">
                        {data.avg_score}%
                    </h2>
                </div>

            </div>

            {/* Charts */}

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-10">

                {/* Bar Chart */}

                <div className="bg-slate-900 rounded-xl p-6">

                    <h2 className="text-xl font-semibold mb-5">
                        📈 Startup Statistics
                    </h2>

                    <ResponsiveContainer width="100%" height={300}>
                        <BarChart data={chartData}>
                            <CartesianGrid strokeDasharray="3 3" />
                            <XAxis dataKey="name" />
                            <YAxis />
                            <Tooltip />
                            <Bar
                                dataKey="value"
                                fill="#06b6d4"
                                radius={[8, 8, 0, 0]}
                            />
                        </BarChart>
                    </ResponsiveContainer>

                </div>

                {/* Pie Chart */}

                <div className="bg-slate-900 rounded-xl p-6">

                    <h2 className="text-xl font-semibold mb-5">
                        🥧 Startup Score
                    </h2>

                    <ResponsiveContainer width="100%" height={300}>

                        <PieChart>

                            <Pie
                                data={scoreData}
                                dataKey="value"
                                nameKey="name"
                                outerRadius={110}
                                label
                            >

                                {scoreData.map((entry, index) => (
                                    <Cell
                                        key={index}
                                        fill={COLORS[index % COLORS.length]}
                                    />
                                ))}

                            </Pie>

                            <Tooltip />

                        </PieChart>

                    </ResponsiveContainer>

                </div>

            </div>
            {/* Line Chart + Recent Activity */}

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-8">

                {/* Line Chart */}

                <div className="bg-slate-900 rounded-xl p-6">

                    <h2 className="text-xl font-semibold mb-5">
                        📈 Growth Trend
                    </h2>

                    <ResponsiveContainer width="100%" height={300}>

                        <LineChart data={growthData}>

                            <CartesianGrid strokeDasharray="3 3" />

                            <XAxis dataKey="month" />

                            <YAxis />

                            <Tooltip />

                            <Line
                                type="monotone"
                                dataKey="score"
                                stroke="#06b6d4"
                                strokeWidth={3}
                            />

                        </LineChart>

                    </ResponsiveContainer>

                </div>

                {/* Recent Activity */}

                <div className="bg-slate-900 rounded-xl p-6">

                    <h2 className="text-2xl font-bold mb-6">
                        📅 Recent Activity
                    </h2>

                    <div className="space-y-4">

                        {activities.map((activity, index) => (

                            <div
                                key={index}
                                className="flex justify-between items-center bg-slate-800 rounded-lg p-4 hover:bg-slate-700 transition"
                            >

                                <div className="flex items-center gap-4">

                                    <div className="text-3xl">
                                        {activity.icon}
                                    </div>

                                    <div>

                                        <h3 className="font-semibold">
                                            {activity.title}
                                        </h3>

                                        <p className="text-gray-400 text-sm">
                                            {activity.time}
                                        </p>

                                    </div>

                                </div>

                            </div>

                        ))}

                    </div>

                </div>

            </div>

            {/* Notifications */}

            <div className="bg-slate-900 rounded-xl p-6 mt-8">

                <h2 className="text-2xl font-bold mb-6">
                    🔔 Notifications
                </h2>

                <div className="space-y-4">

                    {notifications.map((item, index) => (

                        <div
                            key={index}
                            className="bg-slate-800 rounded-lg p-4 flex justify-between items-center"
                        >

                            <span className="text-cyan-400 font-medium">
                                {item.title}
                            </span>

                            <span className="text-gray-400 text-sm">
                                {item.time}
                            </span>

                        </div>

                    ))}
                    <div className="bg-slate-900 rounded-xl p-6 mt-8">

                        <h2 className="text-2xl font-bold text-cyan-400 mb-5">
                            🤖 AI Insights
                        </h2>

                        {insights && (
                            <>
                                <p className="text-lg mb-5">
                                    <strong>Startup Readiness:</strong> {insights.startup_readiness}%
                                </p>

                                <ul className="space-y-3">
                                    {insights.recommendations.map((item, index) => (
                                        <li
                                            key={index}
                                            className="bg-slate-800 p-3 rounded-lg"
                                        >
                                            ✅ {item}
                                        </li>
                                    ))}
                                </ul>
                            </>
                        )}

                    </div>

                </div>

            </div>

        </div>
    );
}