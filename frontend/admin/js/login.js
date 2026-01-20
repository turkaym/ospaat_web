// frontend/admin/js/login.js

import { API_BASE } from "../../shared/js/api.js";

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("login-form");
    const errorBox = document.getElementById("login-error");

    const expired = sessionStorage.getItem("session_expired");
    if (expired) {
        const errorBox = document.getElementById("login-error");
        errorBox.textContent = "Tu sesión expiró. Volvé a iniciar sesión.";
        sessionStorage.removeItem("session_expired");
    }


    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        errorBox.textContent = "";

        const username = form.username.value.trim();
        const password = form.password.value.trim();

        if (!username || !password) {
            errorBox.textContent = "Completa todos los campos";
            return;
        }

        try {
            const res = await fetch(`${API_BASE}/auth/login`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password })
            });

            if (!res.ok) {
                throw new Error("Credenciales inválidas");
            }

            const data = await res.json();
            localStorage.setItem("token", data.access_token);

            window.location.href = "dashboard.html";

        } catch (err) {
            errorBox.textContent = err.message;
        }
    });
});
