/* Smart Global Preloader Logic */
document.addEventListener("DOMContentLoaded", function () {
    const preloader = document.getElementById("global-preloader");
    const FADE_OUT_DELAY = 500;
    const FAILSAFE_TIMEOUT = 5000; // Increased for safety on slower networks
    const DOM_STABILIZATION_DELAY = 100; // Wait for DOM to stop changing before checking images

    let hideTimeout;
    let failsafeTimer;
    let isTransitioning = false;

    function showPreloader() {
        if (preloader && preloader.classList.contains("hidden")) {
            preloader.classList.remove("hidden");
            isTransitioning = true;
            // Set failsafe whenever we show it
            clearTimeout(failsafeTimer);
            failsafeTimer = setTimeout(forceHide, FAILSAFE_TIMEOUT);
        }
    }

    function forceHide() {
        if (preloader && !preloader.classList.contains("hidden")) {
            console.warn("Preloader failsafe triggered.");
            preloader.classList.add("hidden");
            isTransitioning = false;
        }
    }

    function checkReadiness() {
        // 1. Is DOM Stable? (Implied by being called after debounce)

        // 2. Are images loaded?
        const images = document.querySelectorAll("#page-content img");
        const totalImages = images.length;
        let loadedImages = 0;

        if (totalImages === 0) {
            // No images? Safe to hide.
            initiateHide();
            return;
        }

        // Check load status of all images
        let allReady = true;
        images.forEach((img) => {
            if (!img.complete || (img.naturalWidth === 0 && !img.src.endsWith(".svg"))) {
                // Image not ready
                allReady = false;

                // Ensure handlers are attached (idempotent)
                // We use a custom property to avoid stacking listeners
                if (!img.hasAttribute("data-preloader-tracked")) {
                    img.setAttribute("data-preloader-tracked", "true");
                    const onImgDone = () => {
                        // Re-check everything when an image loads
                        // Debounce again to batch multiple image loads
                        scheduleCheck();
                    };
                    img.addEventListener("load", onImgDone);
                    img.addEventListener("error", onImgDone);
                }
            }
        });

        if (allReady) {
            initiateHide();
        }
    }

    function initiateHide() {
        if (isTransitioning || !preloader.classList.contains("hidden")) {
            setTimeout(() => {
                preloader.classList.add("hidden");
                isTransitioning = false;
            }, FADE_OUT_DELAY);
        }
    }

    let stabilizationTimer;
    function scheduleCheck() {
        clearTimeout(stabilizationTimer);
        stabilizationTimer = setTimeout(checkReadiness, DOM_STABILIZATION_DELAY);
    }

    // --- triggers ---

    // 1. Initial Load
    window.addEventListener("load", () => {
        scheduleCheck();
    });

    // 2. Click Navigation (Internal Links)
    document.addEventListener("click", function (e) {
        const target = e.target.closest("a");
        if (target && target.href && target.href.startsWith(window.location.origin)) {
            const isBlank = target.getAttribute("target") === "_blank";
            const isHash = target.href.includes("#");
            const isSamePage = target.href === window.location.href;

            if (!isBlank && !isHash && !isSamePage) {
                showPreloader();
            }
        }
    });

    // 3. History Navigation (Back/Forward)
    window.addEventListener("popstate", () => {
        showPreloader();
    });

    // 4. Dash Content Injection (MutationObserver)
    const observer = new MutationObserver(function (mutations) {
        let significantMutation = false;

        mutations.forEach((mutation) => {
            if (mutation.addedNodes.length > 0) {
                significantMutation = true;
            }
        });

        if (significantMutation) {
            // New content arrived.
            // If we aren't showing the loader (e.g. minor update), we might not want to force it?
            // But requirement says "Every page transition". 
            // Usually internal Dash Nav triggers the click listener => shows loader.
            // Then this observer sees content => schedules check => hides loader.

            // If we are already transitioning, just debounce the check.
            if (isTransitioning) {
                scheduleCheck();
            }
        }
    });

    const contentDiv = document.getElementById("page-content");
    if (contentDiv) {
        observer.observe(contentDiv, { childList: true, subtree: true });
    }
});
