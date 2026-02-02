"""
Página: Dashboard de Atividades
Utiliza dados do Supabase para exibir atividades de funcionários
"""

import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px

from config import CONTENT_STYLE, CARD_STYLE, COLOR_TEXT_TITLE, COLOR_GRAPH_MAIN, COLOR_SEQUENCE
from supabase_service import (
    get_time_records, 
    calculate_kpis, 
    get_distribuicao_por_funcao,
    get_distribuicao_por_funcionario
)
from components.cards import criar_kpi_card

# Registrar a página
dash.register_page(__name__, path='/atividades', name='Dashboard de Atividades')


# =====================================================================
# LAYOUT DA PÁGINA
# =====================================================================

layout = html.Div(
    [
        dbc.Row([
            dbc.Col(html.H2("Dashboard de Atividades", style={"color": COLOR_TEXT_TITLE, "fontWeight": "600"}), width=12)
        ], className="mb-4"),

        # KPIs - 4 Cards Horizontais
        dbc.Row([
            dbc.Col(dbc.Card([
                html.H6("Total de Registros", className="text-muted", style={"marginBottom": "8px"}),
                html.H3(id="kpi-total-registros", style={"color": COLOR_TEXT_TITLE, "fontWeight": "bold", "marginBottom": "0"})
            ], style=CARD_STYLE), width=12, md=3, className="mb-3"),
            
            dbc.Col(dbc.Card([
                html.H6("Total de Horas", className="text-muted", style={"marginBottom": "8px"}),
                html.H3(id="kpi-total-horas", style={"color": COLOR_TEXT_TITLE, "fontWeight": "bold", "marginBottom": "0"})
            ], style=CARD_STYLE), width=12, md=3, className="mb-3"),
            
            dbc.Col(dbc.Card([
                html.H6("Quantidade de Funcionários", className="text-muted", style={"marginBottom": "8px"}),
                html.H3(id="kpi-qtd-funcionarios", style={"color": COLOR_TEXT_TITLE, "fontWeight": "bold", "marginBottom": "0"})
            ], style=CARD_STYLE), width=12, md=3, className="mb-3"),
            
            dbc.Col(dbc.Card([
                html.H6("Quantidade de Funções", className="text-muted", style={"marginBottom": "8px"}),
                html.H3(id="kpi-qtd-funcoes", style={"color": COLOR_TEXT_TITLE, "fontWeight": "bold", "marginBottom": "0"})
            ], style=CARD_STYLE), width=12, md=3, className="mb-3"),
        ]),

        # Gráficos - 2 Pizzas
        dbc.Row([
            dbc.Col(html.Div([
                    html.H5("Distribuição por Função (%)", className="mb-3", style={"color": COLOR_TEXT_TITLE}),
                    dcc.Graph(id="grafico-funcao", style={"height": "400px"}, config={"displayModeBar": False})
                ], style=CARD_STYLE), width=12, lg=6, className="mb-3"),
            
            dbc.Col(html.Div([
                    html.H5("Distribuição por Funcionário (%)", className="mb-3", style={"color": COLOR_TEXT_TITLE}),
                    dcc.Graph(id="grafico-funcionario", style={"height": "400px"}, config={"displayModeBar": False})
                ], style=CARD_STYLE), width=12, lg=6, className="mb-3")
        ]),
    ],
    style=CONTENT_STYLE
)


# =====================================================================
# CALLBACKS
# =====================================================================

@callback(
    [Output("kpi-total-registros", "children"),
     Output("kpi-total-horas", "children"),
     Output("kpi-qtd-funcionarios", "children"),
     Output("kpi-qtd-funcoes", "children"),
     Output("grafico-funcao", "figure"),
     Output("grafico-funcionario", "figure")],
    [Input("filtro-funcionarios-atividades", "value"),
     Input("filtro-funcoes-atividades", "value"),
     Input("filtro-periodo-atividades", "start_date"),
     Input("filtro-periodo-atividades", "end_date")]
)
def update_dashboard_atividades(filtro_funcionarios, filtro_funcoes, data_inicio, data_fim):
    """Atualiza todos os KPIs e gráficos baseado nos filtros"""
    
    # Buscar dados do Supabase com filtros aplicados
    records = get_time_records(
        filtro_funcionarios=filtro_funcionarios,
        filtro_funcoes=filtro_funcoes,
        data_inicio=data_inicio,
        data_fim=data_fim
    )
    
    # Calcular KPIs
    kpis = calculate_kpis(records)
    
    # Formatar valores dos KPIs
    total_registros = kpis['total_registros']
    total_horas = f"{kpis['total_horas']:.2f}h"
    qtd_funcionarios = kpis['qtd_funcionarios']
    qtd_funcoes = kpis['qtd_funcoes']
    
    # Gráfico de Pizza - Distribuição por Função
    df_funcao = get_distribuicao_por_funcao(records)
    
    if not df_funcao.empty:
        fig_funcao = px.pie(
            df_funcao, 
            values="total_horas", 
            names="function_name",
            hole=0.6, 
            template="plotly_white",
            color_discrete_sequence=COLOR_SEQUENCE
        )
        fig_funcao.update_traces(textposition='outside', textinfo='percent+label')
        fig_funcao.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=True,
            font={"color": COLOR_TEXT_TITLE},
            legend=dict(orientation="v", yanchor="middle", y=0.5)
        )
    else:
        # Gráfico vazio se não houver dados
        fig_funcao = px.pie(
            values=[1], 
            names=["Sem dados"],
            hole=0.6,
            template="plotly_white"
        )
        fig_funcao.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=False,
            font={"color": COLOR_TEXT_TITLE}
        )
    
    # Gráfico de Pizza - Distribuição por Funcionário
    df_funcionario = get_distribuicao_por_funcionario(records)
    
    if not df_funcionario.empty:
        fig_funcionario = px.pie(
            df_funcionario, 
            values="total_horas", 
            names="employee_name",
            hole=0.6, 
            template="plotly_white",
            color_discrete_sequence=COLOR_SEQUENCE
        )
        fig_funcionario.update_traces(textposition='outside', textinfo='percent+label')
        fig_funcionario.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=True,
            font={"color": COLOR_TEXT_TITLE},
            legend=dict(orientation="v", yanchor="middle", y=0.5)
        )
    else:
        # Gráfico vazio se não houver dados
        fig_funcionario = px.pie(
            values=[1], 
            names=["Sem dados"],
            hole=0.6,
            template="plotly_white"
        )
        fig_funcionario.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=False,
            font={"color": COLOR_TEXT_TITLE}
        )
    
    return (total_registros, total_horas, qtd_funcionarios, qtd_funcoes, 
            fig_funcao, fig_funcionario)
