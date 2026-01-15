"""
Componentes de cartões KPI
"""

from dash import html
import dash_bootstrap_components as dbc
from config import CARD_STYLE, COLOR_TEXT_TITLE


def criar_kpi_card(titulo, id_valor, width_md=3):
    """
    Cria um cartão KPI
    
    Args:
        titulo (str): Título do KPI
        id_valor (str): ID do elemento que receberá o valor
        width_md (int): Largura em colunas (Bootstrap)
        
    Returns:
        dbc.Col: Coluna com o cartão KPI
    """
    return dbc.Col(
        dbc.Card([
            html.H6(titulo, className="text-muted"),
            html.H3(id=id_valor, className="fw-bold", style={"color": COLOR_TEXT_TITLE})
        ], style=CARD_STYLE),
        width=12, md=width_md, className="mb-3"
    )
