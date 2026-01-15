"""
Componente de barra lateral com navegação
"""

from dash import html, dcc
from config import SIDEBAR_STYLE


def criar_sidebar():
    """
    Cria a barra lateral com navegação entre páginas
    
    Returns:
        html.Div: Componente da sidebar
    """
    return html.Div(
        [
            html.H3("Dashboard", className="display-6", style={"color": "#ffffff", "fontWeight": "bold"}),
            html.H5("Rossi", className="fw-bold text-white mt-2"),
            html.Hr(style={"borderColor": "white"}),
            
            # Navegação
            html.Div([
                dcc.Link(
                    "Consertos",
                    href="/",
                    className="nav-link text-white d-block mb-2",
                    style={"padding": "8px 12px", "borderRadius": "5px", "backgroundColor": "rgba(255,255,255,0.1)"}
                ),
                dcc.Link(
                    "Técnicos",
                    href="/novo",
                    className="nav-link text-white d-block mb-2",
                    style={"padding": "8px 12px", "borderRadius": "5px", "backgroundColor": "rgba(255,255,255,0.1)"}
                ),
            ]),
            
            html.Hr(style={"borderColor": "white", "marginTop": "30px"}),
            
            # Container para filtros específicos de cada página
            html.Div(id="filtros-container"),
            

        ],
        style=SIDEBAR_STYLE,
    )
