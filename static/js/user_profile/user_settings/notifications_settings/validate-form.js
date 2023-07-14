function validateForm(form) {
    const telegramUsernameInput = form.querySelector('#telegram-username');

    const feedback = [
        [telegramUsernameInput, validateTelegramUsername(telegramUsernameInput.value)],
    ];

    return displayFeedback(feedback);
}