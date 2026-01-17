document.addEventListener("DOMContentLoaded", () => {
    const params = new URLSearchParams(window.location.search);
    const id = params.get("id");

    const title = document.getElementById("news-title");
    const dateEl = document.getElementById("news-date");
    const content = document.getElementById("news-content");

    title.textContent = "Cargando noticia…";

    if (!id) {
        title.textContent = "Noticia no encontrada";
        return;
    }

    fetch(`http://127.0.0.1:8000/news/${id}`)
        .then(res => {
            if (!res.ok) throw new Error("Not found");
            return res.json();
        })
        .then(news => {
            // SEO dinámico
            document.title = `${news.title} | OSP AAT`;
            const meta = document.querySelector('meta[name="description"]');
            if (meta) meta.setAttribute("content", news.summary || "");

            title.textContent = news.title;
            content.innerHTML = news.content;

            if (news.published_at) {
                dateEl.textContent = new Date(news.published_at)
                    .toLocaleDateString("es-AR");
            }
        })
        .catch(() => {
            title.textContent = "Noticia no encontrada";
            content.innerHTML = "<p>La noticia no existe o no está publicada.</p>";
        });
});
