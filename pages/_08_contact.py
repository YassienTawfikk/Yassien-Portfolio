from dash import html
from utils.json_utils import get_json_values
from components.footer_navigation import FooterNavigation


# Define layout
layout = html.Div([
    html.Link(rel="stylesheet", href="../static/css/_08_contact.css"),
    html.H1("Contact Me", className='head-font title', style={'textAlign': 'center', 'marginTop': '50px'}),
    FooterNavigation("Back to Home", "/")
])
