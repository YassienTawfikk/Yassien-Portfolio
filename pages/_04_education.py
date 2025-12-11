from dash import html
from utils.json_utils import get_json_values

# Constants for paths
CONFIG_FILE_PATH = "data/_04_education.json"
CSS_FILE_PATH = "../static/css/_04_education.css"

image01, image02, university, faculty, degree, expected_graduation, description, biomedical_courses, technical_courses, mathematics_courses = \
    (
        get_json_values(CONFIG_FILE_PATH, [
            ("image_01",),
            ("image_02",),
            ("university",),
            ("faculty",),
            ("degree",),
            ("expected_graduation",),
            ("description",),
            ("key_courses", "biomedical_engineering"),
            ("key_courses", "ai_and_cs"),
            ("key_courses", "mathematics_and_theory"),
        ])
    )

# Define layout
layout = html.Div([
    html.Link(rel="stylesheet", href=CSS_FILE_PATH),
    html.Div(className='image-holder', children=[
        html.Div(children=[html.Img(src=image01)]),
        html.Div(children=[html.Img(src=image02)])
    ]),
    html.Div(className='education-container', children=[
        html.Span('Education', className='head-font title'),
        html.Span(university + " - " + faculty, className='subtitle body-font'),
        html.Span(degree + ' - Expected Graduation: ' + expected_graduation, className='subsubtitle body-font'),
        html.Span(description, className='body-text body-font'),
        html.Div([
            html.Span('Key Courses', className='head-font'),
            html.Ul([
                html.Li('Core Biomedical Courses:', className='body-font courses-head'),
                html.Ul([
                    html.Li(course, className='body-font courses-lists') for course in biomedical_courses
                ], className='list-body-font'),
                html.Li('Technical and Programming Courses:', className='body-font courses-head'),
                html.Ul([
                    html.Li(course, className='body-font courses-lists') for course in technical_courses
                ], className='list-body-font'),
                html.Li('Mathematics Courses:', className='body-font courses-head'),
                html.Ul([
                    html.Li(course, className='body-font courses-lists') for course in mathematics_courses
                ], className='list-body-font'),
            ]),
        ], className='courses-container'),
    ]),

], className='education-port')
