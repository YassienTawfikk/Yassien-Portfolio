document.addEventListener("DOMContentLoaded", () => {
    const track = document.getElementById("education-slider-track");
    const btnBsc = document.getElementById("btn-bsc");
    const btnMsc = document.getElementById("btn-msc");
    const dots = document.querySelectorAll(".slider-dots .dot");
    const images = document.querySelectorAll(".image-holder img");
    const firstImage = images.length > 0 ? images[0] : null;
    const secondImage = images.length > 1 ? images[1] : null;
    
    // Store initial MSc images
    const mscImage1 = firstImage ? firstImage.getAttribute("src") : "";
    const mscImage2 = secondImage ? secondImage.getAttribute("src") : "";

    // Preload BSc images to eliminate latency
    const preload1 = new Image(); preload1.src = "/images/education/cairo-university-1.webp";
    const preload2 = new Image(); preload2.src = "/images/education/cairo-university-2.webp";

    if (!track || !btnBsc || !btnMsc) return;

    let currentSlide = 0; // 0 for MSc, 1 for BSc

    function updateSlider(index) {
        currentSlide = index;
        track.style.transform = `translateX(-${currentSlide * 100}%)`;

        // Update hover behavior (only MSc images get original colors on hover)
        const imageHolder = document.querySelector(".image-holder");
        if (imageHolder) {
            if (currentSlide === 0) {
                imageHolder.classList.add("hover-color");
            } else {
                imageHolder.classList.remove("hover-color");
            }
        }

        // Update buttons
        btnMsc.disabled = currentSlide === 0;
        btnBsc.disabled = currentSlide === 1;

        // Update dots
        dots.forEach((dot, i) => {
            if (i === currentSlide) {
                dot.classList.add("active");
            } else {
                dot.classList.remove("active");
            }
        });

        // Helper to smoothly update an image with zero latency (true crossfade)
        const updateImage = (imgEl, newSrc) => {
            if (!imgEl) return;
            if (!imgEl.src.includes(newSrc)) {
                const wrapper = imgEl.parentElement;
                if (getComputedStyle(wrapper).position === 'static') {
                    wrapper.style.position = 'relative';
                }

                // Create a clone of the old image to fade out on top
                const clone = imgEl.cloneNode();
                clone.style.position = 'absolute';
                clone.style.top = '0';
                clone.style.left = '0';
                clone.style.width = '100%';
                clone.style.height = '100%';
                clone.style.objectFit = 'cover';
                clone.style.transition = 'opacity 0.4s ease';
                clone.style.zIndex = '1';
                clone.style.filter = 'grayscale(100%)';
                
                wrapper.appendChild(clone);
                
                // Instantly update the real image underneath
                imgEl.src = newSrc;
                
                // Trigger the fade out of the clone on the next frame
                requestAnimationFrame(() => {
                    requestAnimationFrame(() => {
                        clone.style.opacity = '0';
                        setTimeout(() => {
                            clone.remove();
                        }, 400); // Remove after transition finishes
                    });
                });
            }
        };

        // Update images based on current slide
        const targetSrc1 = currentSlide === 0 ? mscImage1 : "/images/education/cairo-university-1.webp";
        const targetSrc2 = currentSlide === 0 ? mscImage2 : "/images/education/cairo-university-2.webp";
        
        updateImage(firstImage, targetSrc1);
        updateImage(secondImage, targetSrc2);
    }

    btnMsc.addEventListener("click", () => {
        if (currentSlide > 0) updateSlider(currentSlide - 1);
    });

    btnBsc.addEventListener("click", () => {
        if (currentSlide < 1) updateSlider(currentSlide + 1);
    });

    dots.forEach((dot, index) => {
        dot.addEventListener("click", () => {
            updateSlider(index);
        });
    });
});
