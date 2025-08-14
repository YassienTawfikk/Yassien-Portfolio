from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from utils import clean_cache  # Ensure this module is defined and accessible

# Initialize the Dash app with Bootstrap support
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)
app.title = "Yassien Tawfik | Portfolio"
server = app.server

# Import pages for the routing
from pages import _01_intro, _02_about, _03_projects, _04_education, _05_skills, _06_society, _07_certificates, \
    _08_contact


# Routing callback
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname in ('/', '/intro'):
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
    return html.H1("404: Page Not Found", style={"textAlign": "center"})


# Define app layout
app.layout = html.Div([
    # Place your JS file in ./assets/navbar.js (Dash auto-serves it). No need for html.Script here.
    html.Div(className='main-container navbar', children=[
        html.Span(children=[dcc.Link(_01_intro.signature, className="signature", href="/")]),
        html.Div(className="navbar-nav body-font", children=[
            html.Span(children=[dcc.Link("Home", href="/")]),
            html.Span(children=[dcc.Link("About", href="/about")]),
            html.Span(children=[dcc.Link("Projects", href="/projects")]),
            html.Span(children=[
                html.Img(src="https://i.postimg.cc/MZQ0s1M1/icons.png", className="image", id="hover-trigger")]),
            html.Div(className="navblock", id="nav-block", children=[
                html.Span(children=[dcc.Link("Education", href="/education")]),
                html.Span(children=[dcc.Link("Skills", href="/skills")]),
                html.Span(children=[dcc.Link("Society", href="/society")]),
                html.Span(children=[dcc.Link("Certificates", href="/certificates")]),
                html.Span(children=[dcc.Link("Contact", href="/contact")]),
            ]),
        ]),
    ]),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])

# Clean up cache directories
clean_cache.remove_directories()

# Main execution
server = app.server
if __name__ == "__main__":
    app.run(debug=True)
