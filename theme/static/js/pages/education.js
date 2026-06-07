document.addEventListener("DOMContentLoaded", () => {
    const track = document.getElementById("education-slider-track");
    const btnBsc = document.getElementById("btn-bsc");
    const btnMsc = document.getElementById("btn-msc");
    const dots = document.querySelectorAll(".slider-dots .dot");

    if (!track || !btnBsc || !btnMsc) return;

    let currentSlide = 0; // 0 for BSc, 1 for MSc

    function updateSlider(index) {
        currentSlide = index;
        track.style.transform = `translateX(-${currentSlide * 100}%)`;

        // Update buttons
        btnBsc.disabled = currentSlide === 0;
        btnMsc.disabled = currentSlide === 1;

        // Update dots
        dots.forEach((dot, i) => {
            if (i === currentSlide) {
                dot.classList.add("active");
            } else {
                dot.classList.remove("active");
            }
        });
    }

    btnBsc.addEventListener("click", () => {
        if (currentSlide > 0) updateSlider(currentSlide - 1);
    });

    btnMsc.addEventListener("click", () => {
        if (currentSlide < 1) updateSlider(currentSlide + 1);
    });

    dots.forEach((dot, index) => {
        dot.addEventListener("click", () => {
            updateSlider(index);
        });
    });
});
