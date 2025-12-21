
document.addEventListener('click', function (event) {
    const toggleBtn = event.target.closest('#navbar-toggle-btn');
    const navMenu = document.getElementById('navbar-menu-list');

    // Toggle Menu
    if (toggleBtn && navMenu) {
        toggleBtn.classList.toggle('active');
        navMenu.classList.toggle('active');

        // Update aria-expanded
        const isExpanded = toggleBtn.classList.contains('active');
        toggleBtn.setAttribute('aria-expanded', isExpanded);
    }

    // Close menu when clicking a link (mobile UX)
    if (event.target.closest('.nav-link') && navMenu && navMenu.classList.contains('active')) {
        const toggleBtn = document.getElementById('navbar-toggle-btn');
        if (toggleBtn) {
            toggleBtn.classList.remove('active');
            toggleBtn.setAttribute('aria-expanded', 'false');
        }
        navMenu.classList.remove('active');
    }

    // Close menu when clicking outside
    if (!event.target.closest('.navbar-container') && navMenu && navMenu.classList.contains('active')) {
        const toggleBtn = document.getElementById('navbar-toggle-btn');
        if (toggleBtn) {
            toggleBtn.classList.remove('active');
            toggleBtn.setAttribute('aria-expanded', 'false');
        }
        navMenu.classList.remove('active');
    }
});
