document.addEventListener('DOMContentLoaded', function () {
    // =========================================================
    // 1. Horizontal Scroll Controls
    // =========================================================
    const container = document.getElementById('involvements-id');
    const scrollLeftBtn = document.getElementById('scroll-left');
    const scrollRightBtn = document.getElementById('scroll-right');
    const scrollAmount = 300;

    if (container && scrollLeftBtn && scrollRightBtn) {
        scrollLeftBtn.addEventListener('click', () => {
            container.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
        });

        scrollRightBtn.addEventListener('click', () => {
            container.scrollBy({ left: scrollAmount, behavior: 'smooth' });
        });
    }

    // =========================================================
    // 2. Certificate Gallery (powered by Gallery class)
    // =========================================================
    new Gallery({
        triggerSelector: '.society-cert-trigger',
        modalId: 'society-certificate-modal',
        imageId: 'society-modal-cert-image',
        prevBtnId: 'society-modal-prev',
        nextBtnId: 'society-modal-next',
        dataMode: 'json-array'
    });
});
