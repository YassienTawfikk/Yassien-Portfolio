document.addEventListener('DOMContentLoaded', function () {
    let timer;
    let retryCount = 0;
    const maxRetries = 10;

    function setupNavInteraction() {
        const trigger = document.getElementById('hover-trigger');
        const navBlock = document.getElementById('nav-block');

        if (trigger && navBlock) {
            console.log('Trigger and NavBlock found, adding event listeners.');

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

            trigger.addEventListener('click', function (e) {
                if (window.innerWidth <= 768) {
                    e.stopPropagation();
                    if (navBlock.style.display === 'flex') {
                        navBlock.style.display = 'none';
                    } else {
                        navBlock.style.display = 'flex';
                        navBlock.style.flexDirection = 'column';
                    }
                }
            });

            document.addEventListener('click', function (e) {
                if (window.innerWidth <= 768) {
                    if (!trigger.contains(e.target) && !navBlock.contains(e.target)) {
                        navBlock.style.display = 'none';
                    }
                }
            });
        } else {
            retryCount++;
            if (retryCount < maxRetries) {
                console.warn(`Navbar elements not found, retrying (${retryCount}/${maxRetries})...`);
                setTimeout(setupNavInteraction, 500);
            } else {
                console.warn('Navbar elements not found after maximum retries. Aborting setup.');
            }
        }
    }

    setupNavInteraction();
});
