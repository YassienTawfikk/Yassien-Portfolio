from dash import html, dcc
from src.pages import home

def Navbar():
    """
    Returns the application navigation bar.
    Rebuilt with semantic HTML5 and cleaner structure.
    """
    nav_links = [
        ("Home", "/"),
        ("About", "/about"),
        ("Projects", "/projects"),
        ("Education", "/education"),
        ("Skills", "/skills"),
        ("Society", "/society"),
        ("Credentials", "/credentials"),
        ("Contact", "/contact"),
    ]

    return html.Nav(className="navbar", children=[
        html.Div(className="navbar-container", children=[
            # 1. Logo / Signature
            dcc.Link(
                html.Span(home.signature, className="navbar-logo"),
                href="/",
                className="navbar-brand"
            ),

            # 2. Mobile Menu Toggle
            html.Button(
                children=[
                    html.Span(className="hamburger-line"),
                    html.Span(className="hamburger-line"),
                    html.Span(className="hamburger-line"),
                ],
                id="navbar-toggle-btn",
                className="navbar-toggle",
                **{"aria-label": "Toggle navigation", "aria-expanded": "false"}
            ),

            # 3. Navigation Links
            html.Ul(id="navbar-menu-list", className="navbar-menu", children=[
                html.Li(
                    dcc.Link(label, href=href, className="nav-link")
                ) for label, href in nav_links
            ])
        ])
    ])
