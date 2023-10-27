document.addEventListener("DOMContentLoaded", function () {
    const cursoSelect = document.getElementById("cursoSelect");
    const alumnoSelect = document.getElementById("alumnoSelect");
    const notaInput = document.getElementById("nota_valor");
    const notaAnteriorInput = document.getElementById("nota-anterior-input");
    const notaAnteriorLabel = document.getElementById("nota-anterior-label");
    const notaBtn = document.getElementById("addNoteButton");


    cursoSelect.addEventListener("change", function () {
        const curso_id = this.value;
        notaAnteriorLabel.style.display = "none"
        notaAnteriorInput.style.display = "none";
        notaAnteriorInput.value = "";
        console.log(curso_id);
        // Realiza una solicitud AJAX a la ruta específica para obtener la lista de alumnos
        fetch('/profesor/obtener_alumnos', {
            method: 'POST',
            body: new URLSearchParams({ 
                'curso_id': curso_id
            }),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
        .then(response => response.json())
        .then(data => {
            // Borra el campo de selección de alumnos
            while (alumnoSelect.firstChild) {
                alumnoSelect.removeChild(alumnoSelect.firstChild);
            }
            const optionAllSelect = document.createElement('option');
            optionAllSelect.value = "";
            optionAllSelect.textContent = "Todos los alumnos"
            alumnoSelect.appendChild(optionAllSelect);
            // Llena el campo de selección de alumnos con los resultados
            data.alumnos.forEach(alumno => {
                const option = document.createElement("option");
                option.value = alumno.id_alumno;
                option.textContent = `${alumno.nombre} ${alumno.apellido}`;
                alumnoSelect.appendChild(option);
            });
        });
    });

    alumnoSelect.addEventListener("change", function () {
        const alumno_id = this.value;
        const curso_id = cursoSelect.value;
        notaAnteriorLabel.style.display = "none"
        notaAnteriorInput.style.display = "none";
        notaAnteriorInput.value = "";
        console.log(alumno_id);

        // Realiza una solicitud AJAX a la ruta específica para obtener la nota del alumno
        fetch('/profesor/obtener_nota',{
            method: 'POST',
            body: new URLSearchParams({
                'curso_id': curso_id,
                'alumno_id': alumno_id
            }),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        })
        .then(response => response.json())
        .then(notaData => {
            // Verifica si el alumno tiene una nota asignada
            console.log(notaData.nota);
            if (notaData.nota !== null) {
                // Si el alumno tiene una nota asignada, muestra la nota y oculta el campo de entrada
                notaBtn.disabled = true
                notaInput.style.display = "none";
                notaAnteriorInput.style.display = "block";
                notaAnteriorLabel.style.display = "block"
                notaAnteriorInput.value = notaData.nota;
            } else {
                // Si el alumno no tiene una nota asignada, muestra el campo de entrada y oculta la nota anterior
                notaBtn.disabled = false
                notaInput.style.display = "block";
                notaAnteriorLabel.style.display = "none"
                notaAnteriorInput.style.display = "none";
                notaAnteriorInput.value = "";
            }
        });
    });
});
