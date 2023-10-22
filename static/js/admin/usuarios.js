document.addEventListener("DOMContentLoaded", function () {
    const rolSelect = document.getElementById("rolSelect");
    const userForms = document.querySelectorAll(".user-form"); // Todos los formularios
    const submitButtons = document.querySelectorAll(".submit-button"); // Todos los botones

    // Deshabilitar todos los botones al principio
    submitButtons.forEach(function (button) {
        button.disabled = true;
    });

    rolSelect.addEventListener("change", function () {
        const selectedRolId = parseInt(rolSelect.value);

        // Ocultar todos los formularios
        userForms.forEach(function (form) {
            form.style.display = "none";
        });

        // Mostrar el formulario correspondiente según el rol seleccionado
        let activeForm;

        if (selectedRolId === 1) { // Administrador
            activeForm = document.getElementById("administrador-form");
        } else if (selectedRolId === 2) { // Alumno
            activeForm = document.getElementById("alumno-form");
        } else if (selectedRolId === 3) { // Profesor
            activeForm = document.getElementById("profesor-form");
        }else if (selectedRolId === 4){
            activeForm = document.getElementById('encargado-form')
        }

        if (activeForm) {
            activeForm.style.display = "block";

            // Agregar oyentes de eventos a todos los campos del formulario activo
            const formFields = activeForm.querySelectorAll("input, select");
            formFields.forEach(function (field) {
                field.addEventListener("input", validateForm);
            });

            // Validar el formulario inicialmente
            validateForm();
        }
    });

    function validateForm() {
        const activeForm = document.querySelector(".user-form[style='display: block;']");
        const formFields = activeForm.querySelectorAll("input, select");
        let isFormValid = true;

        formFields.forEach(function (field) {
            if (field.value.trim() === "" || (field.type === "select-one" && field.value === "")) {
                isFormValid = false;
            }
        });

        // Habilitar o deshabilitar todos los botones según si el formulario es válido
        submitButtons.forEach(function (button) {
            button.disabled = !isFormValid;
        });
    }
});
