const modalSaveBtn = document.getElementById('modalSaveBtn');
const modalInputs = document.querySelectorAll('.form-control.modalInput');

modalInputs.forEach((input) => {
    input.addEventListener('input', () => {
        if (checkAllInputsHasBeenChanged()) {
            modalSaveBtn.removeAttribute('disabled');
        } else {
            modalSaveBtn.setAttribute('disabled', 'true');
        }
    })
})

function checkAllInputsHasBeenChanged() {
    let changed = true;
    modalInputs.forEach((input) => {
        if (input.value.length < 1) {
            changed = false;
        }
    })
    return changed;
}