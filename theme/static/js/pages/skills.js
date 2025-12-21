document.addEventListener('DOMContentLoaded', function () {
    const skillModalEl = document.getElementById('skill-modal');
    const skillModal = new bootstrap.Modal(skillModalEl);
    const modalTitle = document.getElementById('skill-modal-title');
    const modalBody = document.getElementById('skill-modal-body');

    document.querySelectorAll('.skill-card').forEach(card => {
        card.addEventListener('click', function () {
            const name = this.getAttribute('data-name');
            const desc = this.getAttribute('data-desc');
            const img = this.getAttribute('data-img');

            modalTitle.textContent = name;

            modalBody.innerHTML = `
                <div class="text-center">
                    <img src="${img}" class="modal-skill-icon" style="max-height: 100px; margin-bottom: 20px;">
                    <p class="modal-skill-desc">${desc}</p>
                </div>
            `;

            skillModal.show();
        });
    });
});
