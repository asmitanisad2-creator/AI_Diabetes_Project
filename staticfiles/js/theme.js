(function () {
    function applyTheme(theme) {
        const body = document.body;
        const button = document.getElementById("themeButton");
        const isDark = theme === "dark";
        body.classList.toggle("dark-mode", isDark);
        if (button) {
            button.innerHTML = isDark ? "☀️" : "🌙";
            button.setAttribute("aria-label", isDark ? "Switch to light mode" : "Switch to dark mode");
            button.setAttribute("title", isDark ? "Light mode" : "Dark mode");
        }
    }

    window.toggleTheme = function () {
        const isDark = document.body.classList.contains("dark-mode");
        const nextTheme = isDark ? "light" : "dark";
        localStorage.setItem("theme", nextTheme);
        applyTheme(nextTheme);
    };

    document.addEventListener("DOMContentLoaded", function () {
        const saved = localStorage.getItem("theme");
        applyTheme(saved === "dark" ? "dark" : "light");
    });
})();
