from dash import html, dcc
from src.pages import home

def Navbar():
    """
    Returns the application navigation bar.
    """
    return html.Div(className='main-container navbar', children=[
        html.Span(children=[dcc.Link(home.signature, className="signature", href="/")]),
        html.Div(className="navbar-nav body-font", children=[
            html.Span(children=[dcc.Link("Home", href="/")]),
            html.Span(children=[dcc.Link("About", href="/about")]),
            html.Span(children=[dcc.Link("Projects", href="/projects")]),
            html.Span(children=[
                html.I(className="fa-solid fa-bars", id="hover-trigger")
            ]),
            html.Div(className="navblock", id="nav-block", children=[
                html.Span(children=[dcc.Link("Education", href="/education")]),
                html.Span(children=[dcc.Link("Skills", href="/skills")]),
                html.Span(children=[dcc.Link("Society", href="/society")]),
                html.Span(children=[dcc.Link("Certificates", href="/certificates")]),
                html.Span(children=[dcc.Link("Contact", href="/contact")]),
            ]),
        ]),
    ])
