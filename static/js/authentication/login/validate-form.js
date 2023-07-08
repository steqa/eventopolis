function validateForm(form) {
    const emailInput = form.querySelector('#email');
    const passwordInput = form.querySelector('#password');

    const feedback = [
        [emailInput, validateEmail(emailInput.value)],
        [passwordInput, validatePassword(passwordInput.value)],
    ];

    return displayFeedback(feedback);
}