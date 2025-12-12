from dash import html

def FooterNavigation(next_page_name, next_page_url, style=None):
    """
    Creates a standardized footer navigation component pointing to the next page.
    """
    return html.Div(className='footer-nav-container', style=style, children=[
        html.A(className='footer-nav-link', href=next_page_url, children=[
            html.Span("Next Chapter", className='footer-nav-label body-font'),
            html.Span(className='footer-nav-title head-font', children=[
                next_page_name,
                html.I(className="fas fa-arrow-right footer-arrow")
            ])
        ])
    ])
