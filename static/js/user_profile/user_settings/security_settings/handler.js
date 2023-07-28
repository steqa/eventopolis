const form = document.getElementById('form');

form.addEventListener('submit', function (event) {
    event.preventDefault();
    const valid = validateForm(this);
    if (valid) {
        sendFormData(this, '?fieldType=slug');
    }
});