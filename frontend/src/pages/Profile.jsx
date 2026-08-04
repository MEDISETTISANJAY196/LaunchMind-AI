import React, { useState } from "react";
import { useAuth } from "../context/AuthContext";
import { api } from "../services/api";
export default function Profile() {
    const { user, setUser } = useAuth();
    console.log(user);
    const [photo, setPhoto] = useState(null);
    const [preview, setPreview] = useState(null);

    const [fullName, setFullName] = useState(user?.full_name || "");
    const [email] = useState(user?.email || "");
    const [currentPassword, setCurrentPassword] = useState("");
    const [newPassword, setNewPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const changePassword = async () => {

        if (newPassword !== confirmPassword) {
            alert("Passwords do not match");
            return;
        }

        try {

            await api.password.change(
                currentPassword,
                newPassword
            );

            alert("Password Updated Successfully!");

            setCurrentPassword("");
            setNewPassword("");
            setConfirmPassword("");

        } catch (err) {
            alert(err.message);
        }

    };
    const handlePhoto = async (e) => {
        const file = e.target.files[0];

        if (!file) return;

        setPreview(URL.createObjectURL(file));

        try {
            await api.profilePhoto.upload(file);

            alert("Photo Uploaded Successfully!");
        } catch (err) {
            alert(err.message);
        }
    };
    const saveProfile = async () => {
        try {
            const result = await api.profile.update(fullName);

            setUser(result.user);

            alert("Profile Updated Successfully!");
        } catch (err) {
            alert(err.message);
        }
    };
    return (
        <div className="min-h-screen bg-slate-950 text-white flex justify-center items-center">

            <div className="bg-slate-900 rounded-xl shadow-xl p-10 w-[450px]">

                <h1 className="text-3xl font-bold text-cyan-400 mb-8">
                    👤 My Profile
                </h1>
                <div className="flex flex-col items-center mb-8">

                    <img
                        src={
                            preview ||
                            `http://127.0.0.1:8000/uploads/profile/user_${user?.id}.jpg`
                        }
                        alt="Profile"
                        className="w-32 h-32 rounded-full object-cover border-4 border-cyan-500"
                    />

                    <label
                        htmlFor="profilePhoto"
                        className="mt-5 cursor-pointer bg-cyan-600 hover:bg-cyan-500 px-5 py-2 rounded-lg"
                    >
                        📷 Upload Photo
                    </label>

                    <input
                        id="profilePhoto"
                        type="file"
                        accept="image/*"
                        onChange={handlePhoto}
                        className="hidden"
                    />

                </div>
                <div className="space-y-5">

                    <div>
                        <label className="block mb-2">Full Name</label>

                        <input
                            type="text"
                            value={fullName}
                            onChange={(e) => setFullName(e.target.value)}
                            className="w-full bg-slate-800 rounded-lg p-3"
                        />
                    </div>

                    <div>
                        <label className="block mb-2">Email</label>

                        <input
                            type="email"
                            value={email}
                            disabled
                            className="w-full bg-slate-800 rounded-lg p-3 opacity-70"
                        />
                    </div>

                    <button
                        onClick={saveProfile}
                        className="w-full bg-cyan-600 hover:bg-cyan-500 py-3 rounded-lg font-semibold"
                    >
                        💾 Save Changes
                    </button>
                    <div className="mt-8 border-t border-slate-700 pt-6">

                        <h2 className="text-2xl font-bold mb-6">
                            🔒 Change Password
                        </h2>

                        <div className="space-y-4">

                            <input
                                type="password"
                                placeholder="Current Password"
                                value={currentPassword}
                                onChange={(e) => setCurrentPassword(e.target.value)}
                                className="w-full bg-slate-800 rounded-lg p-3"
                            />

                            <input
                                type="password"
                                placeholder="New Password"
                                value={newPassword}
                                onChange={(e) => setNewPassword(e.target.value)}
                                className="w-full bg-slate-800 rounded-lg p-3"
                            />

                            <input
                                type="password"
                                placeholder="Confirm Password"
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                                className="w-full bg-slate-800 rounded-lg p-3"
                            />

                            <button
                                onClick={changePassword}
                                className="w-full bg-red-600 hover:bg-red-500 py-3 rounded-lg font-semibold"
                            >
                                🔒 Update Password
                            </button>

                        </div>

                    </div>

                </div>

            </div>

        </div>
    );
}