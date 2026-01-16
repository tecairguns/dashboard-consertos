"""
Página: Dashboard de Performance de Consertos
"""

import dash
from dash import html, dcc, Input, Output, callback, no_update
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

from config import CONTENT_STYLE, CARD_STYLE, COLOR_TEXT_TITLE, COLOR_GRAPH_MAIN, COLOR_SEQUENCE
from data import df
from components.cards import criar_kpi_card

# Registrar a página
dash.register_page(__name__, path='/', name='Performance de Consertos')


# =====================================================================
# LAYOUT DA PÁGINA
# =====================================================================

layout = html.Div(
    [
        dbc.Row([
            dbc.Col(html.H2("Performance de Consertos", style={"color": COLOR_TEXT_TITLE, "fontWeight": "600"}), width=12)
        ], className="mb-4"),

        # KPIs
        dbc.Row([
            criar_kpi_card("Total Consertos", "kpi-total", 3, include_mom=True),
            dbc.Col(dbc.Card([
                html.Div([
                    html.Div(id="kpi-media-mom", style={"marginBottom": "4px"}),
                    html.Div(id="kpi-media-yoy")
                ], style={
                    "position": "absolute",
                    "top": "12px",
                    "right": "16px",
                    "fontSize": "0.75rem",
                    "textAlign": "right",
                    "lineHeight": "1.3"
                }),
                html.H6("Tempo Médio (Dias)", className="text-muted", style={"marginBottom": "8px"}),
                html.H3(id="kpi-media", style={"color": COLOR_TEXT_TITLE, "fontWeight": "bold", "marginBottom": "0"})
            ], style={**CARD_STYLE, "position": "relative"}), width=12, md=3, className="mb-3"),
            dbc.Col(dbc.Card([
                html.H6("Modelo Crítico", className="text-muted"),
                html.H4(id="kpi-modelo", style={"color": COLOR_TEXT_TITLE, "fontWeight": "bold", "fontSize": "1.2rem"})
            ], style=CARD_STYLE), width=12, md=3, className="mb-3"),
            criar_kpi_card("Taxa Reincidência", "kpi-reincidencia", 3, include_mom=True),
        ]),

        # Linha 1: Gráfico Principal
        dbc.Row([
            dbc.Col(html.Div([
                    html.H5("Evolução de Consertos", className="mb-3", style={"color": COLOR_TEXT_TITLE}),
                    dcc.Graph(id="grafico-principal", style={"height": "350px"}, config={"displayModeBar": False})
                ], style=CARD_STYLE), width=12, className="mb-4")
        ]),

        # Linha 2: GRÁFICO DE MODELOS (SOLUÇÃO SCROLL)
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H5("Ranking de Incidência por Modelo (Top 50)", className="mb-3", style={"color": COLOR_TEXT_TITLE}),
                    html.Small("Role para ver mais | Clique para filtrar", className="text-muted mb-2 d-block"),
                    
                    # DIV CONTAINER PARA O SCROLL
                    html.Div(
                        dcc.Graph(
                            id="grafico-modelos",
                            config={"displayModeBar": False},
                            style={"margin": "0"}
                        ),
                        style={
                            "height": "500px",
                            "overflowY": "scroll",
                            "overflowX": "hidden",
                            "display": "block",
                            "border": "1px solid #f0f0f0",
                            "borderRadius": "4px"
                        }
                    )
                ], style=CARD_STYLE),
                width=12, className="mb-4"
            )
        ]),

        # Linha 3: Secundários
        dbc.Row([
            dbc.Col(html.Div([
                    html.H5("Top Categorias", className="mb-3", style={"color": COLOR_TEXT_TITLE}),
                    dcc.Graph(id="grafico-categorias", style={"height": "350px"}, config={"displayModeBar": False})
                ], style=CARD_STYLE), width=12, lg=6, className="mb-3"),
            
            dbc.Col(html.Div([
                    html.H5("Distribuição por Tipo", className="mb-3", style={"color": COLOR_TEXT_TITLE}),
                    dcc.Graph(id="grafico-tipo", style={"height": "350px"}, config={"displayModeBar": False})
                ], style=CARD_STYLE), width=12, lg=6, className="mb-3")
        ]),

        # Linha 4: Tabela
        dbc.Row([
            dbc.Col(html.Div([
                    html.H5("Tabela de Defeitos", className="mb-3", style={"color": COLOR_TEXT_TITLE}),
                    html.Div(id="tabela-defeitos-container", style={"maxHeight": "400px", "overflowY": "auto"})
                ], style=CARD_STYLE), width=12, className="mb-4")
        ])
    ],
    style=CONTENT_STYLE
)


# =====================================================================
# CALLBACKS
# =====================================================================

@callback(
    Output("filtro-busca", "value"),
    Input("grafico-modelos", "clickData"),
    prevent_initial_call=True
)
def selecionar_modelo_grafico(clickData):
    """Atualiza o filtro de busca quando clicar no gráfico de modelos"""
    if clickData:
        return clickData['points'][0]['y']
    return no_update


@callback(
    [Output("kpi-total", "children"),
     Output("kpi-total-mom", "children"),
     Output("kpi-total-yoy", "children"),
     Output("kpi-media", "children"),
     Output("kpi-media-mom", "children"),
     Output("kpi-media-yoy", "children"),
     Output("kpi-modelo", "children"),
     Output("kpi-reincidencia", "children"),
     Output("kpi-reincidencia-mom", "children"),
     Output("kpi-reincidencia-yoy", "children"),
     Output("grafico-principal", "figure"),
     Output("grafico-modelos", "figure"),
     Output("grafico-categorias", "figure"),
     Output("grafico-tipo", "figure"),
     Output("tabela-defeitos-container", "children")],
    [Input("filtro-busca", "value"),
     Input("filtro-ano", "value"),
     Input("filtro-mes", "value"),
     Input("filtro-categoria", "value"),
     Input("filtro-garantia", "value"),
     Input("filtro-tipo", "value")]
)
def update_dashboard(busca_modelo, filtro_ano, filtro_mes, filtro_categoria, filtro_garantia, filtro_tipo):
    """Atualiza todos os gráficos e KPIs baseado nos filtros"""
    
    dff = df.copy()
    
    # Aplicar Filtros
    if busca_modelo:
        dff = dff[dff["Descrição"].str.contains(busca_modelo, case=False, na=False)]
    if filtro_ano != "all":
        dff = dff[dff["Ano"] == filtro_ano]
    if filtro_mes and len(filtro_mes) > 0:
        dff = dff[dff["Mes"].isin(filtro_mes)]
    if filtro_categoria and len(filtro_categoria) > 0:
        dff = dff[dff["Categoria"].isin(filtro_categoria)]
    if filtro_garantia != "all":
        dff = dff[dff["Garantia"] == filtro_garantia]
    if filtro_tipo != "all":
        dff = dff[dff["Tipo"] == filtro_tipo]

    # Calcular KPIs
    total = len(dff)
    media_diaria = f"{dff['Dias'].mean():.1f} dias" if not dff.empty and "Dias" in dff.columns else "0 dias"
    media_diaria_valor = dff['Dias'].mean() if not dff.empty and "Dias" in dff.columns else 0
    
    top_modelo = "-"
    if not dff.empty:
        top_modelo = dff["Descrição"].value_counts().idxmax()
        if len(top_modelo) > 25:
            top_modelo = top_modelo[:25] + "..."
        
    reincidencia_txt = "0%"
    perc_r = 0
    if not dff.empty and "Reincidencia" in dff.columns:
        perc_r = (dff[dff["Reincidencia"] == "Sim"].shape[0] / total) * 100
        reincidencia_txt = f"{perc_r:.1f}%"
    
    # ======== CALCULAR MÊS ANTERIOR (MoM) ========
    mom_total = None
    mom_media = None
    mom_reincidencia = None
    
    if filtro_mes and len(filtro_mes) == 1:
        mes_atual = filtro_mes[0]
        ano_atual = filtro_ano if filtro_ano != "all" else None
        
        # Calcular mês anterior
        mes_anterior = mes_atual - 1 if mes_atual > 1 else 12
        ano_anterior = ano_atual if mes_atual > 1 else (ano_atual - 1 if ano_atual else None)
        
        # Filtrar dados para mês anterior
        dff_prev = df.copy()
        if busca_modelo:
            dff_prev = dff_prev[dff_prev["Descrição"].str.contains(busca_modelo, case=False, na=False)]
        if filtro_categoria and len(filtro_categoria) > 0:
            dff_prev = dff_prev[dff_prev["Categoria"].isin(filtro_categoria)]
        if filtro_garantia != "all":
            dff_prev = dff_prev[dff_prev["Garantia"] == filtro_garantia]
        if filtro_tipo != "all":
            dff_prev = dff_prev[dff_prev["Tipo"] == filtro_tipo]
        
        # Aplicar filtro de ano e mês anterior
        dff_prev = dff_prev[dff_prev["Mes"] == mes_anterior]
        if ano_anterior:
            dff_prev = dff_prev[dff_prev["Ano"] == ano_anterior]
        
        # Calcular métricas do mês anterior
        if not dff_prev.empty:
            total_prev = len(dff_prev)
            media_prev = dff_prev['Dias'].mean() if "Dias" in dff_prev.columns else 0
            
            perc_r_prev = 0
            if "Reincidencia" in dff_prev.columns:
                perc_r_prev = (dff_prev[dff_prev["Reincidencia"] == "Sim"].shape[0] / total_prev) * 100 if total_prev > 0 else 0
            
            # Criar indicadores MoM
            def criar_mom_indicator(valor_atual, valor_prev, eh_percentual=False, inverter=False):
                """Cria indicador MoM com ícone e cor"""
                diff = valor_atual - valor_prev
                is_increase = diff > 0
                
                # Para todas as métricas, diminuição é bom (verde)
                if inverter:
                    is_good = not is_increase
                else:
                    is_good = is_increase
                
                icon = "▲" if is_increase else "▼"
                color = "#28a745" if is_good else "#dc3545"
                
                if eh_percentual:
                    texto = f"{valor_prev:.1f}%"
                elif isinstance(valor_prev, float):
                    texto = f"{valor_prev:.1f}"
                else:
                    texto = str(int(valor_prev))
                
                return html.Div([
                    html.Div(icon, style={"color": color, "fontSize": "0.9rem", "fontWeight": "bold"}),
                    html.Div(f"Mês ant.: {texto}", style={"color": "#6c757d", "fontSize": "0.7rem"})
                ])
            
            mom_total = criar_mom_indicator(total, total_prev, inverter=True)
            mom_media = criar_mom_indicator(media_diaria_valor, media_prev, inverter=True)
            mom_reincidencia = criar_mom_indicator(perc_r, perc_r_prev, eh_percentual=True, inverter=True)
    
    # ======== CALCULAR ANO ANTERIOR (YoY) ========
    yoy_total = None
    yoy_media = None
    yoy_reincidencia = None
    
    if filtro_ano and filtro_ano != "all":
        ano_atual = filtro_ano
        ano_anterior = ano_atual - 1
        
        # Filtrar dados para ano anterior
        dff_yoy = df.copy()
        if busca_modelo:
            dff_yoy = dff_yoy[dff_yoy["Descrição"].str.contains(busca_modelo, case=False, na=False)]
        if filtro_categoria and len(filtro_categoria) > 0:
            dff_yoy = dff_yoy[dff_yoy["Categoria"].isin(filtro_categoria)]
        if filtro_garantia != "all":
            dff_yoy = dff_yoy[dff_yoy["Garantia"] == filtro_garantia]
        if filtro_tipo != "all":
            dff_yoy = dff_yoy[dff_yoy["Tipo"] == filtro_tipo]
        
        # Aplicar filtro de ano anterior
        dff_yoy = dff_yoy[dff_yoy["Ano"] == ano_anterior]
        
        # Se tiver um mês específico selecionado, filtrar pelo mesmo mês
        if filtro_mes and len(filtro_mes) == 1:
            mes_atual = filtro_mes[0]
            dff_yoy = dff_yoy[dff_yoy["Mes"] == mes_atual]
        # Se não tiver mês selecionado ou múltiplos meses, pega o ano inteiro (sem filtro de mês)
        
        # Calcular métricas do ano anterior
        if not dff_yoy.empty:
            total_yoy = len(dff_yoy)
            media_yoy = dff_yoy['Dias'].mean() if "Dias" in dff_yoy.columns else 0
            
            perc_r_yoy = 0
            if "Reincidencia" in dff_yoy.columns:
                perc_r_yoy = (dff_yoy[dff_yoy["Reincidencia"] == "Sim"].shape[0] / total_yoy) * 100 if total_yoy > 0 else 0
            
            # Criar indicadores YoY
            def criar_yoy_indicator(valor_atual, valor_prev, eh_percentual=False, inverter=False):
                """Cria indicador YoY com ícone e cor"""
                diff = valor_atual - valor_prev
                is_increase = diff > 0
                
                # Para todas as métricas, diminuição é bom (verde)
                if inverter:
                    is_good = not is_increase
                else:
                    is_good = is_increase
                
                icon = "▲" if is_increase else "▼"
                color = "#28a745" if is_good else "#dc3545"
                
                if eh_percentual:
                    texto = f"{valor_prev:.1f}%"
                elif isinstance(valor_prev, float):
                    texto = f"{valor_prev:.1f}"
                else:
                    texto = str(int(valor_prev))
                
                return html.Div([
                    html.Div(icon, style={"color": color, "fontSize": "0.9rem", "fontWeight": "bold"}),
                    html.Div(f"Ano ant.: {texto}", style={"color": "#6c757d", "fontSize": "0.7rem"})
                ])
            
            yoy_total = criar_yoy_indicator(total, total_yoy, inverter=True)
            yoy_media = criar_yoy_indicator(media_diaria_valor, media_yoy, inverter=True)
            yoy_reincidencia = criar_yoy_indicator(perc_r, perc_r_yoy, eh_percentual=True, inverter=True)

    # Gráfico Principal - Evolução
    df_chart = dff.groupby(["Ano", "Mes", "Mes_nome"]).size().reset_index(name="Quantidade").sort_values(["Ano", "Mes"])
    df_chart["Ano"] = df_chart["Ano"].astype(str)
    fig_main = px.bar(
        df_chart, x="Mes_nome", y="Quantidade", color="Ano",
        barmode="group", text_auto=True, template="plotly_white",
        color_discrete_sequence=COLOR_SEQUENCE
    )
    fig_main.update_layout(
        xaxis={"title": ""}, yaxis={"title": "Qtd"},
        margin=dict(l=20, r=20, t=30, b=20),
        font={"color": COLOR_TEXT_TITLE}
    )

    # Gráfico de Modelos (com scroll)
    df_modelos = dff["Descrição"].value_counts().head(50).reset_index()
    df_modelos.columns = ["Modelo", "Quantidade"]
    df_modelos = df_modelos.sort_values("Quantidade", ascending=True)

    altura_linha = 35
    altura_total = max(450, len(df_modelos) * altura_linha)

    fig_modelos = px.bar(
        df_modelos, x="Quantidade", y="Modelo", orientation='h',
        text="Quantidade", template="plotly_white"
    )
    fig_modelos.update_traces(marker_color=COLOR_GRAPH_MAIN, textposition="outside")
    fig_modelos.update_layout(
        height=altura_total,
        autosize=True,
        yaxis={"title": ""}, xaxis={"title": ""},
        margin=dict(l=10, r=20, t=20, b=10),
        font={"color": COLOR_TEXT_TITLE},
        bargap=0.2
    )

    # Gráfico de Categorias
    df_cat = dff["Categoria"].value_counts().head(10).reset_index()
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

    # Gráfico de Tipo (Pizza)
    df_tipo_chart = dff["Tipo"].value_counts().reset_index()
    df_tipo_chart.columns = ["Tipo", "Quantidade"]
    fig_tipo = px.pie(
        df_tipo_chart, values="Quantidade", names="Tipo",
        hole=0.6, template="plotly_white",
        color_discrete_sequence=COLOR_SEQUENCE
    )
    fig_tipo.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=True,
        font={"color": COLOR_TEXT_TITLE}
    )

    # Tabela de Defeitos
    if not dff.empty:
        df_defeitos = dff["Defeito"].value_counts().reset_index()
        df_defeitos.columns = ["Defeito", "Quantidade"]
        table = dbc.Table.from_dataframe(
            df_defeitos, striped=True, bordered=True, hover=True,
            style={"color": "#333"}
        )
    else:
        table = html.P("Sem dados.", className="text-muted")

    return (total, mom_total or "", yoy_total or "",
            media_diaria, mom_media or "", yoy_media or "",
            top_modelo,
            reincidencia_txt, mom_reincidencia or "", yoy_reincidencia or "",
            fig_main, fig_modelos, fig_cat, fig_tipo, table)
