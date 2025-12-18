from dash import html, dcc
import json
from src.components.footer_navigation import FooterNavigation


try:
    with open('src/data/contact.json', 'r') as f:
        contact_data = json.load(f)
except FileNotFoundError:
    contact_data = {
        "profile": {"name": "Yassien Tawfik", "location": "Cairo", "image": ""},
        "direct_contact": {"email": "", "phone": ""},
        "social_channels": []
    }

profile = contact_data.get('profile', {})
direct = contact_data.get('direct_contact', {})
socials = contact_data.get('social_channels', [])


social_metadata = {
    str(i): {
        'data-notify-title': social.get('notification_title'),
        'data-notify-desc': social.get('notification_description'),
        'data-href': social['url']
    }
    for i, social in enumerate(socials)
    if social.get('notification_title')
}

layout = html.Div([
    
    dcc.Store(id='social-metadata', data=social_metadata),
    html.Div([
        html.Div([
            html.Img(src=profile.get('image'), alt="Contact Visual")
        ], className="contact-visual-section"),

        html.Div([
        html.Div([
            html.H1("Let's Connect", className="unified-page-title title-left underline-150px")
        ], className=""), # contact-title-block removed class name to avoid conflict but kept div for structure if needed

            html.Div([
                
                html.Div([
                    html.A(
                        direct.get('email', 'Email Me'), 
                        href=f"mailto:{direct.get('email', '')}", 
                        className="contact-direct-link head-font",
                        id="contact-email-text" 
                    ),
                    html.Button(
                        html.I(className="fa-regular fa-copy"),
                        className="copy-btn",
                        id="copy-email-btn",
                        title="Copy Email"
                    ),
                    html.Span("", id="email-copy-feedback", className="copy-feedback")
                ], className="copy-container"),

                html.Div([
                    html.P(direct.get('phone', ''), className="contact-phone-text", id="contact-phone-text"),
                    html.Button(
                        html.I(className="fa-regular fa-copy"),
                        className="copy-btn",
                        id="copy-phone-btn",
                        title="Copy Phone"
                    ),
                    html.Span("", id="phone-copy-feedback", className="copy-feedback")
                ], className="copy-container")

            ], className="contact-info-brief"),

            html.Div([
                # Check if social item needs notification
                html.A(
                    html.I(className=f"fa-brands fa-{social.get('platform', '').lower()}" if social.get('platform', '').lower() != 'linkhub' else "fa-solid fa-link"),
                    id={'type': 'social-link', 'index': i},
                    title=social.get('platform'),
                    **({
                        'href': '#',
                        # data attributes kept for backup/semantics, but logic relies on store
                        'data-href': social['url'],
                    } if social.get('notification_title') else {
                        'href': social['url'],
                        'target': '_blank'
                    })
                ) for i, social in enumerate(socials)
            ], className="contact-social-row"),

            html.Form([
                
                html.Div([
                    html.Div([
                        html.Label("Name", htmlFor="from_name", className="zen-label"),
                        dcc.Input(id="from_name", type="text", className="zen-input", required=True, autoComplete="off")
                    ], className="zen-group"),

                    html.Div([
                        html.Label("Email", htmlFor="reply_to", className="zen-label"),
                        dcc.Input(id="reply_to", type="email", className="zen-input", required=True, autoComplete="off")
                    ], className="zen-group"),

                    html.Div([
                        html.Label("Message", htmlFor="message", className="zen-label"),
                        dcc.Textarea(id="message", className="zen-input", required=True, rows=3)
                    ], className="zen-group"),

                    html.Button("Send Message", type="submit", className="zen-submit", id="zen-submit-btn"),
                    html.Div(id="zen-form-feedback", className="zen-feedback")
                ])

            ], id="zen-contact-form", className="contact-form-container")

        ], className="contact-content-section")

    ], className="contact-wrapper"),

    html.Div([
        html.Div(id='modal-overlay-bg', className='modal-overlay-bg'),

        html.Div([
            html.Div([
                html.H2("", className="notification-title", id="notification-title"),
                html.P("", className="notification-message", id="confirm-message-text"),
                html.Div([
                    html.Button("Continue to Site", id="confirm-ok", className="action-btn ok-btn"),
                    # Cancel button removed per user request
                ], className="notification-actions")
            ], className="notification-box")
        ], className="viewer notification-viewer", id="confirm-modal-content")
    ], id="cv-modal", className="modal-backdrop"),

    FooterNavigation("Back to Home", "/", style={'marginTop': '0'})
])

from dash import clientside_callback, Input, Output, State, MATCH, ALL

clientside_callback(
    r"""
    function(n_clicks, metadata) {
        // Identify which input triggered the callback
        const ctx = dash_clientside.callback_context;
        if (!ctx.triggered.length) return window.dash_clientside.no_update;

        const triggeredIdStr = ctx.triggered[0].prop_id;
        
        // Handle Social Link Clicks
        if (triggeredIdStr.includes('social-link')) {
            // Find the clicked index
            const match = triggeredIdStr.match(/"index":(\d+)/);
            if (match) {
                const index = match[1]; // Keep as string for dict lookup
                
                // Look up data in the Store
                const linkData = metadata[index];
                
                // If this link has notification data
                if (linkData) {
                    document.getElementById('notification-title').textContent = linkData['data-notify-title'];
                    document.getElementById('confirm-message-text').textContent = linkData['data-notify-desc'];
                    
                    document.getElementById('confirm-ok').dataset.targetUrl = linkData['data-href'];
                    
                    const modal = document.getElementById('cv-modal');
                    modal.style.display = 'flex';
                    // Trigger reflow for transition
                    void modal.offsetWidth;
                    modal.classList.add('show');
                    document.body.classList.add('modal-open');
                    
                    return window.dash_clientside.no_update;
                }
            }
        }
        
        return window.dash_clientside.no_update;
    }
    """,
    Output('cv-modal', 'style'), # Dummy output
    Input({'type': 'social-link', 'index': ALL}, 'n_clicks'),
    State('social-metadata', 'data'), 
)

clientside_callback(
    """
    function(ok_clicks, bg_clicks) {
        const ctx = dash_clientside.callback_context;
        if (!ctx.triggered.length) return window.dash_clientside.no_update;
        
        const triggerId = ctx.triggered[0].prop_id;
        const modal = document.getElementById('cv-modal');
        
        if (triggerId === 'confirm-ok.n_clicks') {
            const targetUrl = document.getElementById('confirm-ok').dataset.targetUrl;
            if (targetUrl) {
                window.open(targetUrl, '_blank');
            }
        }
        
        // Close Modal
        modal.classList.remove('show');
        document.body.classList.remove('modal-open');
        setTimeout(() => {
            modal.style.display = 'none';
        }, 300); // Match transition duration
        
        return window.dash_clientside.no_update;
    }
    """,
    Output('notification-title', 'children'), # Dummy output
    Input('confirm-ok', 'n_clicks'),
    Input('modal-overlay-bg', 'n_clicks')
)
