# OSP AAT – Institutional Website

This project is an institutional website developed for **OSP AAT (Obra Social del Personal de la Actividad del Turf)**.

The main goal of the website is to provide clear institutional information and to act as the **official communication channel** through a news and announcements system managed by an admin panel.

---

## 🧩 Project Overview

The website includes:

- Public institutional pages
- A news section for official announcements
- A private admin panel for managing news content
- Secure authentication using JWT
- A scalable backend architecture

---

## 📄 Public Pages

- **Home** – Institutional presentation and highlights
- **About Us** – History, mission, and values
- **Plans** – Available health plans
- **Services** – Medical services and procedures
- **News** – Official announcements and communications

---

## 🔐 Admin Panel

The admin panel allows authorized users to:

- Log in securely
- Create news articles
- Edit existing news
- Publish / unpublish content
- Delete news
- Log out securely

Only authenticated administrators can access this panel.

---

## 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3
- Vanilla JavaScript

### Backend
- Python
- FastAPI
- MySQL
- JWT Authentication

---

## 📁 Project Structure

ospaat_web/
│
├── README.md
├── .gitignore
├── .env.example
│
├── backend/
│   ├── .venv/
│   ├── .env
│   ├── requirements.txt
│   ├── main.py
│   │
│   └── app/
│       ├── __init__.py
│       │
│       ├── core/
│       │   ├── config.py
│       │   ├── security.py
│       │   └── database.py
│       │
│       ├── models/
│       │   ├── __init__.py
│       │   ├── user.py
│       │   └── news.py
│       │
│       ├── schemas/
│       │   ├── __init__.py
│       │   ├── user.py
│       │   └── news.py
│       │
│       ├── routers/
│       │   ├── __init__.py
│       │   ├── auth.py
│       │   ├── news.py
│       │   └── admin_news.py
│       │
│       ├── services/
│       │   ├── __init__.py
│       │   └── news_service.py
│       │
│       └── utils/
│           ├── __init__.py
│           └── jwt.py
│
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   ├── nosotros.html
│   │   ├── planes.html
│   │   ├── servicios.html
│   │   ├── noticias.html
│   │   └── noticia.html
│   │
│   ├── admin/
│   │   ├── login.html
│   │   └── dashboard.html
│   │
│   ├── css/
│   │   ├── main.css
│   │   └── admin.css
│   │
│   └── js/
│       ├── main.js
│       ├── noticias.js
│       ├── noticia.js
│       ├── admin_login.js
│       └── admin_dashboard.js
│
└── docs/
    └── arquitectura.md
