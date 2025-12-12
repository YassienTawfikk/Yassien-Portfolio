document.addEventListener('DOMContentLoaded', function () {
    let timer;  // Declare timer globally to manage hover interactions

    function setupNavInteraction() {
        const trigger = document.getElementById('hover-trigger');
        const navBlock = document.getElementById('nav-block');

        if (trigger && navBlock) {
            console.log('Trigger and NavBlock found, adding interactions.');

            // Universal Click Toggle Logic
            trigger.addEventListener('click', function (e) {
                e.stopPropagation(); // Prevent immediate close by document listener

                if (navBlock.classList.contains('nav-open')) {
                    navBlock.classList.remove('nav-open');
                } else {
                    navBlock.classList.add('nav-open');
                }
            });

            // Close menu when clicking outside (Universal)
            document.addEventListener('click', function (e) {
                // If click is outside trigger AND outside navBlock
                if (!trigger.contains(e.target) && !navBlock.contains(e.target)) {
                    navBlock.classList.remove('nav-open');
                }
            });
        } else {
            console.log('Trigger or NavBlock not found, retrying...');
            setTimeout(setupNavInteraction, 500); // Retry setting up interactions every 500ms
        }
    }

    setupNavInteraction();
});
