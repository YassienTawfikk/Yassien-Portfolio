from dash import html
import json
import os

CONFIG_FILE_PATH = "data/_03_projects.json"
CSS_FILE_PATH = "../static/css/_03_projects.css" 

# Load data
projects_list = []
try:
    with open(CONFIG_FILE_PATH, 'r') as f:
        data = json.load(f)
        projects_list = data.get("Projects", [])
except Exception as e:
    print(f"Error loading projects data: {e}")
    projects_list = []

def create_project_card(project):
    """
    Creates a Dash HTML component for a single project card.
    """
    title = project.get("title", "Untitled Project")
    short_desc = project.get("short_description", "")
    image_url = project.get("overview_image", "")
    tags = project.get("tags", [])
    tech_stack = project.get("tech_stack", [])
    github_link = project.get("github_link", "")
    live_demo = project.get("live_demo", "")
    
    # Limit displayed tags and tech stack to avoid clutter
    display_tags = tags[:3]
    display_tech = tech_stack[:5]

    return html.Div(className='project-card', children=[
        html.Div(className='project-image-container', children=[
            html.Img(src=image_url, className='project-image', alt=f"{title} Overview")
        ]),
        html.Div(className='project-content', children=[
            html.H3(title, className='project-title head-font'),
            
            html.Div(className='project-tags', children=[
                html.Span(tag, className='project-tag body-font') for tag in display_tags
            ]),
            
            html.P(short_desc, className='project-description body-font'),
            
            html.Div(className='project-tech-stack', children=[
                 html.Span(tech, className='tech-badge body-font') for tech in display_tech
            ]),
            
            html.Div(className='project-links', children=[
                html.A("Code", href=github_link, target="_blank", className='project-link-btn body-font') if github_link else None,
                html.A("Live Demo", href=live_demo, target="_blank", className='project-link-btn secondary body-font') if live_demo else None
            ])
        ])
    ])

# Define layout
layout = html.Div([
    html.Link(rel="stylesheet", href=CSS_FILE_PATH),
    html.Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"), # Ensure icons work if needed, generic import
    
    html.Div(className='projects-page-container main-container', children=[
        html.H1("Projects", className='page-title head-font'),
        
        html.Div(className='projects-grid', children=[
            create_project_card(proj) for proj in projects_list
        ])
    ])
])
