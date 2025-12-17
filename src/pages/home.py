from dash import html
from src.utils.json_utils import get_json_values
from src.components.footer_navigation import FooterNavigation


CONFIG_FILE_PATH = "src/data/home.json"
full_name, intro_brief, IMAGE_SRC, CV_SRC = get_json_values(CONFIG_FILE_PATH, [
    ("name",),
    ("brief",),
    ("profile photo",),
    ("cv",),
])

names = full_name.split() if full_name else ["Unknown"]
signature = names[0] + names[1]

layout = html.Div([
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
                html.Button("Résumé", className="std-button std-button-secondary std-button-lg"),
                href=CV_SRC,
                target="_blank"
            )
        ])
    ]),
    FooterNavigation("Projects", "/projects", style={'marginTop': '0'})
])
