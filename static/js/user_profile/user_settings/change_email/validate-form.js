function validateForm(form) {
    const oldEmailInput = form.querySelector('#old-email');
    const newEmail1Input = form.querySelector('#new-email1');
    const newEmail2Input = form.querySelector('#new-email2');

    const feedback = [
        [newEmail1Input, validateNewEmail1(newEmail1Input.value, oldEmailInput.id).concat(
            validateEmail(newEmail1Input.value))],
        [newEmail2Input, validateNewEmail2(newEmail2Input.value, newEmail1Input.id, newEmail2Input.id)]
    ];

    return displayFeedback(feedback);
}