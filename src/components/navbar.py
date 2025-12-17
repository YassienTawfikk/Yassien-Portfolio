from dash import html, dcc
from src.pages import home

def Navbar():
    """
    Returns the application navigation bar component.
    """
    nav_links = [
        ("Home", "/"),
        ("Projects", "/projects"),
        ("Credentials", "/credentials"),
        ("Skills", "/skills"),
        ("About", "/about"),
        ("Education", "/education"),
        ("Society", "/society"),
        ("Contact", "/contact"),
    ]

    return html.Nav(className="navbar", children=[
        html.Div(className="navbar-container", children=[
            dcc.Link(
                html.Span(home.signature, className="navbar-logo"),
                href="/",
                className="navbar-brand"
            ),

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

            html.Ul(id="navbar-menu-list", className="navbar-menu", children=[
                html.Li(
                    dcc.Link(label, href=href, className="nav-link")
                ) for label, href in nav_links
            ])
        ])
    ])
