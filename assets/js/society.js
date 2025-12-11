document.addEventListener("DOMContentLoaded", function () {
    // Function to initialize logic + observers
    function initSocietyScroll() {
        const leftBtn = document.getElementById('scroll-left');
        const rightBtn = document.getElementById('scroll-right');
        const holder = document.getElementById('involvements-id');

        if (!leftBtn || !rightBtn || !holder) return;

        // Check if listeners are already attached to avoid duplicates
        if (leftBtn.dataset.listenerAttached === "true") return;

        leftBtn.addEventListener('click', () => {
            holder.scrollBy({ left: -360, behavior: 'smooth' });
        });
        leftBtn.dataset.listenerAttached = "true";

        rightBtn.addEventListener('click', () => {
            holder.scrollBy({ left: 360, behavior: 'smooth' });
        });
        rightBtn.dataset.listenerAttached = "true";

        console.log("Society scroll initialized.");
    }

    // Attempt init immediately
    initSocietyScroll();

    // Use MutationObserver for SPA navigation changes
    const observer = new MutationObserver((mutations) => {
        // If DOM changes, try re-initializing (e.g., page navigation rendered new buttons)
        initSocietyScroll();
    });

    observer.observe(document.body, { childList: true, subtree: true });
});
