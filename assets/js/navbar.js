document.addEventListener('DOMContentLoaded', function () {
    let timer;  // Declare timer globally to manage hover interactions

    function setupNavInteraction() {
        const trigger = document.getElementById('hover-trigger');  // Select by ID
        const navBlock = document.getElementById('nav-block');  // Select by ID

        if (trigger && navBlock) {
            console.log('Trigger and NavBlock found, adding event listeners.');

            // Desktop Hover Logic
            trigger.addEventListener('mouseover', function () {
                if (window.innerWidth > 768) {
                    clearTimeout(timer);
                    navBlock.style.display = 'flex';
                    navBlock.style.flexDirection = 'column';
                }
            });

            navBlock.addEventListener('mouseleave', function () {
                if (window.innerWidth > 768) {
                    timer = setTimeout(() => {
                        navBlock.style.display = 'none';
                    }, 250);
                }
            });

            navBlock.addEventListener('mouseover', function () {
                if (window.innerWidth > 768) {
                    clearTimeout(timer);
                }
            });

            // Mobile Click Logic
            trigger.addEventListener('click', function (e) {
                if (window.innerWidth <= 768) {
                    e.stopPropagation(); // Prevent immediate close by document listener
                    // Toggle visibility
                    if (navBlock.style.display === 'flex') {
                        navBlock.style.display = 'none';
                    } else {
                        navBlock.style.display = 'flex';
                        navBlock.style.flexDirection = 'column';
                    }
                }
            });

            // Close menu when clicking outside (Mobile)
            document.addEventListener('click', function (e) {
                if (window.innerWidth <= 768) {
                    // If click is outside trigger AND outside navBlock
                    if (!trigger.contains(e.target) && !navBlock.contains(e.target)) {
                        navBlock.style.display = 'none';
                    }
                }
            });
        } else {
            console.log('Trigger or NavBlock not found, retrying...');
            setTimeout(setupNavInteraction, 500); // Retry setting up interactions every 500ms
        }
    }

    setupNavInteraction();
});
