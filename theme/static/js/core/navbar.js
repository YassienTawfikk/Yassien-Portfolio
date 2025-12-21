document.addEventListener('DOMContentLoaded', function () {
    let timer;

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
            console.log('Trigger or NavBlock not found, retrying...');
            setTimeout(setupNavInteraction, 500); // Retry setting up interactions every 500ms
        }
    }

    setupNavInteraction();
});
