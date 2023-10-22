document.addEventListener("DOMContentLoaded", function () {
    const profesorSelect = document.getElementById("profesor");
    const gradoFilter = document.getElementById("gradoFilter");
    const seccionFilter = document.getElementById("seccionFilter");
    const profesoresCursosList = document.getElementById("profesoresCursosList");

    function obtenerCursos(selectedProfesorId) {
        // Realizar una solicitud AJAX para obtener datos de profesores y cursos
        // Incluye los parámetros de filtro según las selecciones en gradoFilter y seccionFilter
        fetch('/admin/obtener_cursos', {
            method: 'POST',
            body: new URLSearchParams({
                'profesor_id': selectedProfesorId,
                'grado_filter': gradoFilter.value,
                'seccion_filter': seccionFilter.value
            }),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
        .then((response) => response.json())
        .then((data) => {
            // Actualizar la tabla con los datos recibidos
            actualizarTablaDeProfesoresYCursos(data); 
        })
        .catch((error) => {
            console.error(error);
        });
    }

    // Escuchar el evento de cambio en el select de profesores
    profesorSelect.addEventListener("change", function () {

        const selectedProfesorId = profesorSelect.value;

        if (selectedProfesorId == ""){
            profesoresCursosList.innerHTML = "";
        }

       fetch('/admin/obtener_cursos', {
            method: 'POST',
            body: new URLSearchParams({
                'profesor_id': selectedProfesorId,
                'grado_filter': gradoFilter.value,
                'seccion_filter': seccionFilter.value
            }),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
        .then((response) => response.json())
        .then((data) => {
          // Actualizar el formulario con los cursos y secciones
            actualizarFormulario(data)
            // Actualizar la tabla con los datos recibidos
            obtenerCursos(selectedProfesorId);  
          
        })
        .catch((error) => {
            console.error(error);
        });
    });

    // Escuchar el evento de cambio en los filtros de grado y sección
    gradoFilter.addEventListener("change", function () {
        // Al cambiar el filtro, realiza una nueva solicitud AJAX con el profesor seleccionado
        const selectedProfesorId = profesorSelect.value;
            // Realiza la solicitud AJAX con los filtros seleccionados
            obtenerCursos(selectedProfesorId);
    });

    seccionFilter.addEventListener("change", function () {
        // Al cambiar el filtro, realiza una nueva solicitud AJAX con el profesor seleccionado
        const selectedProfesorId = profesorSelect.value;
            // Realiza la solicitud AJAX con los filtros seleccionados
        obtenerCursos(selectedProfesorId);
    });

    function actualizarFormulario(data) {
        gradoFilter.innerHTML = "";
        seccionFilter.innerHTML = "";

        const optionAllGrados = document.createElement("option");
        optionAllGrados.value = "";
        optionAllGrados.textContent = "Todos los grados";
        gradoFilter.appendChild(optionAllGrados);

        const optionAllSecciones = document.createElement("option");
        optionAllSecciones.value = "";
        optionAllSecciones.textContent = "Todas las secciones";
        seccionFilter.appendChild(optionAllSecciones);

        const uniqueGrados = new Set();
        const uniqueSecciones = new Set();

        data.forEach((item) => {
            const grado = item.grado;
            const seccion = item.seccion;

            if (!uniqueGrados.has(grado)) {
                uniqueGrados.add(grado);
                const optionGrado = document.createElement("option");
                optionGrado.value = grado;
                optionGrado.textContent = grado;
                gradoFilter.appendChild(optionGrado);
            }

            if (!uniqueSecciones.has(seccion)) {
                uniqueSecciones.add(seccion);
                const optionSeccion = document.createElement("option");
                optionSeccion.value = seccion;
                optionSeccion.textContent = seccion;
                seccionFilter.appendChild(optionSeccion);
            }
        });
    }
    

    // Función para actualizar la tabla con los datos de profesores y cursos
    function actualizarTablaDeProfesoresYCursos(data) {
        profesoresCursosList.innerHTML = ""; // Limpiar la tabla antes de actualizar

        // Recorre los datos y agrega filas a la tabla
        data.forEach((item) => {
            const row = document.createElement("tr");
            const profesorCell = document.createElement("td");
            profesorCell.textContent = item.profesor;
            const cursoCell = document.createElement("td");
            cursoCell.textContent = item.curso;
            const gradoCell = document.createElement("td");
            gradoCell.textContent = item.grado;
            const seccionCell = document.createElement("td");
            seccionCell.textContent = item.seccion;

            row.appendChild(profesorCell);
            row.appendChild(cursoCell);
            row.appendChild(gradoCell);
            row.appendChild(seccionCell);

            profesoresCursosList.appendChild(row);
        });
    }
});
