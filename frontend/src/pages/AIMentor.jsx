import React, { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { api } from "../services/api";

export default function AIMentor() {
    const { id } = useParams();
    const navigate = useNavigate();

    const [mentorName] = useState("Startup Mentor");
    const [message, setMessage] = useState("");
    const [chat, setChat] = useState([]);
    const [loading, setLoading] = useState(false);

    const sendMessage = async () => {
        if (!message.trim()) return;

        const userMessage = {
            role: "user",
            content: message,
        };

        setChat((prev) => [...prev, userMessage]);
        setLoading(true);

        try {
            const res = await api.analyze.mentorChat(
                Number(id),
                mentorName,
                message
            );

            const aiMessage = {
                role: "assistant",
                content: res.reply,
            };

            setChat((prev) => [...prev, aiMessage]);
            setMessage("");
        } catch (err) {
            console.error(err);
            alert("Failed to contact AI Mentor");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-slate-950 text-white p-8">

            <div className="flex justify-between items-center mb-6">
                <h1 className="text-4xl font-bold text-blue-400">
                    💬 AI Mentor Chat
                </h1>

                <button
                    onClick={() => navigate(-1)}
                    className="bg-slate-700 hover:bg-slate-600 px-5 py-2 rounded-lg"
                >
                    ← Back
                </button>
            </div>

            <div className="bg-slate-900 rounded-xl p-6 h-[500px] overflow-y-auto border border-slate-800">

                {chat.length === 0 && (
                    <div className="text-center text-slate-400 mt-20">
                        <h2 className="text-2xl mb-3">
                            Welcome to AI Mentor 🚀
                        </h2>

                        <p>
                            Ask anything about your startup,
                            funding, marketing, MVP,
                            pricing, investors or growth.
                        </p>
                    </div>
                )}

                {chat.map((msg, index) => (
                    <div
                        key={index}
                        className={`mb-5 flex ${msg.role === "user"
                                ? "justify-end"
                                : "justify-start"
                            }`}
                    >
                        <div
                            className={`max-w-[75%] p-4 rounded-xl whitespace-pre-wrap ${msg.role === "user"
                                    ? "bg-indigo-600"
                                    : "bg-slate-800 border border-slate-700"
                                }`}
                        >
                            <strong>
                                {msg.role === "user" ? "You" : "AI Mentor"}
                            </strong>

                            <br />

                            {msg.content}
                        </div>
                    </div>
                ))}

                {loading && (
                    <div className="text-slate-400">
                        AI Mentor is typing...
                    </div>
                )}
            </div>

            <div className="flex gap-3 mt-6">

                <input
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    onKeyDown={(e) => {
                        if (e.key === "Enter") {
                            sendMessage();
                        }
                    }}
                    placeholder="Ask your startup question..."
                    className="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-4 py-3 outline-none"
                />

                <button
                    onClick={sendMessage}
                    disabled={loading}
                    className="bg-blue-600 hover:bg-blue-500 px-8 rounded-lg font-semibold"
                >
                    Send
                </button>

            </div>

        </div>
    );
}