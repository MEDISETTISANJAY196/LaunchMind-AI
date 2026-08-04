import { useEffect, useState } from "react";
import MainLayout from "../components/layout/MainLayout";
import { api } from "../services/api";

export default function AISettings() {
    const [apiKey, setApiKey] = useState("");
    const [configured, setConfigured] = useState(false);
    const [loading, setLoading] = useState(false);

    const loadStatus = async () => {
        try {
            const data = await api.settings.getStatus();

            console.log("Status Response:", data);

            setConfigured(data.configured);
        } catch (err) {
            console.error(err);
        }
    };

    useEffect(() => {
        loadStatus();
    }, []);

    const saveKey = async () => {
        if (!apiKey.trim()) {
            alert("Please enter Gemini API Key");
            return;
        }

        try {
            setLoading(true);
            await api.settings.saveGeminiKey(apiKey);
            alert("Gemini API Key saved successfully");
            setApiKey("");
            await loadStatus();
        } catch (err) {
            alert(err.message);
        } finally {
            setLoading(false);
        }
    };

    const deleteKey = async () => {
        try {
            await api.settings.deleteGeminiKey();
            alert("Gemini API Key deleted successfully");
            setApiKey("");
            await loadStatus();
        } catch (err) {
            alert(err.message);
        }
    };

    return (
        <MainLayout>
            <div className="max-w-2xl mx-auto bg-white rounded-xl shadow-lg p-8 mt-6">
                <h1 className="text-3xl font-bold mb-6">AI Settings</h1>

                <label className="block text-sm font-medium mb-2">
                    Gemini API Key
                </label>

                <input
                    type="password"
                    value={apiKey}
                    onChange={(e) => setApiKey(e.target.value)}
                    placeholder="Paste your Gemini API Key"
                    className="w-full border border-gray-300 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />

                <div className="flex gap-4 mt-6">
                    <button
                        onClick={saveKey}
                        disabled={loading}
                        className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg"
                    >
                        {loading ? "Saving..." : "Save"}
                    </button>

                    <button
                        onClick={deleteKey}
                        className="bg-red-600 hover:bg-red-700 text-white px-6 py-2 rounded-lg"
                    >
                        Delete
                    </button>
                </div>

                <div className="mt-6">
                    {configured ? (
                        <p className="text-green-600 font-semibold">
                            ✅ Gemini API Key Configured
                        </p>
                    ) : (
                        <p className="text-red-600 font-semibold">
                            ❌ Gemini API Key Not Configured
                        </p>
                    )}
                </div>
            </div>
        </MainLayout>
    );
}