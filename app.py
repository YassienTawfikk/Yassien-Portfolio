from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from src.components.navbar import Navbar
from src.routes import render_page_content
from src.utils import clean_cache

# Initialize the Dash app
app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
    ],
    suppress_callback_exceptions=True,
    title="Yassien Tawfik | Portfolio"
)

server = app.server

# Define app layout
app.layout = html.Div([
    Navbar(),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])

# Routing callback
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    return render_page_content(pathname)

# Clean up cache if needed
try:
    clean_cache.remove_directories()
except Exception as e:
    print(f"Cache cleanup optional or failed: {e}")

if __name__ == "__main__":
    app.run(debug=True)
