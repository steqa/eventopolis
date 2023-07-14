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
    if (!(_testStringContainsOnlyLetters(value))) {
        errors.push('Имя может содержать только буквы.');
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
    if (!(_testStringContainsOnlyLetters(value))) {
        errors.push('Фамилия может содержать только буквы.');
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

function validateSecondPassword(value, firstPasswordID, secondPasswordID) {
    let errors = [];
    if (value !== document.getElementById(firstPasswordID).value) {
        const firstPasswordLabel = document.querySelector(`label[for='${firstPasswordID}']`).textContent;
        const secondPasswordLabel = document.querySelector(`label[for='${secondPasswordID}']`).textContent;
        errors.push(`${firstPasswordLabel} и ${secondPasswordLabel.toLowerCase()} не совпадают.`);
    }
    return errors;
}

function validateNewPassword(value, oldPasswordID, newPasswordID) {
    let errors = [];
    if (value === document.getElementById(oldPasswordID).value) {
        const oldPasswordLabel = document.querySelector(`label[for='${oldPasswordID}']`).textContent;
        const newPasswordLabel = document.querySelector(`label[for='${newPasswordID}']`).textContent;
        errors.push(`${newPasswordLabel} слишком похож на ${oldPasswordLabel.toLowerCase()}.`);
    }
    return errors;
}

function validateSlug(value) {
    let errors = [];
    if (value.length < 5) {
        errors.push('Введённый адрес страницы слишком короткий. Он должен содержать как минимум 5 символов.');
    }
    if (value.length > 32) {
        errors.push('Введённый адрес страницы слишком длинный. Он может содержать максимум 32 символа.');
    }
    const slug = /[a-z0-9_-]+/gi;
    if (!(slug.test(value) && value.match(slug)[0] === value)) {
        errors.push('Адрес страницы должен состоять только из латинских букв, цифр, знаков подчеркивания или дефиса.');
    }
    return errors;
}

function validateTelegramUsername(value) {
    let errors = [];
    if (value.length < 5) {
        errors.push('Введённое имя пользователя телеграм слишком короткое. Оно должно содержать как минимум 5 символов.');
    }
    if (value.length > 32) {
        errors.push('Введённое имя пользователя телеграм слишком длинное. Оно может содержать максимум 32 символа.');
    }
    const telegramUsername = /[a-z0-9_]+/gi;
    if (!(telegramUsername.test(value) && value.match(telegramUsername)[0] === value)) {
        errors.push('Имя пользователя телеграм должно состоять только из латинских букв, цифр или знаков подчеркивания.');
    }
    return errors;
}

function _testStringContainsOnlyLetters(string) {
    let inStringOnlyLetters = true;
    for (let i = 0; i < string.length; i++) {
        const character = string[i];
        if (!(_testForLetter(character))) {
            inStringOnlyLetters = false;
        }
    }
    return inStringOnlyLetters;
}

function _testForLetter(character) {
    try {
        eval("let " + character + ";");
        let regExSpecial = /[^\$_]/;
        return regExSpecial.test(character);
    } catch (error) {
        return false;
    }
}