const notification = '' +
    '<div class="toast-container position-fixed top-0 start-50 translate-middle-x p-3">\n' +
    '    <div id="pushNotification" class="toast align-items-center text-bg-{0} border-0" role="alert"\n' +
    '         aria-live="assertive"\n' +
    '         aria-atomic="true">\n' +
    '        <div class="d-flex">\n' +
    '            <div class="toast-body">\n' +
    '                {1}\n' +
    '            </div>\n' +
    '            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"\n' +
    '                    aria-label="Close"></button>\n' +
    '        </div>\n' +
    '    </div>\n' +
    '</div>'

String.prototype.format = function () {
    const args = arguments;
    return this.replace(/{([0-9]+)}/g, function (match, index) {
        return typeof args[index] == 'undefined' ? match : args[index];
    });
};

function showPushNotification(color = 'primary', text) {
    document.body.insertAdjacentHTML('afterbegin', notification.format(color, text));
    const toastLiveExample = document.getElementById('pushNotification')
    const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample)
    toastBootstrap.show()
}
