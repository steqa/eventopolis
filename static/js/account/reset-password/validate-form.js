function validateForm(form) {
    const emailInput = form.querySelector('#email');

    const feedback = [
        [emailInput, validateEmail(emailInput.value)],
    ];

    return displayFeedback(feedback);
}