import React from "react";
import { useNavigate } from "react-router-dom";

export default function StartupCard({
    startup,
    onDelete,
    onEdit,
}) {
    const navigate = useNavigate();

    return (
        <div className="bg-slate-900 rounded-xl p-5 border border-slate-700 hover:border-indigo-500 transition">

            <h2 className="text-xl font-bold text-white">
                {startup.name}
            </h2>

            <p className="text-indigo-400 mt-2">
                {startup.industry}
            </p>

            <p className="text-slate-400 mt-3">
                {startup.description}
            </p>

            <div className="mt-4">
                <span className="bg-indigo-600 px-3 py-1 rounded">
                    {startup.stage}
                </span>
            </div>

            <div className="flex gap-3 mt-6">

                {/* View */}
                <button
                    onClick={() => navigate(`/startup/${startup.id}`)}
                    className="bg-blue-600 px-4 py-2 rounded hover:bg-blue-500"
                >
                    View
                </button>

                {/* Edit */}
                <button
                    onClick={() => onEdit && onEdit(startup)}
                    className="bg-yellow-600 px-4 py-2 rounded hover:bg-yellow-500"
                >
                    Edit
                </button>

                {/* Delete */}
                <button
                    onClick={() => onDelete(startup.id)}
                    className="bg-red-600 px-4 py-2 rounded hover:bg-red-500"
                >
                    Delete
                </button>

            </div>

        </div>
    );
}