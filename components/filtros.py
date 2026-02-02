"""
Componentes de filtros reutilizáveis para diferentes páginas
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from data import opcoes_filtros


def criar_filtros_consertos():
    """
    Cria os filtros específicos para o dashboard de consertos
    
    Returns:
        html.Div: Container com filtros de consertos
    """
    return html.Div([
        html.Label("Filtros", className="fw-bold text-white mb-3"),
        html.Br(),
        html.Label("Buscar Modelo", className="fw-bold text-white mt-2"),
        dcc.Input(
            id="filtro-busca",
            type="text",
            placeholder="Digite ou clique no gráfico...",
            debounce=True,
            style={"width": "100%", "marginBottom": "15px", "borderRadius": "5px", "border": "none", "padding": "5px"}
        ),
        
        html.Label("Ano", className="fw-bold text-white mt-2"),
        dcc.Dropdown(
            id="filtro-ano",
            options=opcoes_filtros["ano"],
            value="all",
            clearable=False,
            style={"color": "#333"}
        ),

        html.Label("Mês(es)", className="fw-bold text-white mt-3"),
        dcc.Dropdown(
            id="filtro-mes",
            options=opcoes_filtros["mes"],
            value=[],
            multi=True,
            placeholder="Selecione meses...",
            style={"color": "#333"}
        ),

        html.Label("Categoria(s)", className="fw-bold text-white mt-3"),
        dcc.Dropdown(
            id="filtro-categoria",
            options=opcoes_filtros["categoria"],
            value=[],
            multi=True,
            placeholder="Selecione categorias...",
            style={"color": "#333"}
        ),

        html.Label("Garantia", className="fw-bold text-white mt-3"),
        dcc.Dropdown(
            id="filtro-garantia",
            options=opcoes_filtros["garantia"],
            value="all",
            clearable=False,
            style={"color": "#333"}
        ),

        html.Label("Tipo", className="fw-bold text-white mt-3"),
        dbc.RadioItems(
            id="filtro-tipo",
            options=opcoes_filtros["tipo"],
            value="all",
            inline=False,
            className="mt-1"
        ),
        

    ])


def criar_filtros_novo_dashboard():
    """
    Cria os filtros específicos para o dashboard de consertos internos
    
    Returns:
        html.Div: Container com filtros do dashboard interno
    """
    return html.Div([
        html.Label("Filtros - Internos", className="fw-bold text-white mb-3"),
        html.Br(),
        
        html.Label("Buscar Modelo", className="fw-bold text-white mt-2"),
        dcc.Input(
            id="filtro-busca-interno",
            type="text",
            placeholder="Digite o modelo...",
            debounce=True,
            style={"width": "100%", "marginBottom": "15px", "borderRadius": "5px", "border": "none", "padding": "5px"}
        ),
        
        html.Label("Ano", className="fw-bold text-white mt-2"),
        dcc.Dropdown(
            id="filtro-ano-interno",
            options=opcoes_filtros["ano"],
            value="all",
            clearable=False,
            style={"color": "#333"}
        ),

        html.Label("Mês(es)", className="fw-bold text-white mt-3"),
        dcc.Dropdown(
            id="filtro-mes-interno",
            options=opcoes_filtros["mes"],
            value=[],
            multi=True,
            placeholder="Selecione meses...",
            style={"color": "#333"}
        ),

        html.Label("Garantia", className="fw-bold text-white mt-3"),
        dcc.Dropdown(
            id="filtro-garantia-interno",
            options=opcoes_filtros["garantia"],
            value="all",
            clearable=False,
            style={"color": "#333"}
        ),
        
        html.Label("Funcionário(s)", className="fw-bold text-white mt-3"),
        dcc.Dropdown(
            id="filtro-funcionario",
            options=opcoes_filtros["funcionario"],
            value=[],
            multi=True,
            placeholder="Selecione funcionários...",
            style={"color": "#333"}
        ),

        html.Label("Categoria(s)", className="fw-bold text-white mt-3"),
        dcc.Dropdown(
            id="filtro-categoria-interno",
            options=opcoes_filtros["categoria"],
            value=[],
            multi=True,
            placeholder="Selecione categorias...",
            style={"color": "#333"}
        ),
    ])


def criar_filtros_atividades():
    """
    Cria os filtros específicos para o dashboard de atividades (Supabase)
    
    Returns:
        html.Div: Container com filtros de atividades
    """
    # Importar aqui para evitar erros se as credenciais ainda não estiverem configuradas
    try:
        from supabase_service import get_employees, get_functions
        
        # Buscar funcionários e funções do Supabase
        employees = get_employees()
        functions = get_functions()
        
        # Preparar opções para os dropdowns
        opcoes_funcionarios = [{"label": emp.get('name', ''), "value": emp.get('name', '')} for emp in employees]
        opcoes_funcoes = [{"label": func.get('name', ''), "value": func.get('name', '')} for func in functions]
    except Exception as e:
        print(f"Erro ao carregar opções de filtros: {e}")
        opcoes_funcionarios = []
        opcoes_funcoes = []
    
    return html.Div([
        html.Label("Filtros - Atividades", className="fw-bold text-white mb-3"),
        html.Br(),
        
        html.Label("Funcionário(s)", className="fw-bold text-white mt-2"),
        dcc.Dropdown(
            id="filtro-funcionarios-atividades",
            options=opcoes_funcionarios,
            value=[],
            multi=True,
            placeholder="Selecione funcionários...",
            style={"color": "#333"}
        ),

        html.Label("Função(ões)", className="fw-bold text-white mt-3"),
        dcc.Dropdown(
            id="filtro-funcoes-atividades",
            options=opcoes_funcoes,
            value=[],
            multi=True,
            placeholder="Selecione funções...",
            style={"color": "#333"}
        ),

        html.Label("Período", className="fw-bold text-white mt-3"),
        dcc.DatePickerRange(
            id="filtro-periodo-atividades",
            start_date_placeholder_text="Data Início",
            end_date_placeholder_text="Data Fim",
            display_format="DD/MM/YYYY",
            style={"width": "100%"}
        ),
    ])

