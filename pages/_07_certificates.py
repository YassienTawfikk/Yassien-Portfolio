from dash import html
from utils.json_utils import get_json_values
from components.footer_navigation import FooterNavigation


# Define layout
layout = html.Div([
    html.Link(rel="stylesheet", href="../static/css/_07_certificates.css"),
    html.H1("Certificates", className='head-font title', style={'textAlign': 'center', 'marginTop': '50px'}),
    FooterNavigation("Get In Touch", "/contact")
])
