document.addEventListener('DOMContentLoaded', function () {
    new Gallery({
        triggerSelector: '.cert-thumb-trigger',
        modalId: 'certificate-modal',
        imageId: 'modal-cert-image',
        prevBtnId: 'btn-prev',
        nextBtnId: 'btn-next',
        dataMode: 'single'
    });
});
