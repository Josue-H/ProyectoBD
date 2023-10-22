// alumno_dashboard.js

document.addEventListener("DOMContentLoaded", function () {
    const cursoSelect = document.getElementById("cursoSelect");
    const tablaCursos = document.querySelector("table tbody");

    cursoSelect.addEventListener("change", function () {
        const cursoId = this.value;

        // Oculta todas las filas de la tabla
        Array.from(tablaCursos.children).forEach(function (fila) {
            fila.style.display = "none";
        });

        if (cursoId) {
            // Muestra solo las filas correspondientes al curso seleccionado
            const filasFiltradas = document.querySelectorAll(`tr[data-curso="${cursoId}"]`);
            filasFiltradas.forEach(function (fila) {
                fila.style.display = "";
            });
        } else {
            // Si se selecciona "Todos los cursos," muestra todas las filas
            Array.from(tablaCursos.children).forEach(function (fila) {
                fila.style.display = "";
            });
        }
    });
});
