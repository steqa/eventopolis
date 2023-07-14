const modalForm = document.getElementById('modalForm');

modalForm.addEventListener('submit', function (event) {
    event.preventDefault();
    const valid = validateModalForm(this);
    if (valid) {
        sendFormData(this);
    }
});