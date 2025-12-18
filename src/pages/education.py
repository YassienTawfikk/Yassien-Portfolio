from dash import html
from src.utils.json_utils import get_json_values
from src.components.footer_navigation import FooterNavigation


CONFIG_FILE_PATH = "src/data/education.json"

image01, image02, university, faculty, degree, expected_graduation, gpa, description, biomedical_courses, technical_courses, mathematics_courses = \
    (
        get_json_values(CONFIG_FILE_PATH, [
            ("image_01",),
            ("image_02",),
            ("university",),
            ("faculty",),
            ("degree",),
            ("expected_graduation",),
            ("gpa",),
            ("description",),
            ("key_courses", "biomedical_engineering"),
            ("key_courses", "ai_and_cs"),
            ("key_courses", "mathematics_and_theory"),
        ])
    )

layout = html.Div([
    html.Div([
        html.Div(className='image-holder', children=[
            html.Div(children=[html.Img(src=image01)]),
            html.Div(children=[html.Img(src=image02)])
        ]),
        html.Div(className='education-container', children=[
            html.Span('Education', className='unified-page-title title-left underline-80px'),
            html.Span(university + " - " + faculty, className='subtitle body-font'),
            html.Span(degree + ' - Expected Graduation: ' + expected_graduation + ' - GPA: ' + gpa, className='subsubtitle body-font'),
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
    ], className='education-port'),
    FooterNavigation("Society", "/society", style={'marginTop': '0'})
])
