"""
Componentes de cartões KPI
"""

from dash import html
import dash_bootstrap_components as dbc
from config import CARD_STYLE, COLOR_TEXT_TITLE


def criar_kpi_card(titulo, id_valor, width_md=3, include_mom=False):
    """
    Cria um cartão KPI com suporte opcional para comparação mês a mês
    
    Args:
        titulo (str): Título do KPI
        id_valor (str): ID do elemento que receberá o valor
        width_md (int): Largura em colunas (Bootstrap)
        include_mom (bool): Se True, inclui indicador de mês anterior
        
    Returns:
        dbc.Col: Coluna com o cartão KPI
    """
    card_content = [
        html.H6(titulo, className="text-muted", style={"marginBottom": "8px"}),
        html.H3(id=id_valor, className="fw-bold", style={"color": COLOR_TEXT_TITLE, "marginBottom": "0"})
    ]
    
    # Se incluir MoM, adiciona os containers para MoM e YoY (serão preenchidos via callback)
    if include_mom:
        card_content.insert(0, html.Div([
            html.Div(id=f"{id_valor}-mom", style={"marginBottom": "4px"}),
            html.Div(id=f"{id_valor}-yoy")
        ], style={
            "position": "absolute",
            "top": "12px",
            "right": "16px",
            "fontSize": "0.75rem",
            "textAlign": "right",
            "lineHeight": "1.3"
        }))
    
    card_style = {**CARD_STYLE, "position": "relative"}
    
    return dbc.Col(
        dbc.Card(card_content, style=card_style),
        width=12, md=width_md, className="mb-3"
    )
