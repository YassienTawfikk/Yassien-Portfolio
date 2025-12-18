from dash import html
from src.utils.json_utils import get_json_values
from src.components.footer_navigation import FooterNavigation


CONFIG_FILE_PATH = "src/data/about.json"

image01, image02, image03, description, vision, mission = get_json_values(CONFIG_FILE_PATH, [
    ("image_01",),
    ("image_02",),
    ("image_03",),
    ("description",),
    ("vision",),
    ("mission",),
])

layout = html.Div([
    html.Div(className='images-holder', children=[
        html.Span(className='image-box image', children=[html.Img(src=image01)]),
        html.Span(className='image-box image', children=[html.Img(src=image02)]),
        html.Span(className='image-box image', children=[html.Img(src=image03)])
    ]),
    html.Div(className='main-container', children=[
        html.Span(className='unified-page-title title-left underline-80percent', children="About Me"),
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
    FooterNavigation("Education", "/education")
])
