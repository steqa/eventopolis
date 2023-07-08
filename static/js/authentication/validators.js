function validateEmail(value) {
    let errors = [];
    const validRegex = /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
    if (!String(value).match(validRegex)) {
        errors.push('Неверный адрес электронной почты.');
    }
    return errors;
}

function validateFirstName(value) {
    let errors = [];
    if (value !== (value[0].toUpperCase() + value.slice(1))) {
        errors.push('Имя должно начинаться с заглавной буквы.');
    }
    if (value.split(' ').length > 1) {
        errors.push('Имя должно содержать одно слово.');
    }
    return errors;
}

function validateLastName(value) {
    let errors = [];
    if (value !== (value[0].toUpperCase() + value.slice(1))) {
        errors.push('Фамилия должна начинаться с заглавной буквы.');
    }
    if (value.split(' ').length > 1) {
        errors.push('Фамилия должна содержать одно слово.');
    }
    return errors;
}

function validatePassword(value) {
    let errors = [];
    if (value.length < 8) {
        errors.push('Введённый пароль слишком короткий. Он должен содержать как минимум 8 символов.');
    }
    if (/^[0-9]+$/.test(value)) {
        errors.push('Введённый пароль состоит только из цифр.');
    }
    return errors;
}

function validateSecondPassword(value) {
    let errors = [];
    if (value !== document.getElementById('password1').value) {
        errors.push('Пароли не совпадают.');
    }
    return errors;
}