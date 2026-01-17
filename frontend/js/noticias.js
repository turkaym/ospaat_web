document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("news-list");

    // Estado inicial
    container.innerHTML = "<p>Cargando noticias…</p>";

    const params = new URLSearchParams(window.location.search);
    const page = parseInt(params.get("page") || "1", 10);
    const limit = 6;

    fetch(`http://127.0.0.1:8000/news?page=${page}&limit=${limit}`)
        .then(res => {
            if (!res.ok) throw new Error("Error loading news");
            return res.json();
        })
        .then(data => {
            if (data.items.length === 0) {
                container.innerHTML = "<p>No hay noticias publicadas.</p>";
                return;
            }

            container.innerHTML = "";

            data.items.forEach(news => {
                const article = document.createElement("article");
                article.className = "news-card";

                const date = news.published_at
                    ? new Date(news.published_at).toLocaleDateString("es-AR")
                    : "";

                article.innerHTML = `
                    <h2>${news.title}</h2>
                    <p class="news-date">${date}</p>
                    <p>${news.summary}</p>
                    <a href="noticia.html?id=${news.id}">Leer más</a>
                `;

                container.appendChild(article);
            });

            renderPagination(page, data.count === limit);
        })
        .catch(() => {
            container.innerHTML = "<p>Error al cargar las noticias.</p>";
        });

    function renderPagination(currentPage, hasNext) {
        const nav = document.createElement("div");
        nav.style.marginTop = "2rem";

        if (currentPage > 1) {
            const prev = document.createElement("a");
            prev.href = `?page=${currentPage - 1}`;
            prev.textContent = "← Anteriores";
            prev.style.marginRight = "1rem";
            nav.appendChild(prev);
        }

        if (hasNext) {
            const next = document.createElement("a");
            next.href = `?page=${currentPage + 1}`;
            next.textContent = "Siguientes →";
            nav.appendChild(next);
        }

        container.after(nav);
    }
});
