document.addEventListener('DOMContentLoaded', function () {
    let timer;  // Declare timer globally to manage hover interactions

    function setupNavInteraction() {
        const trigger = document.querySelector('.navbar-nav span:nth-child(4)');  // Select the fourth span as hover trigger
        const navBlock = document.querySelector('.navbar-nav .navblock');  // Select the navigation block

        if (trigger && navBlock) {
            console.log('Trigger and NavBlock found, adding event listeners.');

            // Display navBlock when hovering over the trigger span
            trigger.addEventListener('mouseover', function () {
                clearTimeout(timer); // Clear any previous timer
                navBlock.style.display = 'flex'; // Apply display flex to show navBlock
                navBlock.style.flexDirection = 'column'; // Ensure flex direction is column as per CSS
            });

            // Hide navBlock when the mouse leaves, with a delay
            navBlock.addEventListener('mouseleave', function () {
                timer = setTimeout(() => {
                    navBlock.style.display = 'none'; // Hide navBlock after delay
                }, 250); // 2.5-millisecond delay before hiding
            });

            // Cancel the timer if the mouse re-enters the navBlock
            navBlock.addEventListener('mouseover', function () {
                clearTimeout(timer); // Stop the hide timer
            });
        } else {
            console.log('Trigger or NavBlock not found, retrying...');
            setTimeout(setupNavInteraction, 500); // Retry setting up interactions every 500ms
        }
    }

    setupNavInteraction();
});
