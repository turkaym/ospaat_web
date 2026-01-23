export function requireAuth() {
    const token = localStorage.getItem("token");

    if (!token || token.split(".").length !== 3) {
        localStorage.removeItem("token");
        window.location.href = "/frontend/admin/pages/login.html";
    }
}


export function logout() {
    localStorage.removeItem("token");
    sessionStorage.clear();
    window.location.replace("/frontend/admin/pages/login.html");
}

