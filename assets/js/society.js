document.addEventListener("DOMContentLoaded", function () {
    setTimeout(function () {
        const scrollLeftButton = document.getElementById('scroll-left');
        const scrollRightButton = document.getElementById('scroll-right');
        const involvementHolder = document.getElementById('involvements-id'); // Corrected typo from 'involvments-id' if it was a typo

        console.log("Scroll Left Button:", scrollLeftButton);  // Debugging line
        console.log("Scroll Right Button:", scrollRightButton);  // Debugging line
        console.log("Involvement Holder:", involvementHolder);  // Debugging line

        if (scrollLeftButton && scrollRightButton && involvementHolder) {
            scrollLeftButton.addEventListener('click', function () {
                involvementHolder.scrollBy({left: -400, behavior: 'smooth'});
            });

            scrollRightButton.addEventListener('click', function () {
                involvementHolder.scrollBy({left: 400, behavior: 'smooth'});
            });
        } else {
            console.error("One or more elements are not found. Check their IDs.");
        }
    }, 500); // Delay script execution for 500ms
});
