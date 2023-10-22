document.addEventListener("DOMContentLoaded", function () {
    const verNotasForm = document.getElementById("verNotasForm");
    const anadirNotasForm = document.getElementById("anadirNotasForm");
    const alumnoSelect = document.getElementById("alumnoSelect");
    const cursoSelect = document.getElementById("cursoSelect");
    const notaInput = document.getElementById("notaInput");
    const guardarNotaBtn = document.getElementById("guardarNota");
    const alumnoSelectAnadir = document.getElementById("alumnoSelectAnadir");
    const cursoSelectAnadir = document.getElementById("cursoSelectAnadir");
    

    // Escuchar el evento de cambio en el campo de entrada de nota
    notaInput.addEventListener("input", function () {
        const notaValue = notaInput.value.trim();

        // Verificar si el valor es un número entre 1 y 100
        const isValid = /^\d{1,2}$|^100$/.test(notaValue);

        if (isValid) {
            // Habilitar el botón si la nota es válida
            guardarNotaBtn.disabled = false;
        } else {
            // Deshabilitar el botón si la nota no es válida
            guardarNotaBtn.disabled = true;
        }
    });

    function habilitarBoton() {
        const alumnoSeleccionado = alumnoSelectAnadir.value.trim() !== "";
        const cursoSeleccionado = cursoSelectAnadir.value.trim() !== "";
        const notaIngresada = notaInput.value.trim() !== "";

        guardarNotaBtn.disabled = !(alumnoSeleccionado && cursoSeleccionado && notaIngresada);
    }
    // Variable para rastrear si ya existe una nota ingresada
    let notaIngresada = false;

    
    // Escuchar el evento de cambio en la selección de acción
    document.getElementById("accionSelect").addEventListener("change", function () {
        const accion = this.value;

        // Mostrar u ocultar el formulario correspondiente según la acción
        verNotasForm.style.display = accion === "ver" ? "block" : "none";
        anadirNotasForm.style.display = accion === "anadir" ? "block" : "none";
        habilitarBoton();
        
    });

    // Escuchar el evento de cambio en la selección de alumno en el formulario de ver notas
    alumnoSelect.addEventListener("change", function () {
        const selectedAlumnoId = this.value;

        // Realizar una solicitud AJAX para cargar los cursos y notas del alumno
        fetch('/admin/cargar_cursos', {
            method: 'POST',
            body: new URLSearchParams({
                'alumno_id': selectedAlumnoId
            }),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
        .then((response) => response.json())
        .then((data) => {
            // Actualizar el formulario con los cursos y notas
            actualizarFormulario(data.cursos, data.notas);
        })
        .catch((error) => {
            console.error(error);
        });
    });

    // Escuchar el evento de cambio en la selección de alumno en el formulario de añadir notas
    alumnoSelectAnadir.addEventListener("change", function () {
        const selectedAlumnoId = this.value;

        // Realizar una solicitud AJAX para cargar los cursos y verificar si ya hay una nota ingresada
        fetch('/admin/cargar_cursos', {
            method: 'POST',
            body: new URLSearchParams({
                'alumno_id': selectedAlumnoId
            }),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
        .then((response) => response.json())
        .then((data) => {
            // Actualizar el select de cursos en el formulario de añadir notas
            actualizarCursosAñadir(data.cursos, data.notaIngresada);

            // Actualizar la variable que rastrea si ya existe una nota ingresada
            notaIngresada = data.notaIngresada;
            

        })
        .catch((error) => {
            console.error(error);
        });
    });

    function actualizarFormulario(cursos, notas) {


        // Mostrar las notas o el mensaje "Nota no ingresada" en el formulario de ver notas
        const notasContainer = document.getElementById("notasContainer");
        notasContainer.innerHTML = "";
        if (notas.length > 0) {
            notas.forEach((nota) => {
                const notaElement = document.createElement("p");
                notaElement.textContent = `Curso: ${nota.id_curso}, Nota: ${nota.nota}`;
                notasContainer.appendChild(notaElement);
            });
        } else {
            const notaElement = document.createElement("p");
            notaElement.textContent = "Nota no ingresada";
            notasContainer.appendChild(notaElement);
        }
    }

    function actualizarCursosAñadir(cursos, notaIngresada) {
        // Actualizar el select de cursos en el formulario de añadir notas
        cursoSelectAnadir.innerHTML = "";
        cursos.forEach((curso) => {
            const option = document.createElement("option");
            option.value = curso.id_curso;
            option.textContent = curso.descripcion;
            cursoSelectAnadir.appendChild(option);
        });
    }

    alumnoSelectAnadir.addEventListener("change", habilitarBoton);
    cursoSelectAnadir.addEventListener("change", habilitarBoton);
    notaInput.addEventListener("input", habilitarBoton);


    // Escuchar el evento de clic en el botón de guardar nota
    guardarNotaBtn.addEventListener("click", function () {
        const selectedAlumnoId = alumnoSelectAnadir.value;
        const selectedCursoId = cursoSelectAnadir.value;
        const notaValue = notaInput.value.trim();

        // Realizar una solicitud AJAX para guardar la nota en la base de datos
        fetch('/admin/guardar_nota', {
            method: 'POST',
            body: new URLSearchParams({
                'alumno_id': selectedAlumnoId,
                'curso_id': selectedCursoId,
                'nota': notaValue
            }),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
        .then((response) => response.json())
        .then((data) => {
            // Actualizar la variable que rastrea si ya existe una nota ingresada
            notaIngresada = data.notaIngresada;
            if (data.success) {
                // Notificar al usuario que la nota se ha guardado
                alert("Nota guardada exitosamente.");
            } else {
                // Notificar al usuario que ya existe una nota para el mismo alumno y curso
                alert("Ya existe una nota para el mismo alumno y curso.");
            }

             // Recargar la página   
             location.reload();
        })
        .catch((error) => {
            console.error(error);
        });
    });

});