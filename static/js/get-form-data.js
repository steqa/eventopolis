function getFormData(form) {
    let formData = new FormData()
    const inputs = form.querySelectorAll('.form-control');
    inputs.forEach((input) => {
        formData.append(input.name, input.value);
    });
    return formData;
}
