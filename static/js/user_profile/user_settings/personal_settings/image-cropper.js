const imageInput = document.getElementById('image');
const errorsDiv = imageInput.parentNode.querySelector('.invalid-feedback');
const imageBox = document.getElementById('imageBox');
const imagePreview = document.getElementById('imagePreview');
const modalSaveBtn = document.getElementById('modalSaveBtn');

let cropper = null;

imageInput.addEventListener('change', () => {
    errorsDiv.innerText = '';
    const img = imageInput.files[0];
    const imgUrl = URL.createObjectURL(img);
    imageBox.classList.remove('d-none');
    imagePreview.src = imgUrl;

    const $image = $('.bootstrap-modal-cropper img');
    $image.cropper('destroy');

    $image.cropper({
        aspectRatio: 1,
        autoCropArea: 0.8,
        highlight: false,
        dragCrop: false,
        autoCrop: true,
        zoomable: false,
        movable: false,
        background: false,
    });

    cropper = $image.data('cropper');
    modalSaveBtn.removeAttribute('disabled');
});


const changeImageModal = document.getElementById('changeImageModal');
changeImageModal.addEventListener('hide.bs.modal', () => {
    setTimeout(() => {
        errorsDiv.innerText = '';
        imageInput.value = null;

        imageBox.classList.add('d-none');
        imagePreview.src = '';

        cropper.destroy();
        cropper = null;
        modalSaveBtn.setAttribute('disabled', 'true');
    }, 300);
})


const imageForm = document.getElementById('imageForm');
imageForm.addEventListener('submit', function (event) {
    event.preventDefault();
    if (cropper) {
        activateLoader();
        cropper.getCroppedCanvas().toBlob((blob) => {
            let formData = new FormData()
            formData.append(imageInput.name, blob, imageInput.value);

            let responseStatus = null
            fetch(window.location.href + '?fieldType=image', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.getElementsByName('csrfmiddlewaretoken')[0].value
                },
                body: formData
            })
                .then((response) => {
                    responseStatus = response.status
                    return response.json();
                })
                .then((data) => {
                    if (responseStatus === 400) {
                        deactivateLoader();
                        const errors = JSON.parse(data);
                        if (imageInput.name in errors) {
                            errorsDiv.innerText = errors[imageInput.name][0]['message'];
                        } else {
                            errorsDiv.innerText = '';
                        }
                    } else if (responseStatus === 302) {
                        window.location.replace(window.location.origin + data['url']);
                    }
                })
                .catch((error) => console.error(error));
        });
    }
});
