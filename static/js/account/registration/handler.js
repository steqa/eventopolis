const registrationForm = document.getElementById('registration-form');

registrationForm.addEventListener('submit', function (event) {
    event.preventDefault();
    const valid = validateRegistrationForm(this);
    if (valid) {
        console.log('POST');
    }
});