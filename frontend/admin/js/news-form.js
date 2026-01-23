import { apiFetch } from "../../shared/js/api.js";
import { requireAuth } from "../../shared/js/auth.js";

requireAuth();

document.addEventListener("DOMContentLoaded", async () => {
    const form = document.getElementById("news-form");
    const params = new URLSearchParams(window.location.search);
    const id = params.get("id");

    if (id) {
        const data = await apiFetch("/admin/news");
        const news = data.items.find(n => n.id === Number(id));

        if (!news) {
            alert("Noticia no encontrada");
            window.location.href = "dashboard.html";
            return;
        }

        form.title.value = news.title;
        form.summary.value = news.summary;
        form.content.value = news.content;
    }

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const submitBtn = form.querySelector("button[type='submit']");
        submitBtn.disabled = true;
        submitBtn.textContent = "Guardando…";

        const payload = {
            title: form.title.value,
            summary: form.summary.value,
            content: form.content.value
        };

        try {
            if (id) {
                await apiFetch(`/admin/news/${id}`, {
                    method: "PUT",
                    body: JSON.stringify(payload)
                });
            } else {
                await apiFetch("/admin/news", {
                    method: "POST",
                    body: JSON.stringify(payload)
                });
            }

            alert("Noticia guardada correctamente");
            window.location.href = "dashboard.html";

        } catch (err) {
            console.error(err);
            alert("Error guardando noticia");

            submitBtn.disabled = false;
            submitBtn.textContent = "Guardar";
        }
    });
});
