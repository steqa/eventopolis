const enableTelegramNotificationsBtn = document.getElementById('enableTelegramNotificationsBtn');
const disableTelegramNotificationsBtn = document.getElementById('disableTelegramNotificationsBtn');
const input = document.getElementById('telegram-notifications');


enableTelegramNotificationsBtn.addEventListener('click', (event) => {
    event.preventDefault();
    sendGETRequest(enableTelegramNotificationsBtn.href);
});

disableTelegramNotificationsBtn.addEventListener('click', (event) => {
    event.preventDefault();
    sendGETRequest(disableTelegramNotificationsBtn.href);
});

function sendGETRequest(url) {
    activateLoader();
    let responseStatus = null
    fetch(url)
        .then((response) => {
            responseStatus = response.status
            return response.json();
        })
        .then((data) => {
            if (responseStatus === 400) {
                deactivateLoader();
                data = JSON.parse(data)
                const message = data['push']['message'];
                showPushNotification('danger', message);
            } else if (responseStatus === 302) {
                window.location.replace(window.location.origin + data['url']);
            }
        })
        .catch((error) => console.error(error));
}