import json
import dash_bootstrap_components as dbc
from dash import html, callback, clientside_callback, Input, Output, State, ALL, ctx, dcc
from src.components.footer_navigation import FooterNavigation


def load_credentials_data():
    with open('src/data/credentials.json', 'r') as f:
        return json.load(f)

data = load_credentials_data()

# Unified list for Gallery Navigation
ALL_GALLERY_ITEMS = data["fieldExperience"]["items"] + data["coursesAndCertificates"]["items"]



def create_credential_card(item, card_type="internship"):
    """
    Creates a unified grid card for both Internships and Certificates.
    Includes explicit Action Footer for better Link UX.
    Includes Overlay Icon for Image Affordance (Mobile).
    """
    image_src = item.get("certificateImage", "/assets/images/placeholder.jpg")
    
    if card_type == "internship":
        title = item.get("role", "Unknown Role")
        subtitle_text = item.get("organization", "")
        subtitle_link = item.get("organizationLink") # Can be None
        
        date_str = item.get("date", "")
        type_str = item.get("type", "Experience")
        
        description = item.get("description", "")
        github_link = item.get("github_link")
        
    else: # certificate
        title = item.get("title", "Unknown Certificate")
        subtitle_text = item.get("issuer", "")
        subtitle_link = item.get("issuerLink") # Added field if exists
        
        date_str = item.get("date", "")
        type_str = "Certification"
        
        description = None
        github_link = None # Certs usually don't have code, but if needed can add

    
    # Image Container (Trigger for Modal)
    image_section = html.Div(
        className="card-image-container",
        id={'type': 'cert-thumb', 'index': item['id']}, # Universal ID pattern
        children=[
            html.Img(src=image_src, className="card-image"),
            html.Div(
                html.I(className="fas fa-expand"),
                className="card-overlay-icon"
            )
        ]
    )
    
    # Subtitle (Organization/Issuer)
    if subtitle_link:
        subtitle_comp = html.A(subtitle_text, href=subtitle_link, target="_blank", className="card-org-link body-font")
    else:
        subtitle_comp = html.Span(subtitle_text, className="card-org-link body-font", style={"borderBottom": "none", "pointerEvents": "none"})
        
    action_buttons = []
    
    if subtitle_link:
        action_buttons.append(html.A(
            [html.I(className="fas fa-globe"), html.Span("Website")],
            href=subtitle_link,
            target="_blank",
            className="std-button std-button-secondary"
        ))
        
    if github_link:
        action_buttons.append(html.A(
            [html.I(className="fab fa-github"), html.Span("Code")],
            href=github_link,
            target="_blank",
            className="std-button std-button-primary"
        ))

    action_footer = None
    if action_buttons:
        action_footer = html.Div(className="card-actions", children=action_buttons)
        
    card_body = html.Div(className="card-content", children=[
        html.H3(title, className="card-title head-font"),
        html.Div(className="card-subtitle-row", children=[
            subtitle_comp
        ]),
        
        html.Div(className="card-meta-row body-font", children=[
            html.Span(date_str),
            html.Span("•"),
            html.Span(type_str, className="card-badge")
        ]),
        
        html.P(description, className="card-description body-font") if description else None,
        
        action_footer
    ])
    
    return html.Div(className="credential-card", children=[
        image_section,
        card_body
    ])


field_experience_section = html.Div(children=[
    html.H2(data["fieldExperience"]["displayTitle"], className="section-title head-font"),
    html.Div(className="credentials-grid", children=[
        create_credential_card(item, card_type="internship") for item in data["fieldExperience"]["items"]
    ])
])

certifications_section = html.Div(children=[
    html.H2(data["coursesAndCertificates"]["displayTitle"], className="section-title head-font"),
    html.Div(className="credentials-grid", children=[
        create_credential_card(item, card_type="certificate") for item in data["coursesAndCertificates"]["items"]
    ])
])

# Modal (Interactive Gallery)
modal = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Certificate View"), close_button=True),
        dbc.ModalBody(
            html.Div(
                className="gallery-container",
                children=[
                    html.Button(
                        html.I(className="fas fa-chevron-left"),
                        id="btn-prev",
                        className="gallery-nav prev",
                        title="Previous (Left Arrow)"
                    ),
                    
                    html.Img(
                        id="modal-cert-image",
                        src="",
                        className="gallery-image"
                    ),
                    
                    html.Button(
                        html.I(className="fas fa-chevron-right"),
                        id="btn-next",
                        className="gallery-nav next",
                        title="Next (Right Arrow)"
                    ),
                ]
            )
        ),
        # Invisible div for listener
        html.Div(id="keyboard-listener-trigger", style={"display": "none"})
    ],
    id="certificate-modal",
    size="xl", 
    is_open=False,
    centered=True,
    className="gallery-modal"
)



# ----------------------------------------------------------------------------------
# CLIENTSIDE INTERACTION LOGIC
# ----------------------------------------------------------------------------------
# All modal interactions (Open, Next, Prev) are handled via Clientside Callbacks
# in assets/js/gallery_callbacks.js to ensure Zero Latency and Atomic UI updates.
# ----------------------------------------------------------------------------------

layout = html.Div(children=[
    # DATA STORE: Holds all certificate data client-side for instant access
    dcc.Store(id='gallery-data', data=ALL_GALLERY_ITEMS),
    
    # STATE STORE: Tracks just the current numeric index
    dcc.Store(id='current-index', data=0),
    
    html.Div(className="main-container", children=[
        
        html.H1("Credentials", className="unified-page-title title-center underline-80px"),
        
        field_experience_section,
        
        html.Hr(className="section-divider"),
        
        certifications_section,
        
        modal
    ]),
    
    FooterNavigation("Skills", "/skills")
])



# 1. ATOMIC OPENING (Clientside)
# Instantly opens modal AND sets the correct image same-frame.
clientside_callback(
    "window.dash_clientside.gallery.open_gallery_modal",
    Output("certificate-modal", "is_open"),
    Output("modal-cert-image", "src"),
    Output("current-index", "data"),
    Input({'type': 'cert-thumb', 'index': ALL}, 'n_clicks'),
    State("gallery-data", "data"),
    prevent_initial_call=True
)

# 2. ZERO-LATENCY NAVIGATION (Clientside)
# Handles Next/Prev buttons instantly.
clientside_callback(
    "window.dash_clientside.gallery.navigate_gallery",
    Output("modal-cert-image", "src", allow_duplicate=True),
    Output("current-index", "data", allow_duplicate=True),
    Input("btn-prev", "n_clicks"),
    Input("btn-next", "n_clicks"),
    State("gallery-data", "data"),
    State("current-index", "data"),
    prevent_initial_call=True
)

# 3. KEYBOARD SHORTCUTS (Clientside)
# Listens for ArrowRight/ArrowLeft and triggers the buttons.
clientside_callback(
    """
    function(isOpen) {
        if (isOpen) {
            // Keyboard Navigation
            document.onkeydown = function(event) {
                if (event.key === 'ArrowRight') {
                    const btn = document.getElementById('btn-next');
                    if (btn) btn.click();
                } else if (event.key === 'ArrowLeft') {
                    const btn = document.getElementById('btn-prev');
                    if (btn) btn.click();
                }
            };
            
            // Swipe Navigation (Mobile)
            let touchStartX = 0;
            let touchEndX = 0;
            const threshold = 50; // Minimum distance for swipe
            
            function handleGesture() {
                if (touchEndX < touchStartX - threshold) {
                    // Swipe Left -> Next
                    const btn = document.getElementById('btn-next');
                    if (btn) btn.click();
                }
                if (touchEndX > touchStartX + threshold) {
                    // Swipe Right -> Prev
                    const btn = document.getElementById('btn-prev');
                    if (btn) btn.click();
                }
            }
            
            document.ontouchstart = function(event) {
                touchStartX = event.changedTouches[0].screenX;
            };
            
            document.ontouchend = function(event) {
                touchEndX = event.changedTouches[0].screenX;
                handleGesture();
            };
            
            return "Listening (Keys + Touch)";
        } else {
            // Cleanup
            document.onkeydown = null;
            document.ontouchstart = null;
            document.ontouchend = null;
            return "Not Listening";
        }
    }
    """,
    Output("keyboard-listener-trigger", "children"),
    Input("certificate-modal", "is_open")
)
