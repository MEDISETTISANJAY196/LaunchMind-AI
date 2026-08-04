import React, { useState } from "react";

export default function CreateStartupModal({
    open,
    onClose,
    onSave,
}) {
    const [form, setForm] = useState({
        name: "",
        industry: "",
        description: "",
        target_audience: "",
        stage: "Ideation",
    });

    if (!open) return null;

    const handleChange = (e) => {
        setForm({
            ...form,
            [e.target.name]: e.target.value,
        });
    };

    const submit = () => {
        onSave(form);

        setForm({
            name: "",
            industry: "",
            description: "",
            target_audience: "",
            stage: "Ideation",
        });
    };

    return (
        <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50">
            <div className="bg-slate-900 p-6 rounded-xl w-[500px] shadow-xl">

                <h2 className="text-2xl font-bold text-white mb-5">
                    Create Startup
                </h2>

                <input
                    className="w-full p-3 mb-3 rounded bg-slate-800 text-white"
                    placeholder="Startup Name"
                    name="name"
                    value={form.name}
                    onChange={handleChange}
                />

                <input
                    className="w-full p-3 mb-3 rounded bg-slate-800 text-white"
                    placeholder="Industry"
                    name="industry"
                    value={form.industry}
                    onChange={handleChange}
                />

                <textarea
                    className="w-full p-3 mb-3 rounded bg-slate-800 text-white"
                    placeholder="Description"
                    name="description"
                    value={form.description}
                    onChange={handleChange}
                />

                <input
                    className="w-full p-3 mb-3 rounded bg-slate-800 text-white"
                    placeholder="Target Audience"
                    name="target_audience"
                    value={form.target_audience}
                    onChange={handleChange}
                />

                <select
                    className="w-full p-3 mb-5 rounded bg-slate-800 text-white"
                    name="stage"
                    value={form.stage}
                    onChange={handleChange}
                >
                    <option value="Ideation">Ideation</option>
                    <option value="MVP">MVP</option>
                    <option value="Startup">Startup</option>
                    <option value="Growth">Growth</option>
                </select>

                <div className="flex justify-end gap-3">

                    <button
                        onClick={onClose}
                        className="px-5 py-2 bg-gray-600 rounded hover:bg-gray-500"
                    >
                        Cancel
                    </button>

                    <button
                        onClick={submit}
                        className="px-5 py-2 bg-indigo-600 rounded hover:bg-indigo-500"
                    >
                        Save Startup
                    </button>

                </div>

            </div>
        </div>
    );
}