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
        const prevBtn = document.getElementById('society-modal-prev');
        const nextBtn = document.getElementById('society-modal-next');

        let currentCertArray = [];
        let currentCertIndex = 0;

        function updateImage(direction) {
            if (currentCertArray.length > 0) {
                const src = currentCertArray[currentCertIndex];

                // Animation Logic
                // 1. Hide immediate
                modalImage.classList.add('is-switching');
                modalImage.classList.remove('anim-next', 'anim-prev');

                // 2. Timeout to allow browser to register the hide, then swap src and animate in
                setTimeout(() => {
                    modalImage.src = src;

                    requestAnimationFrame(() => {
                        modalImage.classList.remove('is-switching');
                        if (direction === 1) {
                            modalImage.classList.add('anim-next');
                        } else if (direction === -1) {
                            modalImage.classList.add('anim-prev');
                        }
                    });
                }, 200);

                // Update buttons state
                if (prevBtn) prevBtn.disabled = (currentCertIndex === 0);
                if (nextBtn) nextBtn.disabled = (currentCertIndex === currentCertArray.length - 1);

                // Hide buttons if only one image
                if (currentCertArray.length <= 1) {
                    if (prevBtn) prevBtn.style.display = 'none';
                    if (nextBtn) nextBtn.style.display = 'none';
                } else {
                    if (prevBtn) prevBtn.style.display = 'flex';
                    if (nextBtn) nextBtn.style.display = 'flex';
                }
            }
        }

        document.querySelectorAll('.society-cert-trigger').forEach(trigger => {
            trigger.addEventListener('click', function () {
                const rawCerts = this.getAttribute('data-certs');
                try {
                    currentCertArray = JSON.parse(rawCerts || '[]');
                } catch (e) {
                    console.error("Failed to parse certificates data", e);
                    // Fallback to data-src if it exists (legacy support)
                    const singleSrc = this.getAttribute('data-src');
                    currentCertArray = singleSrc ? [singleSrc] : [];
                }

                currentCertIndex = 0;

                // Reset display before showing
                if (prevBtn) prevBtn.style.display = 'none';
                if (nextBtn) nextBtn.style.display = 'none';

                if (currentCertArray.length > 0) {
                    modalImage.src = currentCertArray[0];
                    updateImage();
                    modal.show();
                }
            });
        });

        // Navigation Handlers
        if (prevBtn) {
            prevBtn.addEventListener('click', () => {
                if (currentCertIndex > 0) {
                    currentCertIndex--;
                    updateImage(-1);
                }
            });
        }

        if (nextBtn) {
            nextBtn.addEventListener('click', () => {
                if (currentCertIndex < currentCertArray.length - 1) {
                    currentCertIndex++;
                    updateImage(1);
                }
            });
        }
    }
});
