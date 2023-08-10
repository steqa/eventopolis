const loader = '<div class="loader" id="loader">\n' +
    '    <div class="loader__center">\n' +
    '        <div class="spinner-border text-primary" role="status">\n' +
    '            <span class="visually-hidden">Loading...</span>\n' +
    '        </div>\n' +
    '    </div>\n' +
    '</div>'

function activateLoader() {
    document.body.insertAdjacentHTML('afterbegin', loader);
}

function deactivateLoader() {
    document.getElementById('loader').remove();
}
