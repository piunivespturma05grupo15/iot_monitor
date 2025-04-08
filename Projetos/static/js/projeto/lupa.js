let zoomAtivo = false;

document.addEventListener('DOMContentLoaded', () => {
    const zoomBtn = document.getElementById('toggleZoom');
    const zoomWindow = document.getElementById('zoom-window');

    zoomBtn.addEventListener('click', () => {
        zoomAtivo = !zoomAtivo;
        zoomWindow.style.display = zoomAtivo ? 'block' : 'none';
        
        // Troca a imagem da lupa
        zoomBtn.src = zoomAtivo
            ? '/static/images/lupa-desativa.svg' // imagem para DESATIVAR
            : '/static/images/lupa-ativa.svg';   // imagem para ATIVAR
    });

    document.addEventListener('mousemove', (e) => {
        if (!zoomAtivo) return;

        html2canvas(document.body).then(canvas => {
            const ctx = canvas.getContext("2d");
            const zoomWidth = 100, zoomHeight = 100;

            const x = Math.max(0, e.pageX - zoomWidth / 2);
            const y = Math.max(0, e.pageY - zoomHeight / 2);

            const imageData = ctx.getImageData(x, y, zoomWidth, zoomHeight);

            const zoomCanvas = document.createElement("canvas");
            zoomCanvas.width = zoomWidth;
            zoomCanvas.height = zoomHeight;

            zoomCanvas.getContext("2d").putImageData(imageData, 0, 0);

            zoomWindow.innerHTML = '';
            const zoomImg = new Image();
            zoomImg.src = zoomCanvas.toDataURL();
            zoomWindow.appendChild(zoomImg);
        });
    });
});
