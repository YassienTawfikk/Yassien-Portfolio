from dash import html, callback, Input, Output, State, ALL, ctx, no_update
import dash_bootstrap_components as dbc
from src.utils.json_utils import get_json_values
from src.components.footer_navigation import FooterNavigation

# Constants for paths
CONFIG_FILE_PATH = "src/data/skills.json"

skill_categories = get_json_values(CONFIG_FILE_PATH, [("skill_categories",)])


def create_skill_card(skill):
    """Create a large card focused on the skill icon (image)."""
    children = [
        html.Img(src=skill.get('image_url', ''), className='skill-icon'),
        html.Span(skill['name'], className='skill-name body-font'),
    ]
    
    if 'details' in skill:
        children.append(html.Span(skill['details'], className='skill-details-hint body-font'))
        
    return html.Div(
        children, 
        className='skill-card',
        id={'type': 'skill-card', 'index': skill['name']},
        n_clicks=0
    )


def create_category_section(category):
    """Create a section for a category with a grid of skill cards."""
    return html.Div([
        html.Div([
            html.I(className=f"{category['category_icon']} category-icon"),
            html.Span(category['category'], className='category-title head-font'),
        ], className='category-header'),
        
        html.P(category['description'], className='category-desc body-font'),
        
        html.Div([
            create_skill_card(skill) for skill in category['skills']
        ], className='skills-grid')
        
    ], className='category-section')

modal = dbc.Modal(
    [
        dbc.ModalHeader(
            [
                dbc.ModalTitle("Skill Details", id="skill-modal-title", className="modal-title-custom"),
                dbc.Button("×", id="modal-close", className="modal-close-btn", n_clicks=0)
            ],
            className="modal-header-custom",
            close_button=False # We use our own button
        ),
        dbc.ModalBody(id="skill-modal-body", className="modal-body-custom"),
    ],
    id="skill-modal",
    is_open=False,
    centered=True,
    className="skill-modal-custom",
    backdrop=True,
)

layout = html.Div([
    html.Div([
        html.Span('Skills', className='skills-title head-font'),
        html.Div([
            create_category_section(cat) for cat in skill_categories
        ], className='all-skills-container'),
    ], className='skills-page main-container'),
    
    modal,
    FooterNavigation("About Me", "/about")
])

@callback(
    Output("skill-modal", "is_open"),
    Output("skill-modal-title", "children"),
    Output("skill-modal-body", "children"),
    Input({"type": "skill-card", "index": ALL}, "n_clicks"),
    Input("modal-close", "n_clicks"),
    State("skill-modal", "is_open"),
    prevent_initial_call=True
)
def toggle_modal(card_clicks, close_clicks, is_open):
    triggered_id = ctx.triggered_id
    
    if not triggered_id:
        return no_update, no_update, no_update
        
    if triggered_id == "modal-close":
        return False, no_update, no_update
        
    if isinstance(triggered_id, dict) and triggered_id.get('type') == 'skill-card':
        skill_name = triggered_id['index']
        
        # Find the skill description
        description = "No description available."
        found_skill = None
        
        for category in skill_categories:
            for skill in category['skills']:
                if skill['name'] == skill_name:
                    found_skill = skill
                    break
            if found_skill:
                break
        
        if found_skill:
            description = found_skill.get('description', description)
            
            content = html.Div([
                html.Img(src=found_skill.get('image_url', ''), className='modal-skill-icon'),
                html.P(description, className='modal-skill-desc')
            ])
            
            return True, skill_name, content
            
    return no_update, no_update, no_update
