function validateForm(form) {
    const firstNameInput = form.querySelector('#first-name');
    const lastNameInput = form.querySelector('#last-name');

    const feedback = [
        [firstNameInput, validateFirstName(firstNameInput.value)],
        [lastNameInput, validateLastName(lastNameInput.value)],
    ];

    return displayFeedback(feedback);
}