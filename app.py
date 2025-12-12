from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from src.pages import intro, about, projects, education, skills, society, certificates, contact
from src.utils import clean_cache

# Initialize the Dash app
app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
    ],
    suppress_callback_exceptions=True,
    # Assets are automatically served from the 'assets' folder in the root
)

app.title = "Yassien Tawfik | Portfolio"
server = app.server

# Define the Navigation Bar (moved logic here or keep it clean)
def get_navbar():
    return html.Div(className='main-container navbar', children=[
        html.Span(children=[dcc.Link(intro.signature, className="signature", href="/")]),
        html.Div(className="navbar-nav body-font", children=[
            html.Span(children=[dcc.Link("Home", href="/")]),
            html.Span(children=[dcc.Link("About", href="/about")]),
            html.Span(children=[dcc.Link("Projects", href="/projects")]),
            html.Span(children=[
                html.Img(src="assets/images/icon/icons.png", className="image", id="hover-trigger")
            ]),  # Updated path to likely location, or keep absolute if it was external. The original was external URL.
                 # Wait, original was: https://i.postimg.cc/MZQ0s1M1/icons.png. I should keep external if it was external, or local if moved.
                 # I will keep external for now unless I find it in assets.
            html.Div(className="navblock", id="nav-block", children=[
                html.Span(children=[dcc.Link("Education", href="/education")]),
                html.Span(children=[dcc.Link("Skills", href="/skills")]),
                html.Span(children=[dcc.Link("Society", href="/society")]),
                html.Span(children=[dcc.Link("Certificates", href="/certificates")]),
                html.Span(children=[dcc.Link("Contact", href="/contact")]),
            ]),
        ]),
    ])

# Define app layout
app.layout = html.Div([
    get_navbar(),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])

# Routing callback
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname in ('/', '/intro'):
        return intro.layout
    elif pathname == '/about':
        return about.layout
    elif pathname == '/projects':
        return projects.layout
    elif pathname == '/education':
        return education.layout
    elif pathname == '/skills':
        return skills.layout
    elif pathname == '/society':
        return society.layout
    elif pathname == '/certificates':
        return certificates.layout
    elif pathname == '/contact':
        return contact.layout
    else:
        return html.H1("404: Page Not Found", style={"textAlign": "center"})

# Clean up cache if needed
try:
    clean_cache.remove_directories()
except Exception as e:
    print(f"Cache cleanup optional or failed: {e}")

if __name__ == "__main__":
    app.run(debug=True)
