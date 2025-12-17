/* Global Preloader Logic */
document.addEventListener("DOMContentLoaded", function () {
    const preloader = document.getElementById("global-preloader");
    const FADE_OUT_DELAY = 500; // Small buffer for smoothness
    const FAILSAFE_TIMEOUT = 3000; // Max wait time in ms

    function showPreloader() {
        if (preloader) {
            preloader.classList.remove("hidden");
        }
    }

    function hidePreloader() {
        if (preloader) {
            setTimeout(() => {
                preloader.classList.add("hidden");
            }, FADE_OUT_DELAY);
        }
    }

    // Initial load handling
    window.onload = function () {
        hidePreloader();
    };

    // Failsafe: Ensure loader disappears even if something gets stuck
    setTimeout(hidePreloader, FAILSAFE_TIMEOUT);

    // Watch for Dash Page Content Updates
    // Dash updates the "page-content" div when navigating.
    const observer = new MutationObserver(function (mutations) {
        mutations.forEach((mutation) => {
            if (mutation.addedNodes.length > 0) {
                // Determine if we need to wait for images
                const images = document.querySelectorAll("#page-content img");
                if (images.length === 0) {
                    hidePreloader();
                } else {
                    let imagesLoaded = 0;
                    images.forEach((img) => {
                        if (img.complete) {
                            imagesLoaded++;
                        } else {
                            img.addEventListener("load", () => {
                                imagesLoaded++;
                                if (imagesLoaded === images.length) {
                                    hidePreloader();
                                }
                            });
                            img.addEventListener("error", () => {
                                imagesLoaded++; // Treat error as loaded to avoid sticking
                                if (imagesLoaded === images.length) {
                                    hidePreloader();
                                }
                            });
                        }
                    });

                    // If all were already cached/loaded
                    if (imagesLoaded === images.length) {
                        hidePreloader();
                    }
                }

                // Reset failsafe on navigation
                setTimeout(hidePreloader, FAILSAFE_TIMEOUT);
            }
        });
    });

    const contentDiv = document.getElementById("page-content");
    if (contentDiv) {
        observer.observe(contentDiv, { childList: true, subtree: true });
    }

    // Capture Internal Navigation Clicks to Show Loader Immediately
    document.addEventListener("click", function (e) {
        const target = e.target.closest("a");
        if (target && target.href && target.href.startsWith(window.location.origin)) {
            // Ignore anchor links on the same page, or special target=_blank
            if (target.getAttribute("target") !== "_blank" &&
                !target.href.includes("#") &&
                target.href !== window.location.href) {
                showPreloader();
            }
        }
    });
});
