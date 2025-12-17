// assets/js/contact.js

document.addEventListener('DOMContentLoaded', function () {


    const EMAILJS_PUBLIC_KEY = "A03Gz-zzs0j09uVz3";
    const EMAILJS_SERVICE_ID = "service_2k9xyz";
    const EMAILJS_TEMPLATE_ID = "template_d4ryemm";


    if (typeof emailjs !== 'undefined') {
        emailjs.init(EMAILJS_PUBLIC_KEY);
    } else {
        console.warn("EmailJS SDK not loaded. Form functionality disabled.");
    }


    function setupCopyButton(btnId, textId, feedbackId) {
        const btn = document.getElementById(btnId);
        const textEl = document.getElementById(textId); // Or simply pass the string
        const feedback = document.getElementById(feedbackId);

        if (btn && textEl) {
            btn.addEventListener('click', function (e) {
                e.preventDefault();
                let textToCopy = textEl.innerText || textEl.textContent;


                if (textId === 'contact-phone-text') {
                    textToCopy = textToCopy.replace(/[^\d+]/g, '');
                }

                navigator.clipboard.writeText(textToCopy).then(() => {
                    const originalIcon = btn.innerHTML;
                    btn.innerHTML = '<i class="fa-solid fa-check"></i>'; // Change icon to check
                    if (feedback) {
                        feedback.innerText = "Copied!";
                        feedback.classList.add('visible');
                    }

                    setTimeout(() => {
                        btn.innerHTML = '<i class="fa-regular fa-copy"></i>';
                        if (feedback) {
                            feedback.classList.remove('visible');
                        }
                    }, 2000);
                }).catch(err => {
                    console.error('Failed to copy: ', err);
                });
            });
        }
    }

    const observer = new MutationObserver(function (mutations, me) {
        const emailBtn = document.getElementById('copy-email-btn');
        if (emailBtn) {
            setupCopyButton('copy-email-btn', 'contact-email-text', 'email-copy-feedback');
            setupCopyButton('copy-phone-btn', 'contact-phone-text', 'phone-copy-feedback');
            me.disconnect(); // Stop observing once found
            // Re-attach listener for form submission since it might have been missed
            attachFormListener();
        }
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true
    });

    function attachFormListener() {
        const contactForm = document.getElementById('zen-contact-form');
        const submitBtn = document.getElementById('zen-submit-btn');
        const feedbackEl = document.getElementById('zen-form-feedback');

        if (contactForm && !contactForm.dataset.listenerAttached) {
            contactForm.dataset.listenerAttached = "true"; // Prevent double binding
            contactForm.addEventListener('submit', function (event) {
                event.preventDefault();

                const originalBtnText = submitBtn.innerText;
                submitBtn.innerText = "Processing...";
                submitBtn.disabled = true;
                submitBtn.style.opacity = "0.5";

                feedbackEl.classList.remove('visible');
                feedbackEl.innerText = "";

                const params = {
                    from_name: document.getElementById('from_name').value,
                    reply_to: document.getElementById('reply_to').value,
                    message: document.getElementById('message').value
                };



                emailjs.send(EMAILJS_SERVICE_ID, EMAILJS_TEMPLATE_ID, params)
                    .then(function () {
                        feedbackEl.innerText = "Message received. Thank you.";
                        feedbackEl.classList.add('visible');
                        contactForm.reset();
                        submitBtn.innerText = "Sent";
                        setTimeout(() => {
                            submitBtn.innerText = originalBtnText;
                            submitBtn.disabled = false;
                            submitBtn.style.opacity = "1";
                        }, 3000);
                    }, function (error) {
                        console.error('EmailJS Error:', error);
                        feedbackEl.innerText = "Transmission failed. Please try again.";
                        feedbackEl.classList.add('visible');
                        submitBtn.innerText = originalBtnText;
                        submitBtn.disabled = false;
                        submitBtn.style.opacity = "1";
                    });
            });
        }
    }
});
