let responseStatus = 0


function sendFormData(form) {
    const formData = getFormData(form);
    fetch(window.location.href, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value,
        },
        body: formData
    })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            const errors = JSON.parse(data);
            form.querySelectorAll('input').forEach((input) => {
                const errorsDiv = input.parentNode.querySelector('.invalid-feedback');
                if (input.name in errors) {
                    errorsDiv.innerText = errors[input.name][0]['message'];
                } else {
                    errorsDiv.innerText = '';
                }
            })

        })
        .catch((error) => console.error(error));
}
