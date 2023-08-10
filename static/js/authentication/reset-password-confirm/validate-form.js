function validateForm(form) {
    const passwordInput = form.querySelector('#password1');
    const secondPasswordInput = form.querySelector('#password2');

    const feedback = [
        [passwordInput, validatePassword(passwordInput.value)],
        [secondPasswordInput, validateSecondPassword(secondPasswordInput.value, passwordInput.id, secondPasswordInput.id)]
    ];

    return displayFeedback(feedback);
}