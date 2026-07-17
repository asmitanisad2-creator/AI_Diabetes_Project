const themeButton = document.getElementById("themeButton");

// Apply saved theme
window.onload = function () {

    const savedTheme = localStorage.getItem("theme");

    if(savedTheme === "dark"){
        document.body.classList.add("dark-mode");
        document.getElementById("themeButton").innerHTML = "☀️";
    }
    else{
        document.getElementById("themeButton").innerHTML = "🌙";
    }

}

// Toggle Theme

function toggleTheme(){

    document.body.classList.toggle("dark-mode");

    if(document.body.classList.contains("dark-mode")){

        localStorage.setItem("theme","dark");

        document.getElementById("themeButton").innerHTML = "☀️";

    }

    else{

        localStorage.setItem("theme","light");

        document.getElementById("themeButton").innerHTML = "🌙";

    }

}