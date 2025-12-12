from dash import html
from src.components.footer_navigation import FooterNavigation

# Define layout
layout = html.Div([
    html.H1("Certificates", className='head-font title', style={'textAlign': 'center', 'marginTop': '50px'}),
    FooterNavigation("Get In Touch", "/contact")
])
