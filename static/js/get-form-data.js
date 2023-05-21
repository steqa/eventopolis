function getFormData(form) {
    let formData = new FormData()
    const inputs = form.querySelectorAll('input');
    inputs.forEach((input) => {
        formData.append(input.name, input.value);
    });
    return formData;
}
