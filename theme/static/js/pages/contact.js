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
                this.classList.add('copied');

                // Change icon to checkmark temporarily
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

            // Reset buttons for social notification
            if (cancelBtn) cancelBtn.style.display = 'inline-block';
            if (confirmBtn) confirmBtn.textContent = 'Continue to Site';

            modal.style.display = 'flex';
            // Slight delay to allow display:flex to apply before adding opacity class for transition
            setTimeout(() => {
                modal.classList.add('show');
            }, 10);
        });
    });

    function closeModal() {
        modal.classList.remove('show');
        setTimeout(() => {
            modal.style.display = 'none';
        }, 300); // 300ms matches CSS transition
    }

    if (confirmBtn) {
        confirmBtn.addEventListener('click', function () {
            if (targetUrl) window.open(targetUrl, '_blank');
            closeModal();
        });
    }

    if (cancelBtn) {
        cancelBtn.addEventListener('click', function () {
            closeModal();
        });
    }

    if (overlay) {
        overlay.addEventListener('click', function () {
            closeModal();
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
        console.log("Contact form params:", params);

        if (!params.from_name || !params.from_name.trim() ||
            !params.reply_to || !params.reply_to.trim() ||
            !params.message || !params.message.trim()) {

            console.log("Validation failed. Showing modal.");
            // Show modal
            modalTitle.textContent = "Action Required";
            modalMsg.textContent = "Please fill in all the fields.";

            // Clear targetUrl so clicking OK doesn't open a link
            targetUrl = '';

            // Only show one button for simple alert if preferred, or keep both. 
            // The existing modal has "Continue to Site" and "Cancel". 
            // We can repurpose "Confirm" to just close it, or hide "Cancel".

            // For simplicity, we just show it. The existing "Continue to Site" (confirmBtn) closes it if no URL.
            // Let's hide the cancel button for this specific alert to make it cleaner? 
            // Or just leave it as is. The user just asked for "a box".

            if (cancelBtn) cancelBtn.style.display = 'none'; // Hide cancel for this warning
            if (confirmBtn) confirmBtn.textContent = 'OK';   // Rename main button

            // We need to reset these when the modal closes or opens for other things, but strictly for this task:
            modal.style.display = 'flex';
            setTimeout(() => modal.classList.add('show'), 10);

            // Reset button state for next time (optional but good practice if shared)
            // But since this is a specific flow, let's keep it simple.
            // Note: The social links might need the buttons back. 
            // Ideally we should have a helper to showModal(title, msg, showCancel).
            // But I will stick to inline modification for unnecessary complexity avoidance unless requested.

            // Re-attach close listener to restore buttons? 
            // Let's just set them here.

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
