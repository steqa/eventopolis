function validateForm(form) {
    const emailInput = form.querySelector('#email');
    const slugInput = form.querySelector('#slug');

    const feedback = [
        [emailInput, validateEmail(emailInput.value)],
        [slugInput, validateSlug(slugInput.value)],
    ];

    return displayFeedback(feedback);
}