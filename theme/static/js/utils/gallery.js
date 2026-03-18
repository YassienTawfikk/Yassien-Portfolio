/**
 * Reusable Gallery class for modal-based image navigation.
 *
 * Supports two data modes:
 *   - 'single' (default): each trigger has data-src with one image URL.
 *     All triggers form a flat navigable list.
 *   - 'json-array': each trigger has data-certs with a JSON array of URLs.
 *     Clicking a trigger opens a sub-gallery of that trigger's images.
 *
 * Usage:
 *   new Gallery({
 *       triggerSelector: '.cert-thumb-trigger',
 *       modalId:         'certificate-modal',
 *       imageId:         'modal-cert-image',
 *       prevBtnId:       'btn-prev',
 *       nextBtnId:       'btn-next',
 *       dataMode:        'single'           // or 'json-array'
 *   });
 */
class Gallery {
    constructor(config) {
        this.triggerSelector = config.triggerSelector;
        this.modalId = config.modalId;
        this.imageId = config.imageId;
        this.prevBtnId = config.prevBtnId;
        this.nextBtnId = config.nextBtnId;
        this.dataMode = config.dataMode || 'single';

        this.items = [];
        this.currentIndex = 0;
        this.modalEl = document.getElementById(this.modalId);
        this.modalImage = document.getElementById(this.imageId);
        this.prevBtn = document.getElementById(this.prevBtnId);
        this.nextBtn = document.getElementById(this.nextBtnId);

        if (!this.modalEl || !this.modalImage) return;

        this.modal = new bootstrap.Modal(this.modalEl);
        this._bindTriggers();
        this._bindNavigation();
        this._bindKeyboard();
    }

    // ── Trigger binding ─────────────────────────────────────────
    _bindTriggers() {
        const triggers = document.querySelectorAll(this.triggerSelector);

        if (this.dataMode === 'single') {
            // Flat list — collect all trigger sources
            triggers.forEach(el => {
                this.items.push(el.getAttribute('data-src'));
            });

            triggers.forEach((el, idx) => {
                el.addEventListener('click', () => {
                    this.currentIndex = idx;
                    this.modalImage.src = this.items[this.currentIndex];
                    this.modalImage.classList.remove('anim-next', 'anim-prev', 'is-switching');
                    this._updateButtons();
                    this.modal.show();
                });
            });
        } else {
            // JSON array — each trigger has its own sub-gallery
            triggers.forEach(trigger => {
                trigger.addEventListener('click', () => {
                    const raw = trigger.getAttribute('data-certs');
                    try {
                        this.items = JSON.parse(raw || '[]');
                    } catch (e) {
                        console.error('Gallery: failed to parse data-certs', e);
                        const fallback = trigger.getAttribute('data-src');
                        this.items = fallback ? [fallback] : [];
                    }

                    this.currentIndex = 0;

                    if (this.items.length > 0) {
                        this.modalImage.src = this.items[0];
                        this.modalImage.classList.remove('anim-next', 'anim-prev', 'is-switching');
                        this._updateButtons();
                        this.modal.show();
                    }
                });
            });
        }
    }

    // ── Navigation ──────────────────────────────────────────────
    _bindNavigation() {
        if (this.prevBtn) {
            this.prevBtn.addEventListener('click', () => {
                if (this.currentIndex > 0) this._navigate(-1);
            });
        }
        if (this.nextBtn) {
            this.nextBtn.addEventListener('click', () => {
                if (this.currentIndex < this.items.length - 1) this._navigate(1);
            });
        }
    }

    _navigate(direction) {
        const newIndex = this.currentIndex + direction;
        if (newIndex < 0 || newIndex >= this.items.length) return;

        this.currentIndex = newIndex;
        const newSrc = this.items[this.currentIndex];

        // 1. Hide immediately
        this.modalImage.classList.add('is-switching');
        this.modalImage.classList.remove('anim-next', 'anim-prev');

        // 2. Swap source, then animate in
        setTimeout(() => {
            this.modalImage.src = newSrc;

            requestAnimationFrame(() => {
                this.modalImage.classList.remove('is-switching');
                this.modalImage.classList.add(direction === 1 ? 'anim-next' : 'anim-prev');
            });
        }, 200);

        this._updateButtons();
    }

    _updateButtons() {
        if (this.prevBtn) {
            this.prevBtn.disabled = (this.currentIndex === 0);
            this.prevBtn.style.display = this.items.length <= 1 ? 'none' : 'flex';
        }
        if (this.nextBtn) {
            this.nextBtn.disabled = (this.currentIndex === this.items.length - 1);
            this.nextBtn.style.display = this.items.length <= 1 ? 'none' : 'flex';
        }
    }

    // ── Keyboard ────────────────────────────────────────────────
    _bindKeyboard() {
        document.addEventListener('keydown', (e) => {
            if (!this.modalEl.classList.contains('show')) return;
            if (e.key === 'ArrowLeft' && this.currentIndex > 0) {
                this._navigate(-1);
            } else if (e.key === 'ArrowRight' && this.currentIndex < this.items.length - 1) {
                this._navigate(1);
            }
        });
    }
}
