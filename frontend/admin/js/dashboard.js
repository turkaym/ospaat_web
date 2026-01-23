import { apiFetch } from "../../shared/js/api.js";
import { requireAuth, logout } from "../../shared/js/auth.js";

requireAuth();

document.addEventListener("DOMContentLoaded", async () => {
    const tableBody = document.getElementById("news-table-body");
    const logoutBtn = document.getElementById("logout-btn");

    logoutBtn.addEventListener("click", logout);

    try {
        const data = await apiFetch("/admin/news");

        tableBody.innerHTML = "";

        data.items.forEach(news => {
            const tr = document.createElement("tr");

            tr.innerHTML = `
                <td>${news.title}</td>
                <td>${news.is_published ? "Publicada" : "Borrador"}</td>
                <td>${news.is_deleted ? "Eliminada" : "Activa"}</td>
                <td>
                    <a href="news-form.html?id=${news.id}">Editar</a>

                    ${!news.is_deleted ? `
                        <button data-delete="${news.id}">Eliminar</button>
                        <button data-publish="${news.id}" data-value="${!news.is_published}">
                            ${news.is_published ? "Despublicar" : "Publicar"}
                        </button>
                    ` : `
                        <button data-restore="${news.id}">Restaurar</button>
                    `}
                </td>
            `;

            tableBody.appendChild(tr);
        });

        tableBody.addEventListener("click", async (e) => {
            if (e.target.dataset.delete) {
                const id = e.target.dataset.delete;

                const ok = confirm("¿Seguro que querés eliminar esta noticia?");
                if (!ok) return;

                await apiFetch(`/admin/news/${id}`, { method: "DELETE" });
                location.reload();
            }

            if (e.target.dataset.restore) {
                await apiFetch(`/admin/news/${e.target.dataset.restore}/restore`, {
                    method: "POST"
                });
                location.reload();
            }

            if (e.target.dataset.publish) {
                const id = e.target.dataset.publish;
                const value = e.target.dataset.value === "true";

                const msg = value
                    ? "¿Publicar esta noticia?"
                    : "¿Despublicar esta noticia?";

                const ok = confirm(msg);
                if (!ok) return;

                await apiFetch(`/admin/news/${id}/publish`, {
                    method: "PATCH",
                    body: JSON.stringify({ is_published: value })
                });

                location.reload();
            }

        });

    } catch (err) {
        tableBody.innerHTML = `<tr><td colspan="4">Error cargando noticias</td></tr>`;
    }
});
