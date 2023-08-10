window.addEventListener("load", () => {
    const preloaders = document.querySelectorAll('.preloaderJS');
    const contents = document.querySelectorAll('.contentJS');
    preloaders.forEach((preloader) => {
        preloader.classList.add('visually-hidden');
    });
    contents.forEach((content) => {
        content.classList.remove('visually-hidden');
    });
});