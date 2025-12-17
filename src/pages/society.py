from dash import html
import json
from src.components.footer_navigation import FooterNavigation
from src.utils.json_utils import get_json_values

CONFIG_FILE_PATH = "src/data/society.json"

with open(CONFIG_FILE_PATH, 'r') as file:
    data = json.load(file)

# Extracting all data for every entry in the 'society' section
society_data = []
# It's cleaner to just iterate over data['society'] directly, but keeping original logic structure for safety
# except for using the new path and imports.
for index in range(len(data['society'])):
    entry_data = get_json_values(CONFIG_FILE_PATH, [
        ("society", index, "role"),
        ("society", index, "organization"),
        ("society", index, "description"),
        ("society", index, "image_url"),
        ("society", index, "facebook_url"),
        ("society", index, "instagram_url"),
        ("society", index, "youtube_url"),
        ("society", index, "website_url"),
    ])
    society_data.append(entry_data)

# Define layout
layout = html.Div([
    # CSS auto-loaded
    html.Div("Society Involvement", className='society-title head-font'),
    html.Div(className='society-content-wrapper', children=[
        html.Button(id='scroll-left', children=[html.I(className="fa-solid fa-circle-chevron-left")]),
        html.Div(className='involvements-holder main-container', id='involvements-id', children=[
            html.Div(className='involvement-box', children=[
                html.Div(className='member-fig', children=[
                    html.Div(className='image', children=[
                        html.Img(src=society_data[i][3] if len(society_data[i]) > 3 else None)  # Checks if image link exists
                    ]),
                    html.Span(className='member-icons', children=[
                        html.A(href=society_data[i][4], target='_blank', children=[
                            html.I(className='fa-brands fa-facebook social-icons')
                        ]) if len(society_data[i]) > 4 and society_data[i][4] != "" else None,

                        html.A(href=society_data[i][5], target='_blank', children=[
                            html.I(className='fa-brands fa-instagram social-icons')
                        ]) if len(society_data[i]) > 5 and society_data[i][5] != "" else None,

                        html.A(href=society_data[i][6], target='_blank', children=[
                            html.I(className='fa-brands fa-youtube social-icons')
                        ]) if len(society_data[i]) > 6 and society_data[i][6] != "" else None,

                        html.A(href=society_data[i][7], target='_blank', children=[
                            html.I(className='fa-solid fa-globe social-icons')
                        ]) if len(society_data[i]) > 7 and society_data[i][7] != "" else None,
                    ])
                ]),
                html.Div(className='society-card-text', children=[
                    html.Span(society_data[i][0] if len(society_data[i]) > 0 else 'Unknown Title', className='head-font card-title'),
                    html.Span(society_data[i][1] if len(society_data[i]) > 1 else 'Unknown Subtitle', className='body-font card-subtitle'),
                    html.P(society_data[i][2] if len(society_data[i]) > 2 else 'No description available.', className='body-font card-paragraph')
                ])
            ]) for i in range(len(society_data))
        ]),
        html.Button(id='scroll-right', children=[html.I(className="fa-solid fa-circle-chevron-right")]),
    ]),
    FooterNavigation("Credentials", "/credentials")

],
    className='society-port')
