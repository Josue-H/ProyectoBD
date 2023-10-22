document.addEventListener("DOMContentLoaded", function () {
    const alumnoSelect = document.getElementById("alumnoSelect");
    const infoTable = document.getElementById("infoTable");

    alumnoSelect.addEventListener("change", function () {
        const alumnoId = this.value;

        if (alumnoId) {
            // Realiza una solicitud GET al servidor para obtener la información del alumno
            fetch(`/encargado/alumno_info?alumno_id=${alumnoId}`)
                .then((response) => response.json())
                .then((data) => {
                    // Borra el contenido anterior de la tabla
                    infoTable.querySelector("tbody").innerHTML = "";

                    // Itera sobre las asignaciones y agrega cada una a la tabla
                    data.asignaciones.forEach((asignacion) => {
                        const row = document.createElement("tr");
                        const cursoCell = document.createElement("td");
                        cursoCell.textContent = asignacion.curso;
                        row.appendChild(cursoCell);

                        const profesorCell = document.createElement("td");
                        profesorCell.textContent = asignacion.profesor;
                        row.appendChild(profesorCell);

                        const notaCell = document.createElement("td");
                        notaCell.textContent = asignacion.nota;
                        row.appendChild(notaCell);

                        infoTable.querySelector("tbody").appendChild(row);
                    });
                })
                .catch((error) => {
                    console.error("Error al obtener información del alumno:", error);
                });
        } else {
            // Si no se selecciona un alumno, limpia la tabla
            infoTable.querySelector("tbody").innerHTML = "";
        }
    });
});
