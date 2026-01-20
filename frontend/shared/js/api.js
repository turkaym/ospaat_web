// frontend/shared/js/api.js

export const API_BASE = "http://127.0.0.1:8000";

export async function apiFetch(endpoint, options = {}) {
    const token = localStorage.getItem("token");

    const headers = {
        "Content-Type": "application/json",
        ...(token && { Authorization: `Bearer ${token}` })
    };

    const response = await fetch(`${API_BASE}${endpoint}`, {
        ...options,
        headers
    });

    if (response.status === 401) {
        localStorage.removeItem("token");

        // Flag para mostrar mensaje
        sessionStorage.setItem("session_expired", "true");

        window.location.href = "/frontend/admin/pages/login.html";
        throw new Error("Unauthorized");
    }


    if (!response.ok) {
        const text = await response.text();
        throw new Error(text || "API error");
    }

    return response.json();
}
