document.addEventListener('DOMContentLoaded', function () {
    const videoButtons = document.querySelectorAll('.video-btn');
    const videoModal = new bootstrap.Modal(document.getElementById('videoModal'));
    const modalBody = document.getElementById('videoModalBody');
    const modalTitle = document.getElementById('videoModalLabel');
    const modalElement = document.getElementById('videoModal');

    videoButtons.forEach(btn => {
        btn.addEventListener('click', function () {
            const videoUrl = this.getAttribute('data-video-url');
            const title = this.getAttribute('data-project-title');

            modalTitle.textContent = title;

            // Replicate the iframe structure from Dash app to ensuring no-referrer
            const videoHtml = `
                <!DOCTYPE html>
                <html style="margin: 0; padding: 0; height: 100%; overflow: hidden;">
                <head>
                    <meta name="referrer" content="no-referrer">
                    <style>
                        body { margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; height: 100%; background: #000; }
                        video { width: 100%; height: 100%; object-fit: contain; }
                    </style>
                </head>
                <body>
                    <video src="${videoUrl}" controls autoplay loop playsinline></video>
                </body>
                </html>
            `;

            // Create iframe
            const iframe = document.createElement('iframe');
            iframe.style.width = '100%';
            iframe.style.height = '500px';
            iframe.style.border = 'none';
            iframe.allow = 'autoplay';
            iframe.srcdoc = videoHtml;

            modalBody.innerHTML = '';
            modalBody.appendChild(iframe);

            videoModal.show();
        });
    });

    // Clear video when modal closes
    modalElement.addEventListener('hidden.bs.modal', function () {
        modalBody.innerHTML = '';
    });
});
