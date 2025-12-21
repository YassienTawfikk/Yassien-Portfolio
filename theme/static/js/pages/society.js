document.addEventListener('DOMContentLoaded', function () {
    // Scroll Logic
    const container = document.getElementById('involvements-id');
    const scrollLeftBtn = document.getElementById('scroll-left');
    const scrollRightBtn = document.getElementById('scroll-right');
    const scrollAmount = 300; // px

    if (container && scrollLeftBtn && scrollRightBtn) {
        scrollLeftBtn.addEventListener('click', () => {
            container.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
        });

        scrollRightBtn.addEventListener('click', () => {
            container.scrollBy({ left: scrollAmount, behavior: 'smooth' });
        });
    }

    // Modal Logic
    const modalEl = document.getElementById('society-certificate-modal');
    // Ensure modal element exists (bootstrap might not be loaded if network issue, but assumes it is)
    if (modalEl) {
        const modal = new bootstrap.Modal(modalEl);
        const modalImage = document.getElementById('society-modal-cert-image');

        document.querySelectorAll('.society-cert-trigger').forEach(trigger => {
            trigger.addEventListener('click', function () {
                const src = this.getAttribute('data-src');
                modalImage.src = src;
                modal.show();
            });
        });
    }
});
