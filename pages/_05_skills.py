from dash import html
from utils.json_utils import get_json_values
from components.footer_navigation import FooterNavigation

# Constants for paths
CONFIG_FILE_PATH = "data/_05_skills.json"
CSS_FILE_PATH = "../static/css/_05_skills.css"

# Load data
skill_categories = get_json_values(CONFIG_FILE_PATH, [("skill_categories",)])


def create_skill_card(skill):
    """Create a large card focused on the skill icon (image)."""
    children = [
        # Use html.Img instead of html.I
        html.Img(src=skill.get('image_url', ''), className='skill-icon'),
        html.Span(skill['name'], className='skill-name body-font'),
    ]
    
    # Optionally display details if present
    if 'details' in skill:
        children.append(html.Span(skill['details'], className='skill-details-hint body-font'))
        
    return html.Div(children, className='skill-card')


def create_category_section(category):
    """Create a section for a category with a grid of skill cards."""
    return html.Div([
        # Header Section
        html.Div([
            html.I(className=f"{category['category_icon']} category-icon"),
            html.Span(category['category'], className='category-title head-font'),
        ], className='category-header'),
        
        # Description
        html.P(category['description'], className='category-desc body-font'),
        
        # Skills Grid
        html.Div([
            create_skill_card(skill) for skill in category['skills']
        ], className='skills-grid')
        
    ], className='category-section')


# Define layout
layout = html.Div([
    html.Link(rel="stylesheet", href=CSS_FILE_PATH),
    html.Div([
        html.Span('Skills', className='title head-font'),
        # Container
        html.Div([
            create_category_section(cat) for cat in skill_categories
        ], className='all-skills-container'),
    ], className='skills-page main-container'),
    FooterNavigation("Society", "/society")
])
