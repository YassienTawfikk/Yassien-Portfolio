from dash import html, callback, clientside_callback, Input, Output, State, ALL, ctx
import dash_bootstrap_components as dbc
import json
from src.components.footer_navigation import FooterNavigation
from src.utils.json_utils import get_json_values

CONFIG_FILE_PATH = "src/data/society.json"

with open(CONFIG_FILE_PATH, 'r') as file:
    data = json.load(file)

# Extracting all data for every entry in the 'society' section
society_data = []
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
        ("society", index, "certficates"),
    ])
    society_data.append(entry_data)

layout = html.Div([
    html.Div("Society Involvement", className='unified-page-title title-center underline-200px'),
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

                        html.Div(id={'type': 'society-cert-btn', 'index': i}, className='cert-icon-container', children=[
                            html.I(className='fa-solid fa-scroll social-icons')
                        ]) if len(society_data[i]) > 8 and society_data[i][8] else None,
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
    FooterNavigation("Get In Touch", "/contact"),

    # Certificate Modal
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Certificate View"), close_button=True),
            dbc.ModalBody(
                html.Div(
                    className="gallery-container",
                    children=[
                        html.Img(
                            id="society-modal-cert-image",
                            src="",
                            className="gallery-image"
                        ),
                    ]
                )
            ),
            html.Div(id="society-keyboard-listener-trigger", style={"display": "none"})
        ],
        id="society-certificate-modal",
        size="xl",
        is_open=False,
        centered=True,
        className="gallery-modal"
    )

],
    className='society-port')


@callback(
    [Output("society-certificate-modal", "is_open"),
     Output("society-modal-cert-image", "src")],
    [Input({'type': 'society-cert-btn', 'index': ALL}, 'n_clicks')],
    [State("society-certificate-modal", "is_open")],
    prevent_initial_call=True
)
def toggle_society_modal(n_clicks, is_open):
    if not any(n_clicks):
        return is_open, ""

    triggered_id = ctx.triggered_id
    if not triggered_id or triggered_id['type'] != 'society-cert-btn':
        return is_open, ""

    clicked_index = triggered_id['index']
    
    # Retrieve the image path from the pre-loaded data
    # Structure: society_data[i][8] is the certificate path
    if 0 <= clicked_index < len(society_data):
        image_src = society_data[clicked_index][8]
        return True, image_src
    
    return is_open, ""


# ----------------------------------------------------------------------------------
# KEYBOARD SHORTCUTS (Clientside)
# Listens for Escape key to close modal without exiting Full Screen
# ----------------------------------------------------------------------------------
clientside_callback(
    """
    function(isOpen) {
        if (isOpen) {
            document.onkeydown = function(event) {
                if (event.key === 'Escape') {
                    // Prevent exiting Full Screen
                    event.preventDefault();
                    event.stopPropagation();
                    
                    // Manually trigger the close button
                    const closeBtn = document.querySelector('#society-certificate-modal .btn-close');
                    if (closeBtn) closeBtn.click();
                }
            };
            return "Listening for Escape";
        } else {
            document.onkeydown = null;
            return "Not Listening";
        }
    }
    """,
    Output("society-keyboard-listener-trigger", "children"),
    Input("society-certificate-modal", "is_open")
)
