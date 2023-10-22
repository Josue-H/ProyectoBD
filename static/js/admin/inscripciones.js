document.addEventListener("DOMContentLoaded", function () {
    const userForms = document.querySelectorAll(".form-container"); // Todos los formularios
    const submitButtons = document.querySelectorAll(".submit-button"); // Todos los botones
    // Mostrar el formulario correspondiente al hacer clic en un botón del menú
    const btnInscripciones = document.getElementById("btnInscripciones");
    const btnAsignaciones = document.getElementById("btnAsignaciones");
    const btnColegiaturas = document.getElementById("btnColegiaturas");

    const formInscripciones = document.getElementById("formInscripciones");
    const formAsignaciones = document.getElementById("formAsignaciones");
    const formColegiaturas = document.getElementById("formColegiaturas");

    // Deshabilitar todos los botones al principio
    submitButtons.forEach(function (button) {
        button.disabled = true;
    });

    // Agregar oyentes de eventos a todos los campos de formulario
    const formFields = document.querySelectorAll(".form-container input, .form-container select");
    formFields.forEach(function (field) {
        field.addEventListener("input", validateForm);
    });

    function validateForm() {
        const activeForm = document.querySelector(".form-container[style='display: block;']");
        const formFields = activeForm.querySelectorAll("input, select");
        let isFormValid = true;

        formFields.forEach(function (field) {
            if (field.value.trim() === "" || (field.tagName === "SELECT" && field.selectedIndex === 0)) {
                isFormValid = false;
            }
        });

        // Habilitar o deshabilitar todos los botones según si el formulario es válido
        submitButtons.forEach(function (button) {
            button.disabled = !isFormValid;
        });
    }



    btnInscripciones.addEventListener("click", () => {
        userForms.forEach(form => form.style.display = "none");
        formInscripciones.style.display = "block";
        validateForm();
    });

    btnAsignaciones.addEventListener("click", () => {
        userForms.forEach(form => form.style.display = "none");
        formAsignaciones.style.display = "block";
        validateForm();
    });

    btnColegiaturas.addEventListener("click", () => {
        userForms.forEach(form => form.style.display = "none");
        formColegiaturas.style.display = "block";
        validateForm();
    });
});
