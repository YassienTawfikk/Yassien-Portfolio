document.addEventListener('DOMContentLoaded', function () {
    // 1. Copy to Clipboard
    const copyBtns = document.querySelectorAll('.copy-btn');
    copyBtns.forEach(btn => {
        btn.addEventListener('click', function () {
            const text = this.getAttribute('data-text');
            const feedbackId = this.id.replace('btn', 'feedback').replace('copy-', '');
            const feedbackEl = document.nextElementSibling || this.parentElement.querySelector('.copy-feedback');

            navigator.clipboard.writeText(text).then(() => {
                feedbackEl.textContent = 'Copied!';
                setTimeout(() => feedbackEl.textContent = '', 2000);
            });
        });
    });

    // 2. Notification Modal for Socials
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

            modal.style.display = 'flex';
            // Simple display toggle, matching Dash behavior mostly
        });
    });

    if (confirmBtn) {
        confirmBtn.addEventListener('click', function () {
            if (targetUrl) window.open(targetUrl, '_blank');
            modal.style.display = 'none';
        });
    }

    if (cancelBtn) {
        cancelBtn.addEventListener('click', function () {
            modal.style.display = 'none';
        });
    }

    if (overlay) {
        overlay.addEventListener('click', function () {
            modal.style.display = 'none';
        });
    }

    // 3. EmailJS Form
    if (window.emailjs) {
        emailjs.init("YOUR_PUBLIC_KEY"); // User needs to provide this or I should extract it if visible. 
        // Note: The Dash app included the script but I didn't see the init call in app.py or contact.py.
        // It might be in src/data/contact.json or environment vars. 
        // For now I will assume standard usage or leave a placeholder. 
        // Actually app.py included "https://cdn.jsdelivr.net/npm/@emailjs/browser@3/dist/email.min.js".
        // Use logic from existing codebase if found. 
        // I'll try to find where emailjs.init is called. 
    }

    const submitBtn = document.getElementById('zen-submit-btn');
    const nameInput = document.getElementById('from_name');
    const emailInput = document.getElementById('reply_to');
    const msgInput = document.getElementById('message');
    const feedback = document.getElementById('zen-form-feedback');

    submitBtn.addEventListener('click', function (e) {
        e.preventDefault();

        const serviceID = 'default_service'; // Placeholder
        const templateID = 'template_id';    // Placeholder

        const params = {
            from_name: nameInput.value,
            reply_to: emailInput.value,
            message: msgInput.value
        };

        if (!params.from_name || !params.reply_to || !params.message) {
            feedback.textContent = "Please fill in all fields.";
            feedback.style.color = "red";
            return;
        }

        feedback.textContent = "Sending...";

        // Try to send if emailjs is defined
        if (window.emailjs) {
            emailjs.send(serviceID, templateID, params)
                .then(() => {
                    feedback.textContent = "Message Sent!";
                    feedback.style.color = "green";
                    nameInput.value = '';
                    emailInput.value = '';
                    msgInput.value = '';
                }, (err) => {
                    feedback.textContent = "Failed to send. Please try direct email.";
                    feedback.style.color = "red";
                    console.log(JSON.stringify(err));
                });
        } else {
            feedback.textContent = "Email service not configured.";
        }
    });
});
