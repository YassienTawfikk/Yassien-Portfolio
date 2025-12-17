from dash import html
import json
from src.components.footer_navigation import FooterNavigation
import os

CONFIG_FILE_PATH = "src/data/projects.json"

projects_list = []
try:
    with open(CONFIG_FILE_PATH, 'r') as f:
        data = json.load(f)
        projects_list = data.get("Projects", [])
except Exception as e:
    print(f"Error loading projects data: {e}")
    projects_list = []

def get_project_domain(title, tags):
    """
    Infers the primary domain/direction from tags and title.
    Returns a tuple (Domain Name, Icon Class).
    """
    tags_str = " ".join(tags).lower()
    title_lower = title.lower()
    
    # Explicit Overrides
    if "soundprints" in title_lower or "audiophileeq" in title_lower:
        return "Audio & Signal Processing", "fa-solid fa-wave-square"
    if "lifestream" in title_lower:
        return "Mobile & IoT System", "fa-solid fa-mobile-screen"
    if "sequencealignx" in title_lower:
        return "Biomedical Engineering", "fa-solid fa-heart-pulse"
    if "smartretailregressor" in title_lower or "predictiloan" in title_lower:
        return "Data Science & analytics", "fa-solid fa-chart-line"
    
    if "game" in tags_str:
        return "Game Development", "fa-solid fa-gamepad"
    if "medical" in tags_str or "biomedical" in tags_str or "healthcare" in tags_str:
        if "ai" in tags_str or "learning" in tags_str:
            return "Medical AI", "fa-solid fa-brain"
        return "Biomedical Engineering", "fa-solid fa-heart-pulse"
    if "deep learning" in tags_str or "machine learning" in tags_str or "data" in tags_str:
        return "AI & Data Science", "fa-solid fa-robot"
    if "computer vision" in tags_str or "image" in tags_str:
        return "Computer Vision", "fa-solid fa-eye"
    if "embedded" in tags_str or "hardware" in tags_str or "iot" in tags_str:
        return "Embedded Systems", "fa-solid fa-microchip"
    if "audio" in tags_str or "signal" in tags_str:
        return "Signal Processing", "fa-solid fa-wave-square"
    if "web" in tags_str or "mobile" in tags_str or "app" in tags_str:
        return "Web & Mobile App", "fa-solid fa-laptop-code"
    
    return "Software Engineering", "fa-solid fa-code"

def create_project_card(project, is_featured=False):
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
    
    domain_name, domain_icon = get_project_domain(title, tags)
    
    # Limit displayed tech stack to avoid clutter
    display_tech = tech_stack[:5]

    card_class = 'project-card featured-card' if is_featured else 'project-card'

    return html.Div(className=card_class, children=[
        html.Div(className='project-image-container', children=[
            html.Img(src=image_url, className='project-image', alt=f"{title} Overview"),
            html.Div(className="live-badge", children="LIVE DEMO") if is_featured else None
        ]),
        html.Div(className='project-content', children=[
            html.Div(className='project-domain-badge', children=[
                html.I(className=f"{domain_icon} domain-icon"),
                html.Span(domain_name, className='domain-text body-font')
            ]),
            
            html.H3(title, className='project-title head-font'),
            
            html.P(short_desc, className='project-description body-font'),
            
            html.P(short_desc, className='project-description body-font'),
            
            html.Div(className='tech-stack-section', children=[
                html.P("Tech Stack", className='tech-section-label head-font'),
                html.Div(className='project-tech-stack', children=[
                     html.Span(tech, className='tech-badge body-font') for tech in display_tech
                ])
            ]),
            
            html.Div(className='project-links', children=[
                html.A([html.I(className="fab fa-github"), " Code"], href=github_link, target="_blank", className='std-button std-button-primary') if github_link else None,
                html.A([html.I(className="fas fa-play"), " Live Demo"], href=live_demo, target="_blank", className='std-button std-button-secondary') if live_demo else None
            ])
        ])
    ])

featured_projects = [p for p in projects_list if p.get("live_demo")]
other_projects = [p for p in projects_list if not p.get("live_demo")]

categories = {
    "AI & Data Science": [],
    "Computer Vision & Image Processing": [],
    "Biomedical & Signal Processing": [],
    "Web, Mobile & Software": [],
    "Embedded Systems & IoT": [],
    "Game Development": []
}

for p in other_projects:
    tags_str = " ".join(p.get("tags", [])).lower()
    title = p.get("title", "").lower()
    
    if "lifestream" in title or "soundprints" in title:
         categories["Web, Mobile & Software"].append(p)
         continue
         
    if "game" in tags_str:
        categories["Game Development"].append(p)
    elif any(kw in tags_str for kw in ["deep learning", "machine learning", "data", "regression", "prediction", "analytics", "svm", "forest", "xgboost", "ml"]):
        categories["AI & Data Science"].append(p)
    elif "computer vision" in tags_str or "image" in tags_str:
        categories["Computer Vision & Image Processing"].append(p)
    elif "embedded" in tags_str or "arduino" in tags_str:
        categories["Embedded Systems & IoT"].append(p)
    elif "medical" in tags_str or "biomedical" in tags_str or "signal" in tags_str or "audio" in tags_str:
        categories["Biomedical & Signal Processing"].append(p)
    else:
        categories["Web, Mobile & Software"].append(p)

sections = []

sections.append(html.H1("Projects", className='page-title head-font'))

if featured_projects:
    sections.append(html.H2([html.I(className="fas fa-star"), " Featured Live Demos"], className='section-title featured-title head-font'))
    sections.append(html.Div(className='projects-grid featured-grid', children=[
        create_project_card(proj, is_featured=True) for proj in featured_projects
    ]))
    sections.append(html.Hr(className="section-divider"))

for category, projects in categories.items():
    if projects:
        sections.append(html.H2(category, className='section-title head-font'))
        sections.append(html.Div(className='projects-grid', children=[
            create_project_card(proj, is_featured=False) for proj in projects
        ]))

layout = html.Div([
    html.Div(className='projects-page-container main-container', children=sections),
    FooterNavigation("Credentials", "/credentials")
])
