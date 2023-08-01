const popupContainer = document.getElementById('popup-container');
const openButton = document.getElementById('open-popup');
const closeButton = document.getElementById('close-popup');

openButton.addEventListener('click', function () {
    popupContainer.classList.remove('hidden');
});

closeButton.addEventListener('click', function () {
    popupContainer.classList.add('hidden');
});

window.addEventListener('click', function (event) {
    if (event.target === popupContainer) {
        popupContainer.classList.add('hidden');
    }
});

// Show the button only if the current path is not '/'
if (window.location.pathname !== '/' && window.location.pathname !== '/profile/') {
    openButton.classList.remove('hidden');
}
