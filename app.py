from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from src.components.navbar import Navbar
from src.routes import render_page_content
from src.utils import clean_cache

app = Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
    ],
    external_scripts=[
        "https://cdn.jsdelivr.net/npm/@emailjs/browser@3/dist/email.min.js"
    ],
    suppress_callback_exceptions=True,
    title="Yassien Tawfik | Portfolio",
    meta_tags=[
        # Social Media Meta Tags (OG, Twitter)
        {'property': 'og:type', 'content': 'website'},
        {'property': 'og:title', 'content': 'Yassien Tawfik · Portfolio'},
        {'property': 'og:description', 'content': 'Explore my projects, skills, and professional experience.'},
        {'property': 'og:url', 'content': 'https://ytawfik-portfolio.vercel.app/'},
        {'property': 'og:image', 'content': 'https://ytawfik-portfolio.vercel.app/assets/images/icon/icon-512.png'},

        {'name': 'twitter:card', 'content': 'summary'},
        {'name': 'twitter:title', 'content': 'Yassien Tawfik · Portfolio'},
        {'name': 'twitter:description', 'content': 'Explore my projects, skills, and professional experience.'},
        {'name': 'twitter:image', 'content': 'https://ytawfik-portfolio.vercel.app/assets/images/icon/icon-512.png'}
    ]
)

# Template configuration for Dash to include Web App Icons and meta tags.
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        <link rel="icon" type="image/x-icon" href="/assets/images/icon/favicon.ico?v=2">
        {%css%}
        <!-- Web App Icons -->
        <link rel="apple-touch-icon" href="/assets/images/icon/apple-touch-icon.png?v=2"/>
        <link rel="icon" sizes="192x192" href="/assets/images/icon/icon-250.png?v=2"/>
        <link rel="icon" sizes="512x512" href="/assets/images/icon/icon-512.png?v=2"/>
    </head>
    <body>
        <div id="global-preloader">
            <h1 class="zen-signature">Yassien Tawfik</h1>
        </div>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

server = app.server

app.layout = html.Div([
    Navbar(),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    return render_page_content(pathname)

try:
    clean_cache.remove_directories()
except Exception as e:
    print(f"Cache cleanup optional or failed: {e}")

if __name__ == "__main__":
    app.run(debug=True)
