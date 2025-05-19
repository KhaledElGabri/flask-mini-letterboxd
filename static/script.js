const username = localStorage.getItem("username");
const storedUsername = localStorage.getItem("username");
const welcomeMessage = document.querySelector(".welcome-message");
const logoutButton = document.getElementById("logout-btn");
const currentPath = window.location.pathname;

// display a welcome message
function showWelcomeMsg() {
    if (username && welcomeMessage) {
        if (!logoutButton) {
            localStorage.removeItem("username");
            return;
        }
        welcomeMessage.innerHTML = 'Welcome back, <a href="/user/profile">' + username + '</a>';
        welcomeMessage.style.display = "block";
    }
}

// check username in localStorage
function checkLogin() {
    if (storedUsername && !logoutButton) {
        localStorage.removeItem("username");
        if (currentPath !== "/") {
            window.location.replace("/");
        } else {
            window.location.reload();
        }
    }
}

window.addEventListener('DOMContentLoaded', checkLogin);
showWelcomeMsg();