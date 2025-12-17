import json
import dash_bootstrap_components as dbc
from dash import html, callback, Input, Output, ALL, ctx
from src.components.footer_navigation import FooterNavigation


def load_credentials_data():
    with open('src/data/credentials.json', 'r') as f:
        return json.load(f)

data = load_credentials_data()



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

    
    # Image Container (Trigger for Modal) - With Overlay Icon
    image_section = html.Div(
        className="card-image-container",
        id={'type': 'cert-thumb', 'index': item['id']}, # Universal ID pattern
        children=[
            html.Img(src=image_src, className="card-image"),
            # New Overlay Icon for Affordance
            html.Div(
                html.I(className="fas fa-expand"),
                className="card-overlay-icon"
            )
        ]
    )
    
    # Subtitle (Organization/Issuer) - Keep original link for redundancy
    if subtitle_link:
        subtitle_comp = html.A(subtitle_text, href=subtitle_link, target="_blank", className="card-org-link body-font")
    else:
        subtitle_comp = html.Span(subtitle_text, className="card-org-link body-font", style={"borderBottom": "none", "pointerEvents": "none"})
        
    # Action Buttons (Footer)
    action_buttons = []
    
    # Website Button
    if subtitle_link:
        action_buttons.append(html.A(
            [html.I(className="fas fa-globe"), html.Span("Website")],
            href=subtitle_link,
            target="_blank",
            className="action-btn website-btn body-font"
        ))
        
    # GitHub Button
    if github_link:
        action_buttons.append(html.A(
            [html.I(className="fab fa-github"), html.Span("Code")],
            href=github_link,
            target="_blank",
            className="action-btn github-btn body-font"
        ))

    action_footer = None
    if action_buttons:
        action_footer = html.Div(className="card-actions", children=action_buttons)
        
    card_body = html.Div(className="card-content", children=[
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

# Modal
modal = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Certificate View"), close_button=True),
        dbc.ModalBody(
            html.Img(id="modal-cert-image", src="", style={"width": "100%", "height": "auto", "borderRadius": "8px"})
        ),
    ],
    id="certificate-modal",
    size="lg",
    is_open=False,
    centered=True
)


layout = html.Div(children=[
    html.Div(className="main-container", children=[
        
        html.H1("Credentials", className="page-title head-font"),
        
        field_experience_section,
        
        html.Hr(className="section-divider"),
        
        certifications_section,
        
        modal
    ]),
    
    FooterNavigation("Skills", "/skills")
])





@callback(
    [Output("certificate-modal", "is_open"), Output("modal-cert-image", "src")],
    [Input({'type': 'cert-thumb', 'index': ALL}, 'n_clicks')],
    prevent_initial_call=True
)
def display_certificate(n_clicks):
    if not any(n_clicks):
         return False, ""
    
    triggered_id = ctx.triggered_id
    if not triggered_id or triggered_id['type'] != 'cert-thumb':
        return False, ""

    clicked_id = triggered_id['index']
    
    image_src = ""
    
    # Efficient Search: Combine both lists
    all_items = data["coursesAndCertificates"]["items"] + data["fieldExperience"]["items"]
    
    for item in all_items:
        if item["id"] == clicked_id:
            image_src = item.get("certificateImage", "")
            break
            
    return True, image_src
