"""
Página: Dashboard de Consertos Internos
Análise de Performance dos Funcionários Internos
"""

import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

from config import CONTENT_STYLE, CARD_STYLE, COLOR_TEXT_TITLE, COLOR_GRAPH_MAIN, COLOR_SEQUENCE
from data import df
from components.cards import criar_kpi_card

# Registrar a página
dash.register_page(__name__, path='/novo', name='Consertos Internos')


# =====================================================================
# LAYOUT DA PÁGINA
# =====================================================================

layout = html.Div(
    [
        dbc.Row([
            dbc.Col(html.H2("Performance - Consertos Internos", style={"color": COLOR_TEXT_TITLE, "fontWeight": "600"}), width=12)
        ], className="mb-4"),

        # KPIs
        dbc.Row([
            criar_kpi_card("Total Consertos", "kpi-total-interno", 4),
            dbc.Col(dbc.Card([
                html.H6("Tempo Médio (Dias)", className="text-muted"),
                html.H3(id="kpi-media-interno", style={"color": COLOR_TEXT_TITLE, "fontWeight": "bold"})
            ], style=CARD_STYLE), width=12, md=4, className="mb-3"),
            criar_kpi_card("Taxa Reincidência", "kpi-reincidencia-interno", 4),
        ]),

        # Gráfico de Evolução Mensal
        dbc.Row([
            dbc.Col(html.Div([
                    html.H5("Evolução Mensal de Consertos", className="mb-3", style={"color": COLOR_TEXT_TITLE}),
                    dcc.Graph(id="grafico-evolucao-interno", style={"height": "350px"}, config={"displayModeBar": False})
                ], style=CARD_STYLE), width=12, className="mb-4")
        ]),

        # Linha: Gráfico de Funcionários (Rosca) e Categorias
        dbc.Row([
            dbc.Col(html.Div([
                    html.H5("Distribuição por Funcionário", className="mb-3", style={"color": COLOR_TEXT_TITLE}),
                    dcc.Graph(id="grafico-funcionarios", style={"height": "400px"}, config={"displayModeBar": False})
                ], style=CARD_STYLE), width=12, lg=6, className="mb-3"),
            
            dbc.Col(html.Div([
                    html.H5("Top Categorias", className="mb-3", style={"color": COLOR_TEXT_TITLE}),
                    dcc.Graph(id="grafico-categorias-interno", style={"height": "400px"}, config={"displayModeBar": False})
                ], style=CARD_STYLE), width=12, lg=6, className="mb-3")
        ]),

        # Gráfico de Modelos
        dbc.Row([
            dbc.Col(html.Div([
                    html.H5("Top Modelos Reparados", className="mb-3", style={"color": COLOR_TEXT_TITLE}),
                    dcc.Graph(id="grafico-modelos-interno", style={"height": "450px"}, config={"displayModeBar": False})
                ], style=CARD_STYLE), width=12, className="mb-4")
        ])
    ],
    style=CONTENT_STYLE
)


# =====================================================================
# CALLBACKS
# =====================================================================

@callback(
    [Output("kpi-total-interno", "children"),
     Output("kpi-media-interno", "children"),
     Output("kpi-reincidencia-interno", "children"),
     Output("grafico-evolucao-interno", "figure"),
     Output("grafico-funcionarios", "figure"),
     Output("grafico-categorias-interno", "figure"),
     Output("grafico-modelos-interno", "figure")],
    [Input("filtro-busca-interno", "value"),
     Input("filtro-ano-interno", "value"),
     Input("filtro-mes-interno", "value"),
     Input("filtro-garantia-interno", "value"),
     Input("filtro-funcionario", "value"),
     Input("filtro-categoria-interno", "value")]
)
def update_dashboard_interno(busca_modelo, filtro_ano, filtro_mes, filtro_garantia, filtro_funcionario, filtro_categoria):
    """Atualiza todos os gráficos e KPIs do dashboard interno"""
    
    # IMPORTANTE: Filtrar apenas consertos INTERNOS
    dff = df[df["Tipo"].str.capitalize() == "Interno"].copy()
    
    # Aplicar Filtros
    if busca_modelo:
        dff = dff[dff["Descrição"].str.contains(busca_modelo, case=False, na=False)]
    if filtro_ano != "all":
        dff = dff[dff["Ano"] == filtro_ano]
    if filtro_mes and len(filtro_mes) > 0:
        dff = dff[dff["Mes"].isin(filtro_mes)]
    if filtro_garantia != "all":
        dff = dff[dff["Garantia"] == filtro_garantia]
    if filtro_funcionario and len(filtro_funcionario) > 0:
        dff = dff[dff["Nome"].isin(filtro_funcionario)]
    if filtro_categoria and len(filtro_categoria) > 0:
        dff = dff[dff["Categoria"].isin(filtro_categoria)]

    # Calcular KPIs
    total = len(dff)
    media_diaria = f"{dff['Dias'].mean():.1f} dias" if not dff.empty and "Dias" in dff.columns else "0 dias"
    
    # Calcular Reincidência
    reincidencia_txt = "0%"
    if not dff.empty and "Reincidencia" in dff.columns:
        perc_r = (dff[dff["Reincidencia"] == "Sim"].shape[0] / total) * 100 if total > 0 else 0
        reincidencia_txt = f"{perc_r:.1f}%"

    # Gráfico 1: Evolução Mensal (Barras)
    if not dff.empty:
        df_chart = dff.groupby(["Ano", "Mes", "Mes_nome"]).size().reset_index(name="Quantidade").sort_values(["Ano", "Mes"])
        df_chart["Ano"] = df_chart["Ano"].astype(str)
        fig_evolucao = px.bar(
            df_chart, x="Mes_nome", y="Quantidade", color="Ano",
            barmode="group", text_auto=True, template="plotly_white",
            color_discrete_sequence=COLOR_SEQUENCE
        )
        fig_evolucao.update_layout(
            xaxis={"title": ""}, yaxis={"title": "Qtd"},
            margin=dict(l=20, r=20, t=30, b=20),
            font={"color": COLOR_TEXT_TITLE}
        )
    else:
        fig_evolucao = px.bar(template="plotly_white")
        fig_evolucao.update_layout(annotations=[dict(text="Sem dados", showarrow=False, font_size=16)])

    # Gráfico 2: Distribuição por Funcionário (Rosca com %)
    if not dff.empty:
        df_func = dff["Nome"].value_counts().reset_index()
        df_func.columns = ["Funcionário", "Quantidade"]
        fig_funcionarios = px.pie(
            df_func, values="Quantidade", names="Funcionário",
            hole=0.6, template="plotly_white",
            color_discrete_sequence=COLOR_SEQUENCE
        )
        fig_funcionarios.update_traces(textposition='outside', textinfo='percent')
        fig_funcionarios.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=True,
            font={"color": COLOR_TEXT_TITLE}
        )
    else:
        fig_funcionarios = go.Figure()
        fig_funcionarios.update_layout(annotations=[dict(text="Sem dados", showarrow=False, font_size=16)])

    # Gráfico 3: Top Categorias (Barras Horizontais)
    if not dff.empty:
        df_cat = dff["Categoria"].value_counts().head(15).reset_index()
        df_cat.columns = ["Categoria", "Quantidade"]
        fig_cat = px.bar(
            df_cat.sort_values("Quantidade", ascending=True),
            x="Quantidade", y="Categoria", orientation="h",
            text="Quantidade", template="plotly_white"
        )
        fig_cat.update_traces(marker_color=COLOR_GRAPH_MAIN, textposition="outside")
        fig_cat.update_layout(
            yaxis={"title": ""}, xaxis={"title": ""},
            margin=dict(l=20, r=20, t=20, b=20),
            font={"color": COLOR_TEXT_TITLE}
        )
    else:
        fig_cat = px.bar(template="plotly_white")
        fig_cat.update_layout(annotations=[dict(text="Sem dados", showarrow=False, font_size=16)])

    # Gráfico 4: Top Modelos (Barras Horizontais)
    if not dff.empty:
        df_modelos = dff["Descrição"].value_counts().head(20).reset_index()
        df_modelos.columns = ["Modelo", "Quantidade"]
        fig_modelos = px.bar(
            df_modelos.sort_values("Quantidade", ascending=True),
            x="Quantidade", y="Modelo", orientation="h",
            text="Quantidade", template="plotly_white"
        )
        fig_modelos.update_traces(marker_color=COLOR_GRAPH_MAIN, textposition="outside")
        fig_modelos.update_layout(
            yaxis={"title": ""}, xaxis={"title": ""},
            margin=dict(l=20, r=20, t=20, b=20),
            font={"color": COLOR_TEXT_TITLE}
        )
    else:
        fig_modelos = px.bar(template="plotly_white")
        fig_modelos.update_layout(annotations=[dict(text="Sem dados", showarrow=False, font_size=16)])

    return total, media_diaria, reincidencia_txt, fig_evolucao, fig_funcionarios, fig_cat, fig_modelos
