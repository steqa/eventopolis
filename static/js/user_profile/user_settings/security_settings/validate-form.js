function validateForm(form) {
    const slugInput = form.querySelector('#slug');

    const feedback = [
        [slugInput, validateSlug(slugInput.value)],
    ];

    return displayFeedback(feedback);
}