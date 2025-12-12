from dash import html
from src.pages import home, about, projects, education, skills, society, certificates, contact

def render_page_content(pathname):
    """
    Determines which page layout to return based on the pathname.
    """
    if pathname in ('/', '/intro', '/home'):
        return home.layout
    elif pathname == '/about':
        return about.layout
    elif pathname == '/projects':
        return projects.layout
    elif pathname == '/education':
        return education.layout
    elif pathname == '/skills':
        return skills.layout
    elif pathname == '/society':
        return society.layout
    elif pathname == '/certificates':
        return certificates.layout
    elif pathname == '/contact':
        return contact.layout
    else:
        return html.H1("404: Page Not Found", style={"textAlign": "center"})
