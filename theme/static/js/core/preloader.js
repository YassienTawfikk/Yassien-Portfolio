/* Global Preloader Behavior */
document.addEventListener("DOMContentLoaded", function () {
    const preloader = document.getElementById("global-preloader");
    if (!preloader) return;

    const MIN_VISIBLE_TIME = 550;
    const MAX_INITIAL_WAIT = 2800;
    const TRANSITION_FAILSAFE = 3500;
    const DOM_STABILIZATION_DELAY = 80;

    const shownAt = performance.now();
    let transitionTimer;
    let hidden = false;

    function wait(ms) {
        return new Promise((resolve) => setTimeout(resolve, ms));
    }

    function waitForImage(img) {
        if (!img || (img.complete && img.naturalWidth > 0)) {
            return Promise.resolve();
        }

        return new Promise((resolve) => {
            const done = () => resolve();
            img.addEventListener("load", done, { once: true });
            img.addEventListener("error", done, { once: true });
        }).then(() => {
            if (img.decode && img.complete && img.naturalWidth > 0) {
                return img.decode().catch(() => undefined);
            }
            return undefined;
        });
    }

    function getCriticalImages() {
        return Array.from(document.querySelectorAll(".main-content img[data-preload-critical]"));
    }

    function raceWithTimeout(promise, timeout) {
        return Promise.race([
            promise,
            wait(timeout)
        ]);
    }

    function hidePreloader() {
        if (hidden) return;

        const elapsed = performance.now() - shownAt;
        const remaining = Math.max(0, MIN_VISIBLE_TIME - elapsed);

        hidden = true;
        clearTimeout(transitionTimer);

        setTimeout(() => {
            preloader.classList.add("hidden");
        }, remaining);
    }

    function showForNavigation() {
        if (!preloader.classList.contains("hidden")) return;

        preloader.classList.remove("hidden");
        clearTimeout(transitionTimer);
        transitionTimer = setTimeout(() => {
            preloader.classList.add("hidden");
        }, TRANSITION_FAILSAFE);
    }

    function readyInitialView() {
        setTimeout(() => {
            const imagePromises = getCriticalImages().map(waitForImage);
            raceWithTimeout(Promise.all(imagePromises), MAX_INITIAL_WAIT)
                .then(hidePreloader)
                .catch(hidePreloader);
        }, DOM_STABILIZATION_DELAY);
    }

    readyInitialView();
    window.addEventListener("load", hidePreloader, { once: true });
    window.addEventListener("pageshow", function (event) {
        if (event.persisted) hidePreloader();
    });

    document.addEventListener("click", function (event) {
        const link = event.target.closest("a");
        if (!link || !link.href || event.defaultPrevented) return;
        if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;

        const url = new URL(link.href, window.location.href);
        const isSameOrigin = url.origin === window.location.origin;
        const isSameDocument = url.pathname === window.location.pathname && url.search === window.location.search;
        const isHashOnly = isSameDocument && url.hash;
        const opensNewContext = link.target && link.target !== "_self";
        const isDownload = link.hasAttribute("download");

        if (isSameOrigin && !isHashOnly && !opensNewContext && !isDownload) {
            showForNavigation();
        }
    });
});
