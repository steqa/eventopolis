function validateModalForm(form) {
    const oldPasswordInput = form.querySelector('#old-password');
    const newPassword1Input = form.querySelector('#new-password1');
    const newPassword2Input = form.querySelector('#new-password2');

    const feedback = [
        [oldPasswordInput, validatePassword(oldPasswordInput.value)],
        [newPassword1Input, validatePassword(newPassword1Input.value).concat(
            validateNewPassword(newPassword1Input.value, oldPasswordInput.id, newPassword1Input.id))],
        [newPassword2Input, validateSecondPassword(newPassword2Input.value, newPassword1Input.id, newPassword2Input.id)]
    ];

    return displayFeedback(feedback);
}