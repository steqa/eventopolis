const telegramNotificationsInput = document.getElementById('telegram-notifications');

telegramNotificationsInput.addEventListener('input', () => {
    if (telegramNotificationsInput.value === 'False') {
        telegramNotificationsInput.value = 'True';
    } else {
        telegramNotificationsInput.value = 'False';
    }
})