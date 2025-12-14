from dash import html, dcc
import json
from src.components.footer_navigation import FooterNavigation

# Load data
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

layout = html.Div([
    
    # Mirroring the 'intro-wrapper' structure from Home
    html.Div([
        
        # Left Side (Visual)
        html.Div([
            html.Img(src="/assets/images/contact/contact.jpg", alt="Contact Visual")
        ], className="contact-visual-section"),

        # Right Side (Content)
        html.Div([
            
            # Title Area
            html.Div([
                html.H1("Let's Connect", className="head-font")
            ], className="contact-title-block"),

            # Info Brief with Copy Buttons
            html.Div([
                
                # Email Group
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

                # Phone Group
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

            # Socials
            html.Div([
                 html.A(
                    html.I(className=f"fa-brands fa-{social['platform'].lower()}"),
                    href=social['url'],
                    target="_blank",
                    title=social['platform']
                ) for social in socials
            ], className="contact-social-row"),

            # The Form
            html.Form([
                
                html.Div([
                    # Name
                    html.Div([
                        html.Label("Name", htmlFor="from_name", className="zen-label"),
                        dcc.Input(id="from_name", type="text", className="zen-input", required=True, autoComplete="off")
                    ], className="zen-group"),

                    # Email
                    html.Div([
                        html.Label("Email", htmlFor="reply_to", className="zen-label"),
                        dcc.Input(id="reply_to", type="email", className="zen-input", required=True, autoComplete="off")
                    ], className="zen-group"),

                    # Message
                    html.Div([
                        html.Label("Message", htmlFor="message", className="zen-label"),
                        dcc.Textarea(id="message", className="zen-input", required=True, rows=3)
                    ], className="zen-group"),

                    # Submit
                    html.Button("Send Message", type="submit", className="zen-submit", id="zen-submit-btn"),
                    html.Div(id="zen-form-feedback", className="zen-feedback")
                ])

            ], id="zen-contact-form", className="contact-form-container")

        ], className="contact-content-section")

    ], className="contact-wrapper"),

    FooterNavigation("Back to Home", "/")
])
