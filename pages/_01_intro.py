from dash import html
from utils.json_utils import get_json_values
from components.footer_navigation import FooterNavigation

# Constants for paths
CONFIG_FILE_PATH = "data/_01_intro.json"
CONFIG_DB_FILE_PATH = "data/db_data.json"
CSS_FILE_PATH = "../static/css/_01_intro.css"

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
    html.Link(rel="stylesheet", href=CSS_FILE_PATH),
    html.Div(className="intro-wrapper", children=[
        html.Div(className="profile-section", children=[
            html.Img(src=IMAGE_SRC)
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
