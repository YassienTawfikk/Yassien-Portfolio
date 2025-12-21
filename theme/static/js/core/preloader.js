/* Smart Global Preloader Logic */
document.addEventListener("DOMContentLoaded", function () {
    const preloader = document.getElementById("global-preloader");
    const FADE_OUT_DELAY = 500;
    const FAILSAFE_TIMEOUT = 15000;
    const DOM_STABILIZATION_DELAY = 100;

    let failsafeTimer;
    let isTransitioning = false;

    // --- Core Visualization Control ---

    function showPreloader() {
        if (preloader && preloader.classList.contains("hidden")) {
            preloader.classList.remove("hidden");
            isTransitioning = true;

            // Always set a failsafe when showing
            clearTimeout(failsafeTimer);
            failsafeTimer = setTimeout(forceHide, FAILSAFE_TIMEOUT);
        }
    }

    function forceHide() {
        if (preloader && !preloader.classList.contains("hidden")) {
            console.warn("Preloader failsafe triggered: forcing hide.");
            hidePreloader();
        }
    }

    function hidePreloader() {
        if (preloader && !preloader.classList.contains("hidden")) {
            // Cancel failsafe since we are closing naturally (or forced)
            clearTimeout(failsafeTimer);

            setTimeout(() => {
                preloader.classList.add("hidden");
                isTransitioning = false;
            }, FADE_OUT_DELAY);
        }
    }

    // --- Strict Wait Logic ---

    function waitForImagesAndHide() {
        // give the DOM a moment to settle (unfolding logic, etc)
        setTimeout(() => {
            // Select all images in the content area (including lazy loaded ones, as we want the "fully loaded" feel)
            // Note: Since we have aggressive pre-caching, this should be fast.
            const images = Array.from(document.querySelectorAll("#page-content img"));

            if (images.length === 0) {
                hidePreloader();
                return;
            }

            // User requested explicit 15-second timeout or until images are loaded
            const loadFailsafe = setTimeout(() => {
                console.warn("Preloader timeout (15s) reached. Forcing hide.");
                hidePreloader();
            }, 15000);

            const imagePromises = images.map((img) => {
                return new Promise((resolve) => {
                    // specific check for already loaded images
                    if (img.complete && img.naturalHeight !== 0) {
                        resolve();
                    } else {
                        // attach listeners
                        img.addEventListener("load", () => resolve(), { once: true });
                        img.addEventListener("error", () => resolve(), { once: true }); // resolve on error too so we don't hang
                    }
                });
            });

            Promise.all(imagePromises)
                .then(() => {
                    clearTimeout(loadFailsafe); // Clear the failsafe if we finish early
                    hidePreloader();
                })
                .catch((e) => {
                    console.error("Preloader error:", e);
                    hidePreloader();
                });

        }, DOM_STABILIZATION_DELAY);
    }

    // --- Triggers ---

    // 1. Initial Load
    window.addEventListener("load", () => {
        waitForImagesAndHide();
    });

    // Track current path to detect actual page changes vs hash changes
    let currentPath = window.location.pathname;

    // 2. Click Navigation (Internal Links)
    document.addEventListener("click", function (e) {
        const target = e.target.closest("a");
        if (target && target.href && target.href.startsWith(window.location.origin)) {
            const isBlank = target.getAttribute("target") === "_blank";

            // robust check for same-page hash navigation
            // If path and query are same, but hash is different (or present), it's a local jump
            const isSamePage = (target.pathname === window.location.pathname) &&
                (target.search === window.location.search);

            const hasHash = target.getAttribute("href").includes("#") || target.hash.length > 0;

            // If it's a hash jump on the same page, do NOT show preloader
            if (isSamePage && hasHash) {
                return;
            }

            // Normal Navigation Check
            if (!isBlank && !isSamePage) {
                showPreloader();
            }
        }
    });

    // 3. History Navigation
    window.addEventListener("popstate", () => {
        // Only trigger if the actual path changed (ignore hash changes)
        const newPath = window.location.pathname;
        if (newPath !== currentPath) {
            currentPath = newPath;
            showPreloader();
        }
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
            // New content injected by Dash.
            // If we are currently showing the loader (from click listener), this logic will check images & hide it.
            // If the loader wasn't showing (background update?), this might hide strictly, but that's okay.
            waitForImagesAndHide();
        }
    });

    const contentDiv = document.getElementById("page-content");
    if (contentDiv) {
        observer.observe(contentDiv, { childList: true, subtree: true });
    }
});
