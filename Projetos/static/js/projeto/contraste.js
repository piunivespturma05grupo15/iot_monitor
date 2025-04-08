document.addEventListener('DOMContentLoaded', () => {
    const contrasteBtn = document.getElementById('toggleContrast');

    contrasteBtn.addEventListener('click', () => {
        document.body.classList.toggle('high-contrast');
    });
});
