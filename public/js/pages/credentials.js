document.addEventListener('DOMContentLoaded', function () {
    const galleryItems = [];

    // Collect all gallery items in order from the DOM
    document.querySelectorAll('.cert-thumb-trigger').forEach(el => {
        galleryItems.push({
            src: el.getAttribute('data-src'),
            index: parseInt(el.getAttribute('data-index'))
        });
    });

    let currentIndex = 0;
    const modalElement = document.getElementById('certificate-modal');
    const modalImage = document.getElementById('modal-cert-image');
    // We assume bootstrap is loaded globally
    const modal = new bootstrap.Modal(modalElement);

    // Open Modal
    document.querySelectorAll('.cert-thumb-trigger').forEach((el, index) => {
        el.addEventListener('click', function () {
            currentIndex = index;
            // Immediate set for opening
            if (galleryItems[currentIndex]) {
                modalImage.src = galleryItems[currentIndex].src;
                modalImage.classList.remove('anim-next', 'anim-prev', 'is-switching');
            }
            modal.show();
        });
    });

    // Navigation
    document.getElementById('btn-prev').addEventListener('click', function () {
        if (currentIndex > 0) {
            navigate(-1);
        }
    });

    document.getElementById('btn-next').addEventListener('click', function () {
        if (currentIndex < galleryItems.length - 1) {
            navigate(1);
        }
    });

    function navigate(direction) {
        // direction: -1 (prev) or 1 (next)
        const newIndex = currentIndex + direction;

        // Bounds check
        if (newIndex < 0 || newIndex >= galleryItems.length) return;

        currentIndex = newIndex;
        const newSrc = galleryItems[currentIndex].src;

        // Animation Logic
        // 1. Hide immediate
        modalImage.classList.add('is-switching');
        modalImage.classList.remove('anim-next', 'anim-prev');

        // 2. Timeout to allow browser to register the hide, then swap src and animate in
        setTimeout(() => {
            modalImage.src = newSrc;

            requestAnimationFrame(() => {
                modalImage.classList.remove('is-switching');
                if (direction === 1) {
                    modalImage.classList.add('anim-next');
                } else {
                    modalImage.classList.add('anim-prev');
                }
            });
        }, 200);

        updateButtons();
    }

    function updateButtons() {
        document.getElementById('btn-prev').disabled = (currentIndex === 0);
        document.getElementById('btn-next').disabled = (currentIndex === galleryItems.length - 1);
    }

    // Keyboard Navigation
    document.addEventListener('keydown', function (event) {
        if (modalElement.classList.contains('show')) {
            if (event.key === 'ArrowLeft') {
                if (currentIndex > 0) navigate(-1);
            } else if (event.key === 'ArrowRight') {
                if (currentIndex < galleryItems.length - 1) navigate(1);
            }
        }
    });
});
