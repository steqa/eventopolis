function displayFeedback(feedback) {
    let valid = true;
    feedback.forEach(([input, errors]) => {
        const errorsDiv = input.parentNode.querySelector('.invalid-feedback');
        errorsDiv.innerText = '';
        if (errors.length > 0) {
            errors.forEach((error) => {
                errorsDiv.innerText += error + '\n';
            });
            valid = false;
        }
    });
    return valid;
}