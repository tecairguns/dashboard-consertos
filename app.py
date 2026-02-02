"""
Dashboard de Consertos - Aplicação Principal
Arquitetura Multi-Página com Navegação
"""

from dash import Dash, html, page_container, dcc, Input, Output, callback
import dash_bootstrap_components as dbc

from components.sidebar import criar_sidebar
from components.filtros import criar_filtros_consertos, criar_filtros_novo_dashboard, criar_filtros_atividades

# =====================================================================
# INICIALIZAÇÃO DA APLICAÇÃO
# =====================================================================

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.SPACELAB],
    use_pages=True,  # Habilita o sistema multi-página
    suppress_callback_exceptions=True
)

server = app.server

# =====================================================================
# LAYOUT PRINCIPAL
# =====================================================================

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),  # Rastreamento de URL para filtros dinâmicos
    criar_sidebar(),
    page_container  # Container que renderiza as páginas registradas
])


# =====================================================================
# CALLBACK GLOBAL PARA ATUALIZAR FILTROS NA SIDEBAR
# =====================================================================

@callback(
    Output("filtros-container", "children"),
    Input("url", "pathname")
)
def atualizar_filtros_sidebar(pathname):
    """Atualiza os filtros na sidebar quando muda de página"""
    if pathname == "/" or pathname is None:
        return criar_filtros_consertos()
    elif pathname == "/novo":
        return criar_filtros_novo_dashboard()
    elif pathname == "/atividades":
        return criar_filtros_atividades()
    return html.Div()


# =====================================================================
# EXECUÇÃO
# =====================================================================

if __name__ == "__main__":
    app.run(debug=True)