const telegramUsernameInput = document.getElementById('telegram-username');
const telegramNotificationsInput = document.getElementById('telegram-notifications');

if (telegramNotificationsInput.value === 'True') {
    telegramNotificationsInput.setAttribute('checked', 'true');
}

if (!telegramUsernameInput.value) {
    telegramNotificationsInput.setAttribute('disabled', 'true');
}
