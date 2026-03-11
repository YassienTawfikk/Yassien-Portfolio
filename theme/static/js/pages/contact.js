document.addEventListener('DOMContentLoaded', function () {
    // =========================================================
    // 1. Copy to Clipboard
    // =========================================================
    const copyBtns = document.querySelectorAll('.copy-btn');
    copyBtns.forEach(btn => {
        btn.addEventListener('click', function () {
            const text = this.getAttribute('data-text');
            const feedbackEl = document.nextElementSibling || this.parentElement.querySelector('.copy-feedback');

            navigator.clipboard.writeText(text).then(() => {
                feedbackEl.textContent = 'Copied!';
                this.classList.add('copied');

                const icon = this.querySelector('i');
                const originalIconClass = icon.className;
                icon.className = 'fa-solid fa-check';

                setTimeout(() => {
                    feedbackEl.textContent = '';
                    this.classList.remove('copied');
                    icon.className = originalIconClass;
                }, 2000);
            });
        });
    });

    // =========================================================
    // 2. Notification Modal for Socials
    // =========================================================
    const modal = document.getElementById('cv-modal');
    const modalTitle = document.getElementById('notification-title');
    const modalMsg = document.getElementById('confirm-message-text');
    const confirmBtn = document.getElementById('confirm-ok');
    const cancelBtn = document.getElementById('confirm-cancel');
    const overlay = document.getElementById('modal-overlay-bg');

    let targetUrl = '';

    document.querySelectorAll('.social-notify-trigger').forEach(trigger => {
        trigger.addEventListener('click', function (e) {
            e.preventDefault();
            targetUrl = this.getAttribute('data-href');
            modalTitle.textContent = this.getAttribute('data-notify-title');
            modalMsg.textContent = this.getAttribute('data-notify-desc');

            if (cancelBtn) cancelBtn.style.display = 'inline-block';
            if (confirmBtn) confirmBtn.textContent = 'Continue to Site';

            modal.style.display = 'flex';
            setTimeout(() => { modal.classList.add('show'); }, 10);
        });
    });

    function closeModal() {
        modal.classList.remove('show');
        setTimeout(() => { modal.style.display = 'none'; }, 300);
    }

    if (confirmBtn) {
        confirmBtn.addEventListener('click', function () {
            if (targetUrl) window.open(targetUrl, '_blank');
            closeModal();
        });
    }
    if (cancelBtn) {
        cancelBtn.addEventListener('click', function () { closeModal(); });
    }
    if (overlay) {
        overlay.addEventListener('click', function () { closeModal(); });
    }

    // =========================================================
    // 3. Toast Notification System
    // =========================================================
    const toast = document.getElementById('form-toast');
    let toastTimer = null;

    function showToast(msg, type) {
        // type: 'warning', 'success', 'error'
        if (toastTimer) clearTimeout(toastTimer);

        toast.textContent = msg;
        toast.className = 'form-toast form-toast--' + type + ' form-toast--visible';

        // Auto-hide after 4 seconds (except 'sending' which stays)
        if (type !== 'sending') {
            toastTimer = setTimeout(function () {
                toast.classList.remove('form-toast--visible');
            }, 4000);
        }
    }

    function hideToast() {
        if (toastTimer) clearTimeout(toastTimer);
        toast.classList.remove('form-toast--visible');
    }

    // =========================================================
    // 4. EmailJS Contact Form
    // =========================================================
    if (window.emailjs) {
        emailjs.init("A03Gz-zzs0j09uVz3");
    }

    const submitBtn = document.getElementById('zen-submit-btn');
    const nameInput = document.getElementById('from_name');
    const emailInput = document.getElementById('reply_to');
    const msgInput = document.getElementById('message');

    submitBtn.addEventListener('click', function () {
        // Client-side validation
        if (!nameInput.value.trim() || !emailInput.value.trim() || !msgInput.value.trim()) {
            showToast('Please fill in all the fields.', 'warning');
            return;
        }

        // Simple email format check
        var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(emailInput.value.trim())) {
            showToast('Please enter a valid email address.', 'warning');
            return;
        }

        // Disable button to prevent double-send
        submitBtn.disabled = true;
        submitBtn.textContent = 'Sending...';
        submitBtn.style.opacity = '0.5';
        submitBtn.style.pointerEvents = 'none';
        showToast('Sending your message...', 'sending');

        var params = {
            from_name: nameInput.value,
            reply_to: emailInput.value,
            message: msgInput.value
        };

        if (window.emailjs) {
            emailjs.send('service_2k9xyz', 'template_d4ryemm', params)
                .then(function () {
                    showToast('Message sent successfully!', 'success');
                    nameInput.value = '';
                    emailInput.value = '';
                    msgInput.value = '';
                    resetButton();
                }, function (err) {
                    showToast('Failed to send. Please try direct email.', 'error');
                    console.error('EmailJS error:', err);
                    resetButton();
                });
        } else {
            showToast('Email service unavailable. Please use direct email.', 'error');
            resetButton();
        }
    });

    function resetButton() {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Send Message';
        submitBtn.style.opacity = '';
        submitBtn.style.pointerEvents = '';
    }
});
