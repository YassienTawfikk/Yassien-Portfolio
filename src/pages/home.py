from dash import html
from src.utils.json_utils import get_json_values
from src.components.footer_navigation import FooterNavigation

# Constants for paths
CONFIG_FILE_PATH = "src/data/home.json"
CONFIG_DB_FILE_PATH = "src/data/db_data.json"

# Fetch data safely
full_name = get_json_values(CONFIG_DB_FILE_PATH, [("personal_information", "name")])
names = full_name.split() if full_name else ["Unknown"]
signature = names[0] + names[1]

intro_brief, IMAGE_SRC, CV_SRC = get_json_values(CONFIG_FILE_PATH, [
    ("brief",),
    ("profile photo",),
    ("cv",),
])

# Define layout
layout = html.Div([
    # CSS is auto-loaded from assets/ folder
    html.Div(className="intro-wrapper", children=[
        html.Div(className="profile-section", children=[
            html.Img(src=IMAGE_SRC, key="home-intro-image")
        ]),
        html.Div(className="heading-section", children=[
            html.Span(className="name-title", children=[
                html.Span(names[0], className="head-font first-name"),
                html.Span(names[1], className="head-font"),
            ]),
            html.Span(intro_brief, className="intro-brief body-font"),
            html.A(
                html.Button("Résumé", className="resume-button"),
                href=CV_SRC,
                target="_blank"
            )
        ])
    ]),
    FooterNavigation("About Me", "/about", style={'marginTop': '0'})
])
