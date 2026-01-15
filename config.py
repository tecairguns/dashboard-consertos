"""
Configurações e constantes do Dashboard
"""

# =====================================================================
# DADOS
# =====================================================================

NOME_ARQUIVO = "CONSERTOS 20242025.xlsx - rci3040.xls 1.csv"
NOME_ARQUIVO_EXCEL = "CONSERTOS 20242025.xlsx"

# =====================================================================
# PALETA DE CORES
# =====================================================================

COLOR_ASIDE_BG = "#445569"
COLOR_TEXT_TITLE = "#445569"
COLOR_GRAPH_MAIN = "#E8D166"
COLOR_SEQUENCE = ["#E8D166", "#C9B250", "#F0E290", "#9C8A35", "#E8D166"]

# =====================================================================
# ESTILOS
# =====================================================================

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "2rem 1rem",
    "backgroundColor": COLOR_ASIDE_BG,
    "color": "white",
    "boxShadow": "2px 0 5px rgba(0,0,0,0.1)",
    "overflowY": "auto"
}

CONTENT_STYLE = {
    "marginLeft": "21rem",
    "padding": "2rem 1rem",
    "backgroundColor": "#f4f7f6",
    "minHeight": "100vh"
}

CARD_STYLE = {
    "backgroundColor": "#ffffff",
    "borderRadius": "10px",
    "boxShadow": "0 2px 4px rgba(0,0,0,0.05)",
    "padding": "20px",
    "border": "none"
}

# =====================================================================
# MAPEAMENTO DE MESES
# =====================================================================

MESES_MAP = {
    1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
    7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
}
