from dash import html
from utils.json_utils import get_json_values
from components.footer_navigation import FooterNavigation

# Constants for paths
CONFIG_FILE_PATH = "data/_02_about.json"
CSS_FILE_PATH = "../static/css/_02_about.css"

image01, image02, image03, description, vision, mission = get_json_values(CONFIG_FILE_PATH, [
    ("image_01",),
    ("image_02",),
    ("image_03",),
    ("description",),
    ("vision",),
    ("mission",),
])

# Define layout
layout = html.Div([
    html.Link(rel="stylesheet", href=CSS_FILE_PATH),
    html.Div(className='images-holder', children=[
        html.Span(className='image-box image', children=[html.Img(src=image01)]),
        html.Span(className='image-box image', children=[html.Img(src=image02)]),
        html.Span(className='image-box image', children=[html.Img(src=image03)])
    ]),
    html.Div(className='main-container', children=[
        html.Span(className='about-title head-font', children="About Me"),
        html.Div(className='about-content', children=[
            html.Div(className='body-font topic', children=description),
            html.Div(className='topic', children=[
                html.Span(className='head-font', children='Vision'),
                html.Span(className='body-font', children=vision)
            ]),
            html.Div(className='topic', children=[
                html.Span(className='head-font', children='Mission'),
                html.Span(className='body-font', children=mission)
            ])
        ])
    ]),
    FooterNavigation("Projects", "/projects")
])
