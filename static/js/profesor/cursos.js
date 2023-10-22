document.addEventListener("DOMContentLoaded", function () {
    const cursoSelect = document.getElementById("cursoSelect");
    const seccionFilter = document.getElementById("seccionFilter");
    const alumnosList = document.getElementById("alumnosList");

    cursoSelect.addEventListener("change", function () {
        const selectedCursoId = this.value;
        seccionFilter.value = "";
        const selectedSeccion = seccionFilter.value;

        fetch('/profesor/obtener_secciones', {
            method: 'POST',
            body: new URLSearchParams({
                'curso_id': selectedCursoId,
            }),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
        .then(response => response.json())
        .then(data => {
            seccionFilter.innerHTML = "";
            const optionAllSecciones = document.createElement("option");
            optionAllSecciones.value = "";
            optionAllSecciones.textContent = "Todas las secciones";
            seccionFilter.appendChild(optionAllSecciones);

            data.secciones.forEach(seccion => {
                const optionSeccion = document.createElement("option");
                optionSeccion.value = seccion;
                optionSeccion.textContent = seccion;
                seccionFilter.appendChild(optionSeccion);
            });

            obtenerYMostrarAlumnos(selectedCursoId, selectedSeccion);
        });
    });

    seccionFilter.addEventListener("change", function () {
        const selectedCursoId = cursoSelect.value;
        const selectedSeccion = this.value;

        obtenerYMostrarAlumnos(selectedCursoId, selectedSeccion);
    });

    function obtenerYMostrarAlumnos(cursoId, seccion) {

        fetch('/profesor/obtener_alumnos_filtrados', {
            method: 'POST',
            body: new URLSearchParams({
                'curso_id': cursoId,
                'seccion': seccion
            }),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
        .then(response => response.json())
        .then(data => {
            alumnosList.innerHTML = "";

            data.alumnos.forEach(alumno => {
                const row = document.createElement("tr");
                const alumnoCell = document.createElement("td");
                alumnoCell.textContent = `${alumno.nombre} ${alumno.apellido}`;
                const gradoCell = document.createElement("td");
                console.log(alumno.grado , "  ",alumno.seccion)
                gradoCell.textContent = alumno.grado;
                const seccionCell = document.createElement("td");
                seccionCell.textContent = alumno.seccion;

                row.appendChild(alumnoCell);
                row.appendChild(gradoCell);
                row.appendChild(seccionCell);

                alumnosList.appendChild(row);
            });
        });
    }
});
