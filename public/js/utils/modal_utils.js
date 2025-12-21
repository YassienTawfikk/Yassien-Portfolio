document.addEventListener('DOMContentLoaded', function () {
    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape') {
            // 1. Prevent exiting Full Screen mode
            event.preventDefault();
            event.stopPropagation();

            // 2. Find any open modal
            // Bootstrap adds '.show' class to the modal div
            const openModal = document.querySelector('.modal.show');
            const openBackdrop = document.querySelector('.modal-backdrop.show'); // Customizable backdrops (e.g. Contact)

            // 3. Close it
            if (openModal) {
                // Try to find a standard close button first
                const closeBtn = openModal.querySelector('.btn-close') || openModal.querySelector('[data-bs-dismiss="modal"]');
                if (closeBtn) {
                    closeBtn.click();
                } else {
                    // Fallback: Use Bootstrap API if available
                    // We can try to get the instance and hide it
                    try {
                        const modalInstance = bootstrap.Modal.getInstance(openModal);
                        if (modalInstance) {
                            modalInstance.hide();
                        } else {
                            // Last resort: simple CSS hide (might leave backdrop)
                            // openModal.classList.remove('show');
                            // document.body.classList.remove('modal-open');
                            // Actually, relying on click is safest for mostly all cases suited here.
                            // If no close button, we might need to find another way.
                            // Let's stick to button click which triggers all standard cleanup.
                        }
                    } catch (e) {
                        console.log("Could not close modal via Bootstrap API", e);
                    }
                }
            }

            // Custom Contact/Notification Modal (non-bootstrap)
            // It uses style="display: flex/block" or class 'show' on .modal-backdrop
            // In contact.js we used id='cv-modal' and style.display
            const customModal = document.getElementById('cv-modal');
            if (customModal && customModal.style.display !== 'none') {
                customModal.style.display = 'none';
            }
        }
    });
});
