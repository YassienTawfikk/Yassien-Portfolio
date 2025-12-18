if (!window.dash_clientside) {
    window.dash_clientside = {};
}

window.dash_clientside.gallery = {

    /**
     * ATOMIC OPENING
     * Triggered by clicking any certificate thumbnail.
     * 
     * @param {Array} n_clicks_list - List of n_clicks from all trigger buttons
     * @param {Array} gallery_data - The static list of all certificates
     * @returns {Array} [is_open (bool), image_src (str), current_index (int)]
     */
    open_gallery_modal: function (n_clicks_list, gallery_data) {
        // Dash triggers callback even if no clicks, check if any exists
        const triggered = dash_clientside.callback_context.triggered;

        if (!triggered || triggered.length === 0) {
            return [false, "", 0];
        }

        // Identify which item was clicked
        // Trigger ID format is: {"index":"exp_001","type":"cert-thumb"}
        // We need to match the 'index' (which is the item ID) to our gallery data

        // Use a safe check to ensure we have a valid trigger
        const trigger_id_str = triggered[0].prop_id.split('.')[0];
        let clicked_id = null;

        try {
            const trigger_obj = JSON.parse(trigger_id_str);
            clicked_id = trigger_obj.index;
        } catch (e) {
            // Fallback or error if not JSON
            return [false, "", 0];
        }

        if (!gallery_data) {
            return [true, "", 0];
        }

        // Find the numeric index and source for this specific ID
        let new_index = 0;
        let new_src = "";

        for (let i = 0; i < gallery_data.length; i++) {
            if (gallery_data[i].id === clicked_id) {
                new_index = i;
                new_src = gallery_data[i].certificateImage || "/assets/images/placeholder.jpg";
                break;
            }
        }

        // Return [is_open, src, local_store_index]
        return [true, new_src, new_index];
    },

    /**
     * ZERO-LATENCY NAVIGATION
     * Triggered by Next/Prev buttons
     * 
     * @param {number} prev_clicks
     * @param {number} next_clicks
     * @param {Array} gallery_data 
     * @param {number} current_index
     * @returns {Array} [image_src (str), new_index (int)]
     */
    navigate_gallery: function (prev_clicks, next_clicks, gallery_data, current_index) {
        if (!gallery_data || gallery_data.length === 0) {
            return ["", 0];
        }

        const triggered = dash_clientside.callback_context.triggered;
        if (!triggered || triggered.length === 0) {
            return [window.dash_clientside.no_update, window.dash_clientside.no_update];
        }

        const trigger_id = triggered[0].prop_id;
        const total = gallery_data.length;
        let new_index = current_index;
        let direction = null;

        if (trigger_id.includes('btn-next')) {
            new_index = (current_index + 1) % total;
            direction = 'next';
        } else if (trigger_id.includes('btn-prev')) {
            new_index = (current_index - 1 + total) % total;
            direction = 'prev';
        }

        const new_src = gallery_data[new_index].certificateImage || "/assets/images/placeholder.jpg";

        // ANIMATION LOGIC
        const image_el = document.getElementById('modal-cert-image');
        if (image_el && direction) {
            // 1. Hide immediately to prevent ghosting of old image
            image_el.classList.add('is-switching');
            image_el.classList.remove('anim-next', 'anim-prev');

            // 2. Wait for Dash to update the src (approx 50-100ms) + buffer
            setTimeout(() => {
                // Safari Fix: Double RAF ensures the 'hidden' state is fully painted 
                // before the new animation class is applied.
                requestAnimationFrame(() => {
                    requestAnimationFrame(() => {
                        // 3. Unhide and animate
                        image_el.classList.remove('is-switching');
                        if (direction === 'next') {
                            image_el.classList.add('anim-next');
                        } else {
                            image_el.classList.add('anim-prev');
                        }
                    });
                });
            }, 250); // 250ms delay to ensure source is swapped
        }

        return [new_src, new_index];
    }
};
