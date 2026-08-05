const API_BASE =
  "https://launch-mind-ai-eqtv-tawny.vercel.app/api";

const getHeaders = () => {
  const token = localStorage.getItem("token");



  const headers = {
    "Content-Type": "application/json",
  };

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }



  return headers;
};
export const api = {
  // Authentication
  auth: {
    register: async (email, password, fullName) => {
      const res = await fetch(`${API_BASE}/auth/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email,
          password,
          full_name: fullName,
        }),
      });

      if (!res.ok) throw new Error((await res.json()).detail);

      return res.json();
    },

    login: async (email, password) => {
      const form = new URLSearchParams();
      form.append("username", email);
      form.append("password", password);

      const res = await fetch(`${API_BASE}/auth/login`, {
        method: "POST",
        body: form,
      });

      if (!res.ok) throw new Error((await res.json()).detail);

      return res.json();
    },

    me: async () => {
      const res = await fetch(`${API_BASE}/auth/me`, {
        headers: getHeaders(),
      });

      if (!res.ok) throw new Error("Failed");

      return res.json();
    },
  },

  // Startup CRUD
  startups: {
    list: async () => {
      const res = await fetch(`${API_BASE}/startups/`, {
        headers: getHeaders(),
      });

      if (!res.ok) throw new Error("Failed");

      return res.json();
    },

    create: async (startup) => {
      const res = await fetch(`${API_BASE}/startups/`, {
        method: "POST",
        headers: getHeaders(),
        body: JSON.stringify(startup),
      });

      if (!res.ok) throw new Error("Failed");

      return res.json();
    },

    get: async (id) => {
      const res = await fetch(`${API_BASE}/startups/${id}`, {
        headers: getHeaders(),
      });

      if (!res.ok) throw new Error("Failed");

      return res.json();
    },

    update: async (id, startup) => {
      const res = await fetch(`${API_BASE}/startups/${id}`, {
        method: "PUT",
        headers: getHeaders(),
        body: JSON.stringify(startup),
      });

      if (!res.ok) throw new Error("Failed");

      return res.json();
    },

    delete: async (id) => {
      const res = await fetch(`${API_BASE}/startups/${id}`, {
        method: "DELETE",
        headers: getHeaders(),
      });

      if (!res.ok) throw new Error("Failed");

      return true;
    },
  },
  profile: {
    update: async (fullName) => {
      const res = await fetch(`${API_BASE}/profile/`, {
        method: "PUT",
        headers: getHeaders(),
        body: JSON.stringify({
          full_name: fullName,
        }),
      });

      if (!res.ok) {
        throw new Error("Failed to update profile");
      }

      return res.json();
    },
  },
  password: {
    change: async (currentPassword, newPassword) => {

      const res = await fetch(`${API_BASE}/password/`, {

        method: "PUT",

        headers: getHeaders(),

        body: JSON.stringify({

          current_password: currentPassword,

          new_password: newPassword,

        }),

      });

      if (!res.ok)
        throw new Error((await res.json()).detail);

      return res.json();
    },
  },
  notifications: {
    list: async () => {
      const res = await fetch(`${API_BASE}/notifications/`, {
        headers: getHeaders(),
      });

      if (!res.ok) {
        throw new Error("Failed to load notifications");
      }

      return res.json();
    },
  },

  // SWOT
  swot: {
    get: async (id) => {
      const res = await fetch(`${API_BASE}/swot/startup/${id}`, {
        headers: getHeaders(),
      });

      if (!res.ok) throw new Error("Failed");

      return res.json();
    },

    save: async (startupId, data, generateAi = false) => {
      const res = await fetch(`${API_BASE}/swot/`, {
        method: "POST",
        headers: getHeaders(),
        body: JSON.stringify({
          startup_id: startupId,
          generate_ai: generateAi,
          ...data,
        }),
      });

      if (!res.ok) throw new Error("Failed");

      return res.json();
    },
  },
  profilePhoto: {
    upload: async (file) => {
      const formData = new FormData();

      formData.append("photo", file);

      const token = localStorage.getItem("token");

      const res = await fetch(`${API_BASE}/profile-photo/`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      if (!res.ok) {
        throw new Error("Photo upload failed");
      }

      return res.json();
    },
  },
  // AI Analysis
  analyze: {
    startup: async (id) => {
      const res = await fetch(`${API_BASE}/analyze/${id}`, {
        method: "POST",
        headers: getHeaders(),
      });

      if (!res.ok) {
        throw new Error("Failed to analyze startup");
      }

      return res.json();
    },

    competitor: async (id) => {
      const res = await fetch(`${API_BASE}/analyze/competitor/${id}`, {
        method: "POST",
        headers: getHeaders(),
      });

      if (!res.ok) {
        throw new Error("Failed to analyze competitors");
      }

      return res.json();
    },

    businessModel: async (id) => {
      const res = await fetch(`${API_BASE}/analyze/business-model/${id}`, {
        method: "POST",
        headers: getHeaders(),
      });

      if (!res.ok) {
        throw new Error("Failed to generate Business Model Canvas");
      }

      return res.json();
    },

    pitchDeck: async (id) => {
      const res = await fetch(`${API_BASE}/analyze/pitch-deck/${id}`, {
        method: "POST",
        headers: getHeaders(),
      });

      if (!res.ok) {
        throw new Error("Failed to generate Pitch Deck");
      }

      return res.json();
    },

    financialProjection: async (id) => {
      const res = await fetch(`${API_BASE}/analyze/financial-projection/${id}`, {
        method: "POST",
        headers: getHeaders(),
      });

      if (!res.ok) {
        throw new Error("Failed to generate Financial Projection");
      }

      return res.json();
    },

    investorReadiness: async (id) => {
      const res = await fetch(`${API_BASE}/analyze/investor-readiness/${id}`, {
        method: "POST",
        headers: getHeaders(),
      });

      if (!res.ok) {
        throw new Error("Failed to generate Investor Readiness");
      }

      return res.json();
    },

    goToMarket: async (id) => {
      const res = await fetch(`${API_BASE}/analyze/go-to-market/${id}`, {
        method: "POST",
        headers: getHeaders(),
      });

      if (!res.ok) {
        throw new Error("Failed to generate Go-To-Market Strategy");
      }

      return res.json();
    },

    mentorChat: async (startupId, mentorName, message) => {
      const res = await fetch(`${API_BASE}/mentor/chat`, {
        method: "POST",
        headers: getHeaders(),   // <-- Important
        body: JSON.stringify({
          startup_id: startupId,
          mentor_name: mentorName,
          message: message,
        }),
      });

      if (!res.ok) {
        throw new Error("Failed to chat with mentor");
      }

      return res.json();
    },

    downloadReport: async (id) => {
      const res = await fetch(`${API_BASE}/analyze/download-report/${id}`, {
        method: "GET",
        headers: getHeaders(),
      });

      if (!res.ok) {
        throw new Error("Failed to download PDF");
      }

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);

      const a = document.createElement("a");
      a.href = url;
      a.download = "LaunchMind_Report.pdf";

      document.body.appendChild(a);
      a.click();
      a.remove();

      window.URL.revokeObjectURL(url);
    },
  },
  insights: {
    get: async () => {
      const res = await fetch(`${API_BASE}/insights/`, {
        headers: getHeaders(),
      });

      if (!res.ok) {
        throw new Error("Failed to load AI Insights");
      }

      return res.json();
    },
  },

  // Reports
  reports: {
    list: async (startupId) => {
      const res = await fetch(`${API_BASE}/reports/startup/${startupId}`, {
        headers: getHeaders(),
      });

      if (!res.ok) throw new Error("Failed");

      return res.json();
    },

    generate: async (startupId) => {
      const res = await fetch(`${API_BASE}/reports/generate/${startupId}`, {
        method: "POST",
        headers: getHeaders(),
      });

      if (!res.ok) throw new Error("Failed");

      return res.json();
    },

    downloadUrl: (reportId) => {
      const token = localStorage.getItem("token");
      return `${API_BASE}/reports/download/${reportId}?token=${token}`;
    },
  },

  // Dashboard Analytics
  analytics: {
    dashboard: async () => {
      console.log("TOKEN =", localStorage.getItem("token"));

      const res = await fetch(`${API_BASE}/analytics/dashboard`, {
        headers: getHeaders(),
      });



      if (!res.ok) {
        throw new Error(await res.text());
      }

      return res.json();
    },
  },

  // AI Settings
  settings: {
    saveGeminiKey: async (geminiApiKey) => {
      const res = await fetch(`${API_BASE}/settings/gemini-key`, {
        method: "POST",
        headers: getHeaders(),
        body: JSON.stringify({
          gemini_api_key: geminiApiKey,
        }),
      });

      if (!res.ok) throw new Error("Failed to save Gemini API Key");

      return res.json();
    },

    getStatus: async () => {
      const res = await fetch(`${API_BASE}/settings/gemini-key/status`, {
        headers: getHeaders(),
      });

      if (!res.ok) throw new Error("Failed");

      return res.json();
    },

    deleteGeminiKey: async () => {
      const res = await fetch(`${API_BASE}/settings/gemini-key`, {
        method: "DELETE",
        headers: getHeaders(),
      });

      if (!res.ok) throw new Error("Failed");

      return res.json();
    },
  },
};
