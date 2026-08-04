import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { api } from "../services/api";

export default function StartupDetails() {
    const { id } = useParams();
    const navigate = useNavigate();

    const [startup, setStartup] = useState(null);
    const [loading, setLoading] = useState(true);

    const [analysis, setAnalysis] = useState("");
    const [competitorAnalysis, setCompetitorAnalysis] = useState("");
    const [businessModel, setBusinessModel] = useState("");
    const [pitchDeck, setPitchDeck] = useState("");
    const [financialProjection, setFinancialProjection] = useState("");
    const [investorReadiness, setInvestorReadiness] = useState("");
    const [goToMarket, setGoToMarket] = useState("");

    const [analyzing, setAnalyzing] = useState(false);

    useEffect(() => {
        loadStartup();
    }, []);

    const loadStartup = async () => {
        try {
            const data = await api.startups.get(id);
            setStartup(data);
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleAnalyze = async () => {
        try {
            setAnalyzing(true);

            const result = await api.analyze.startup(id);

            setAnalysis(result.analysis);
        } catch (err) {
            console.error(err);
            alert("Failed to analyze startup");
        } finally {
            setAnalyzing(false);
        }
    };

    const handleCompetitorAnalysis = async () => {
        try {
            setAnalyzing(true);

            const result = await api.analyze.competitor(id);

            setCompetitorAnalysis(result.competitor_analysis);
        } catch (err) {
            console.error(err);
            alert("Failed to analyze competitors");
        } finally {
            setAnalyzing(false);
        }
    };

    const handleBusinessModel = async () => {
        try {
            setAnalyzing(true);

            const result = await api.analyze.businessModel(id);

            setBusinessModel(result.business_model_canvas);
        } catch (err) {
            console.error(err);
            alert("Failed to generate Business Model Canvas");
        } finally {
            setAnalyzing(false);
        }
    };
    const handlePitchDeck = async () => {
        try {
            setAnalyzing(true);

            const result = await api.analyze.pitchDeck(id);

            setPitchDeck(result.pitch_deck);
        } catch (err) {
            console.error(err);
            alert("Failed to generate Pitch Deck");
        } finally {
            setAnalyzing(false);
        }
    };

    const handleFinancialProjection = async () => {
        try {
            setAnalyzing(true);

            const result = await api.analyze.financialProjection(id);

            setFinancialProjection(result.financial_projection);
        } catch (err) {
            console.error(err);
            alert("Failed to generate Financial Projection");
        } finally {
            setAnalyzing(false);
        }
    };
    const handleInvestorReadiness = async () => {
        try {
            setAnalyzing(true);

            const result = await api.analyze.investorReadiness(id);

            setInvestorReadiness(result.investor_readiness);
        } catch (err) {
            console.error(err);
            alert("Failed to generate Investor Readiness");
        } finally {
            setAnalyzing(false);
        }
    };
    const handleGoToMarket = async () => {
        try {
            setAnalyzing(true);

            const result = await api.analyze.goToMarket(id);

            setGoToMarket(result.go_to_market);
        } catch (err) {
            console.error(err);
            alert("Failed to generate Go-To-Market Strategy");
        } finally {
            setAnalyzing(false);
        }
    };
    const handleDownloadPDF = async () => {
        try {
            await api.analyze.downloadReport(id);
        } catch (err) {
            console.error(err);
            alert("Failed to download PDF");
        }
    };
    if (loading) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-slate-950 text-white">
                Loading...
            </div>
        );
    }

    if (!startup) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-slate-950 text-white">
                Startup not found.
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-slate-950 text-white p-10">
            <h1 className="text-5xl font-bold text-indigo-400 mb-8">
                {startup.name}
            </h1>

            <div className="bg-slate-900 rounded-xl p-8 border border-slate-800">
                <div className="grid grid-cols-2 gap-8">
                    <div>
                        <h3 className="text-gray-400 mb-2">Industry</h3>
                        <p className="text-xl">{startup.industry}</p>
                    </div>

                    <div>
                        <h3 className="text-gray-400 mb-2">Stage</h3>
                        <p className="text-xl">{startup.stage}</p>
                    </div>

                    <div className="col-span-2">
                        <h3 className="text-gray-400 mb-2">Target Audience</h3>
                        <p>{startup.target_audience}</p>
                    </div>

                    <div className="col-span-2">
                        <h3 className="text-gray-400 mb-2">Description</h3>
                        <p>{startup.description}</p>
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-10">

                <button
                    onClick={handleAnalyze}
                    disabled={analyzing}
                    className="w-full bg-indigo-600 hover:bg-indigo-500 py-3 rounded-lg font-semibold transition"
                >
                    🤖 Analyze with AI
                </button>

                <button
                    onClick={handleCompetitorAnalysis}
                    disabled={analyzing}
                    className="w-full bg-green-600 hover:bg-green-500 py-3 rounded-lg font-semibold transition"
                >
                    🏆 Competitor Analysis
                </button>

                <button
                    onClick={handleBusinessModel}
                    disabled={analyzing}
                    className="w-full bg-purple-600 hover:bg-purple-500 py-3 rounded-lg font-semibold transition"
                >
                    📊 Business Model Canvas
                </button>

                <button
                    onClick={handlePitchDeck}
                    disabled={analyzing}
                    className="w-full bg-pink-600 hover:bg-pink-500 py-3 rounded-lg font-semibold transition"
                >
                    🎤 Generate Pitch Deck
                </button>
                <button
                    onClick={handleFinancialProjection}
                    disabled={analyzing}
                    className="bg-yellow-600 hover:bg-yellow-500 px-8 py-3 rounded-lg font-semibold"
                >
                    {analyzing ? "Generating..." : "💰 Financial Projection"}
                </button>
                <button
                    onClick={handleInvestorReadiness}
                    disabled={analyzing}
                    className="bg-cyan-600 hover:bg-cyan-500 px-8 py-3 rounded-lg font-semibold"
                >
                    {analyzing ? "Generating..." : "🎯 Investor Readiness"}
                </button>
                <button
                    onClick={handleGoToMarket}
                    disabled={analyzing}
                    className="bg-emerald-600 hover:bg-emerald-500 px-8 py-3 rounded-lg font-semibold"
                >
                    {analyzing ? "Generating..." : "📈 Go-To-Market Strategy"}
                </button>
                <button
                    onClick={handleDownloadPDF}
                    className="bg-red-600 hover:bg-red-500 px-8 py-3 rounded-lg font-semibold"
                >
                    📄 Download PDF Report
                </button>
                <button
                    onClick={() => navigate(`/mentor/${id}`)}
                    className="w-full bg-blue-600 hover:bg-blue-500 py-3 rounded-lg font-semibold"
                >
                    💬 AI Mentor Chat
                </button>

                <button
                    onClick={() => navigate("/dashboard")}
                    className="w-full bg-slate-700 hover:bg-slate-600 py-3 rounded-lg font-semibold transition"
                >
                    ← Back to Dashboard
                </button>

            </div>

            {analysis && (
                <div className="mt-10 bg-slate-900 border border-slate-700 rounded-xl p-6">
                    <h2 className="text-2xl font-bold text-indigo-400 mb-4">
                        🤖 AI Analysis
                    </h2>

                    <pre className="whitespace-pre-wrap text-gray-300">
                        {analysis}
                    </pre>
                </div>
            )}

            {competitorAnalysis && (
                <div className="mt-10 bg-slate-900 border border-green-700 rounded-xl p-6">
                    <h2 className="text-2xl font-bold text-green-400 mb-4">
                        🏆 Competitor Analysis
                    </h2>

                    <pre className="whitespace-pre-wrap text-gray-300">
                        {competitorAnalysis}
                    </pre>
                </div>
            )}

            {businessModel && (
                <div className="mt-10 bg-slate-900 border border-purple-700 rounded-xl p-6">
                    <h2 className="text-2xl font-bold text-purple-400 mb-4">
                        📊 Business Model Canvas
                    </h2>

                    <pre className="whitespace-pre-wrap text-gray-300">
                        {businessModel}
                    </pre>
                </div>
            )}
            {pitchDeck && (
                <div className="mt-10 bg-slate-900 border border-pink-700 rounded-xl p-6">
                    <h2 className="text-2xl font-bold text-pink-400 mb-4">
                        🎤 AI Pitch Deck
                    </h2>

                    <pre className="whitespace-pre-wrap text-gray-300">
                        {pitchDeck}
                    </pre>
                </div>
            )}
            {financialProjection && (
                <div className="mt-10 bg-slate-900 border border-yellow-700 rounded-xl p-6">
                    <h2 className="text-2xl font-bold text-yellow-400 mb-4">
                        💰 Financial Projection
                    </h2>

                    <pre className="whitespace-pre-wrap text-gray-300">
                        {financialProjection}
                    </pre>
                </div>
            )}
            {investorReadiness && (
                <div className="mt-10 bg-slate-900 border border-cyan-700 rounded-xl p-6">
                    <h2 className="text-2xl font-bold text-cyan-400 mb-4">
                        🎯 Investor Readiness
                    </h2>

                    <pre className="whitespace-pre-wrap text-gray-300">
                        {investorReadiness}
                    </pre>
                </div>
            )}
            {goToMarket && (
                <div className="mt-10 bg-slate-900 border border-emerald-700 rounded-xl p-6">
                    <h2 className="text-2xl font-bold text-emerald-400 mb-4">
                        📈 Go-To-Market Strategy
                    </h2>

                    <pre className="whitespace-pre-wrap text-gray-300">
                        {goToMarket}
                    </pre>
                </div>
            )}
        </div>
    );
}