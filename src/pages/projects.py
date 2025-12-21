from dash import html, Input, Output, State, ALL, callback, ctx
import dash_bootstrap_components as dbc
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
    Handles Live Demo and Video Demo independently.
    """
    title = project.get("title", "Untitled Project")
    short_desc = project.get("short_description", "")
    image_url = project.get("overview_image", "")
    tags = project.get("tags", [])
    tech_stack = project.get("tech_stack", [])
    github_link = project.get("github_link", "")
    
    # Independent resources
    live_demo = project.get("live_demo", "")
    video_demo = project.get("video_demo", "")
    
    domain_name, domain_icon = get_project_domain(title, tags)
    
    # Limit displayed tech stack to avoid clutter
    display_tech = tech_stack[:5]

    # Only apply 'featured-card' styling if it's in the featured section
    card_class = 'project-card featured-card' if is_featured else 'project-card'

    return html.Div(className=card_class, children=[
        html.Div(className='project-image-container', children=[
            html.Img(src=image_url, className='project-image', alt=f"{title} Overview"),
            # The Live Badge appears ONLY if it is in the Featured Section (implies Live Demo exists)
            html.Div(className="live-badge", children="LIVE DEMO") if is_featured else None
        ]),
        html.Div(className='project-content', children=[
            html.Div(className='project-domain-badge', children=[
                html.I(className=f"{domain_icon} domain-icon"),
                html.Span(domain_name, className='domain-text body-font')
            ]),
            
            html.H3(title, className='project-title head-font'),
            
            html.P(short_desc, className='project-description body-font'),
            
            html.Div(className='tech-stack-section', children=[
                html.P("Tech Stack", className='tech-section-label head-font'),
                html.Div(className='project-tech-stack', children=[
                     html.Span(tech, className='tech-badge body-font') for tech in display_tech
                ])
            ]),
            
            html.Div(className='project-links', children=[
                # GitHub Link
                html.A([html.I(className="fab fa-github"), " Code"], 
                       href=github_link, target="_blank", 
                       className='std-button std-button-primary') if github_link else None,
                
                # Live Demo Link (Independent)
                html.A([html.I(className="fas fa-play"), " Live Demo"], 
                       href=live_demo, target="_blank", 
                       className='std-button std-button-secondary') if live_demo else None,
                
                # Video Demo Button (Independent)
                html.Button([html.I(className="fas fa-video"), " Video Demo"],
                            id={'type': 'video-btn', 'index': title},
                            n_clicks=0,
                            className='std-button std-button-secondary') if video_demo else None
            ])
        ])
    ])

# --- Logic Separation ---
# 1. Featured Live: Strictly projects that HAVE a live_demo.
featured_projects = [p for p in projects_list if p.get("live_demo")]

# 2. Featured Video: Projects that HAVE a video_demo but NO live_demo.
featured_video_projects = [p for p in projects_list if p.get("video_demo") and not p.get("live_demo")]

# 3. Others: Strictly projects that have neither live_demo nor video_demo.
other_projects = [p for p in projects_list if not p.get("live_demo") and not p.get("video_demo")]

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

sections.append(html.H1("Projects", className='unified-page-title title-center underline-80px'))

# Only render Featured Section if there are actually projects with Live Demos
if featured_projects:
    sections.append(html.H2([html.I(className="fas fa-star"), " Featured Live Demos"], className='section-title featured-title head-font'))
    sections.append(html.Div(className='projects-grid featured-grid', children=[
        create_project_card(proj, is_featured=True) for proj in featured_projects
    ]))
    sections.append(html.Hr(className="section-divider"))

if featured_video_projects:
    sections.append(html.H2([html.I(className="fas fa-video"), " Featured Video Demos"], className='section-title featured-title head-font'))
    sections.append(html.Div(className='projects-grid featured-grid', children=[
        create_project_card(proj, is_featured=True) for proj in featured_video_projects
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
    FooterNavigation("Credentials", "/credentials"),
    
    # Video Modal
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Project Demo"), id="video-modal-header"),
            dbc.ModalBody(html.Div(id="video-modal-body")),
        ],
        id="video-modal",
        is_open=False,
        size="lg",
        centered=True,
    ),
])


@callback(
    [Output("video-modal", "is_open"),
     Output("video-modal-body", "children"),
     Output("video-modal-header", "children")],
    [Input({'type': 'video-btn', 'index': ALL}, 'n_clicks')],
    [State("video-modal", "is_open")],
    prevent_initial_call=True
)
def toggle_modal(video_clicks, is_open):
    triggered_id = ctx.triggered_id
    
    if not triggered_id:
        return is_open, None, "Project Demo"

    # If a video button was clicked
    if isinstance(triggered_id, dict) and triggered_id.get('type') == 'video-btn':
        project_title = triggered_id.get('index')
        
        # Find the project data
        project_data = next((p for p in projects_list if p.get("title") == project_title), None)
        
        if project_data:
            video_url = project_data.get("video_demo")
            
            if video_url:
                # Create video player (using HTML5 video tag)
                video_content = html.Video(
                    src=video_url,
                    controls=True,
                    autoPlay=True,
                    muted=True,
                    loop=True,
                    style={"width": "100%", "height": "auto"}
                )
            else:
                # Placeholder for missing videos (fallback)
                video_content = html.Div([
                    html.I(className="fas fa-video-slash", style={"fontSize": "3rem", "marginBottom": "1rem", "color": "#666"}),
                    html.H4("Video Demo Coming Soon", style={"color": "#ccc"}),
                    html.P("A demonstration video for this project is not yet available.", style={"color": "#888"})
                ], style={"textAlign": "center", "padding": "3rem"})
            
            return True, video_content, dbc.ModalTitle(project_title)
            
    return is_open, None, "Project Demo"