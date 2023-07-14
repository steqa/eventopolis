const saveBtn = document.getElementById('saveBtn');
const inputs = document.querySelectorAll('.form-control:not(.modalInput)');
let defaultInputsValues = [];


inputs.forEach((input) => {
    defaultInputsValues[input.name] = input.value;

    input.addEventListener('input', () => {
        if (checkAnyInputHasBeenChanged()) {
            saveBtn.removeAttribute('disabled');
        } else {
            saveBtn.setAttribute('disabled', 'true');
        }
    })
})

function checkAnyInputHasBeenChanged() {
    let changed = false;
    inputs.forEach((input) => {
        if (input.value !== defaultInputsValues[input.name]) {
            changed = true;
        }
    })
    return changed;
}