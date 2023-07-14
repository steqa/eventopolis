const aboutMeInput = document.getElementById('about-me');
const aboutMeLength = document.getElementById('aboutMeLength');

aboutMeLength.innerHTML = aboutMeInput.value.length + ' / 150';
const aboutMeLengthOriginalColor = aboutMeLength.style.color;
aboutMeInput.addEventListener('input', () => {
    if (aboutMeInput.value.length > 150) {
        aboutMeLength.style.color = 'var(--bs-danger)';
        setTimeout(() => {
            saveBtn.setAttribute('disabled', 'true');
        }, 1);
    } else {
        aboutMeLength.style.color = aboutMeLengthOriginalColor;
    }
    aboutMeLength.innerHTML = aboutMeInput.value.length + ' / 150';
})
