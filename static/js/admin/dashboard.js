document.getElementById("menu-button").addEventListener("click", function() {
    var menuContainer = document.querySelector(".menu-container");
    var buttonContainer = document.querySelector(".menu-button-container");
    var isOpen = menuContainer.classList.contains("open");

    if (isOpen) {
        menuContainer.classList.remove("open");
        buttonContainer.style.left = "10px"; // Ajusta la posición a la izquierda
    } else {
        menuContainer.classList.add("open");
        buttonContainer.style.left = "260px"; // Ajusta la posición a la derecha
    }
});
