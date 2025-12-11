from dash import html, dcc, Input, Output
from dash_app import app  # Ensure you import the Dash app instance
from pages import _01_intro, _02_about, _03_projects, _04_education, _05_skills, _06_society, _07_certificates, _08_contact
import os


# Routing callback
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname in ['/', '/intro']:
        return _01_intro.layout
    elif pathname == '/about':
        return _02_about.layout
    elif pathname == '/projects':
        return _03_projects.layout
    elif pathname == '/education':
        return _04_education.layout
    elif pathname == '/skills':
        return _05_skills.layout
    elif pathname == '/society':
        return _06_society.layout
    elif pathname == '/certificates':
        return _07_certificates.layout
    elif pathname == '/contact':
        return _08_contact.layout
    else:
        return html.H1("404: Page Not Found", style={"textAlign": "center"})


app.layout = html.Div([
    html.Div(className='navbar', children=[
        # html.Span(intro.signature, className="signature"),
        html.Span(children=[html.A(_01_intro.signature, className="signature", href="/")]),
        html.Div(className="navbar-nav body-font", children=[
            html.Span(children=[html.A("Home", href="/")]),
            html.Span(children=[html.A("About", href="/about")]),
            html.Span(children=[html.A("Projects", href="/projects")]),
            html.Span(children=[html.Img(src="https://i.postimg.cc/MZQ0s1M1/icons.png", className="image", id="hover-trigger")]),
            html.Div(className="navblock", children=[
                html.Span(children=[html.A("Education", href="/education")]),
                html.Span(children=[html.A("Skills", href="/skills")]),
                html.Span(children=[html.A("Society", href="/society")]),
                html.Span(children=[html.A("Certificates", href="/certificates")]),
                html.Span(children=[html.A("Contact", href="/contact")])
            ], id="nav-block")
        ])
    ]),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])
