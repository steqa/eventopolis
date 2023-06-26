function validateForm(form) {
    const emailInput = form.querySelector('#email');
    const firstNameInput = form.querySelector('#first-name');
    const lastNameInput = form.querySelector('#last-name');
    const passwordInput = form.querySelector('#password1');
    const secondPasswordInput = form.querySelector('#password2');

    const feedback = [
        [emailInput, validateEmail(emailInput.value)],
        [firstNameInput, validateFirstName(firstNameInput.value)],
        [lastNameInput, validateLastName(lastNameInput.value)],
        [passwordInput, validatePassword(passwordInput.value)],
        [secondPasswordInput, validateSecondPassword(secondPasswordInput.value)]
    ];

    return displayFeedback(feedback);
}