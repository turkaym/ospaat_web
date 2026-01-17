document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("news-list");

    fetch("http://127.0.0.1:8000/news")
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
        })
        .catch(err => {
            console.error(err);
            container.innerHTML = "<p>Error al cargar las noticias.</p>";
        });
});
