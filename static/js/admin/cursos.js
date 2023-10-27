document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const btnCrear = document.getElementById("btnCrear");
    const btnAsignar = document.getElementById("btnAsignar");
    const formCrear = document.getElementById("formCrear");
    const formAsignar = document.getElementById("formAsignar");
    const crearCursoButton = document.getElementById("crear_curso");
    const asignarCursoButton = document.getElementById("asignar_curso");
    const flashMessages = document.getElementById("flash-messages");
    // Función para mostrar mensajes flash en una ventana emergente de alerta
    // Función para mostrar mensajes flash en alertas
    function displayFlashMessage(message, type) {
        alert(message);
    }

    // Escuchar mensajes flash y mostrarlos en alertas
    fetch('/admin/cursos', {
        method: 'GET',
    })
    .then((response) => response.json())
    .then((data) => {
        if (data.success) {
            displayFlashMessage("Operación exitosa", "success");
        } else {
            displayFlashMessage("Ocurrió un error", "error");
        }
    })
    .catch((error) => {
        console.error(error);
    });
    

    // Función para comprobar si los campos del formulario activo están completos
    function isFormValid(activeForm) {
        const inputs = activeForm.querySelectorAll("input");
        const selects = activeForm.querySelectorAll("select");

        let isFormValid = true;

        inputs.forEach(function (input) {
            if (input.value.trim() === "") {
                isFormValid = false;
            }
        });

        selects.forEach(function (select) {
            if (select.value.trim() === "") {
                isFormValid = false;
            }
        });

        return isFormValid;
    }

    btnCrear.addEventListener("click", function () {
        // Mostrar el formulario de creación y ocultar el de asignación
        formCrear.style.display = "block";
        formAsignar.style.display = "none";
        // Comprobar la validez del formulario de creación
        crearCursoButton.disabled = !isFormValid(formCrear);
        asignarCursoButton.disabled = true; // Deshabilita el botón de asignación
    });

    btnAsignar.addEventListener("click", function () {
        // Mostrar el formulario de asignación y ocultar el de creación
        formCrear.style.display = "none";
        formAsignar.style.display = "block";
        // Comprobar la validez del formulario de asignación
        asignarCursoButton.disabled = !isFormValid(formAsignar);
        crearCursoButton.disabled = true; // Deshabilita el botón de creación
    });

    // Escuchar cambios en los elementos del formulario activo
    form.addEventListener("input", function () {
        if (formCrear.style.display === "block") {
            crearCursoButton.disabled = !isFormValid(formCrear);
        } else {
            asignarCursoButton.disabled = !isFormValid(formAsignar);
        }
    });

    // Comprueba la validez del formulario al cargar la página
    crearCursoButton.disabled = !isFormValid(formCrear);
    asignarCursoButton.disabled = true; // Inicialmente, solo el botón de creación está habilitado
});
