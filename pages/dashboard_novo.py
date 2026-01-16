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
            criar_kpi_card("Total Consertos", "kpi-total-interno", 4, include_mom=True),
            dbc.Col(dbc.Card([
                html.Div([
                    html.Div(id="kpi-media-interno-mom", style={"marginBottom": "4px"}),
                    html.Div(id="kpi-media-interno-yoy")
                ], style={
                    "position": "absolute",
                    "top": "12px",
                    "right": "16px",
                    "fontSize": "0.75rem",
                    "textAlign": "right",
                    "lineHeight": "1.3"
                }),
                html.H6("Tempo Médio (Dias)", className="text-muted", style={"marginBottom": "8px"}),
                html.H3(id="kpi-media-interno", style={"color": COLOR_TEXT_TITLE, "fontWeight": "bold", "marginBottom": "0"})
            ], style={**CARD_STYLE, "position": "relative"}), width=12, md=4, className="mb-3"),
            criar_kpi_card("Taxa Reincidência", "kpi-reincidencia-interno", 4, include_mom=True),
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
     Output("kpi-total-interno-mom", "children"),
     Output("kpi-total-interno-yoy", "children"),
     Output("kpi-media-interno", "children"),
     Output("kpi-media-interno-mom", "children"),
     Output("kpi-media-interno-yoy", "children"),
     Output("kpi-reincidencia-interno", "children"),
     Output("kpi-reincidencia-interno-mom", "children"),
     Output("kpi-reincidencia-interno-yoy", "children"),
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
    media_diaria_valor = dff['Dias'].mean() if not dff.empty and "Dias" in dff.columns else 0
    
    # Calcular Reincidência
    reincidencia_txt = "0%"
    perc_r = 0
    if not dff.empty and "Reincidencia" in dff.columns:
        perc_r = (dff[dff["Reincidencia"] == "Sim"].shape[0] / total) * 100 if total > 0 else 0
        reincidencia_txt = f"{perc_r:.1f}%"
    
    # ======== CALCULAR MÊS ANTERIOR (MoM) ========
    # Só calcular se um único mês está selecionado
    mom_total = None
    mom_media = None
    mom_reincidencia = None
    
    if filtro_mes and len(filtro_mes) == 1:
        mes_atual = filtro_mes[0]
        ano_atual = filtro_ano if filtro_ano != "all" else None
        
        # Calcular mês anterior
        mes_anterior = mes_atual - 1 if mes_atual > 1 else 12
        ano_anterior = ano_atual if mes_atual > 1 else (ano_atual - 1 if ano_atual else None)
        
        # Filtrar dados para mês anterior (aplicando mesmos filtros exceto ano e mês)
        dff_prev = df[df["Tipo"].str.capitalize() == "Interno"].copy()
        if busca_modelo:
            dff_prev = dff_prev[dff_prev["Descrição"].str.contains(busca_modelo, case=False, na=False)]
        if filtro_garantia != "all":
            dff_prev = dff_prev[dff_prev["Garantia"] == filtro_garantia]
        if filtro_funcionario and len(filtro_funcionario) > 0:
            dff_prev = dff_prev[dff_prev["Nome"].isin(filtro_funcionario)]
        if filtro_categoria and len(filtro_categoria) > 0:
            dff_prev = dff_prev[dff_prev["Categoria"].isin(filtro_categoria)]
        
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
        dff_yoy = df[df["Tipo"].str.capitalize() == "Interno"].copy()
        if busca_modelo:
            dff_yoy = dff_yoy[dff_yoy["Descrição"].str.contains(busca_modelo, case=False, na=False)]
        if filtro_garantia != "all":
            dff_yoy = dff_yoy[dff_yoy["Garantia"] == filtro_garantia]
        if filtro_funcionario and len(filtro_funcionario) > 0:
            dff_yoy = dff_yoy[dff_yoy["Nome"].isin(filtro_funcionario)]
        if filtro_categoria and len(filtro_categoria) > 0:
            dff_yoy = dff_yoy[dff_yoy["Categoria"].isin(filtro_categoria)]
        
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
            
            # Criar indicadores YoY usando mesma função
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

    return (total, mom_total or "", yoy_total or "", 
            media_diaria, mom_media or "", yoy_media or "", 
            reincidencia_txt, mom_reincidencia or "", yoy_reincidencia or "", 
            fig_evolucao, fig_funcionarios, fig_cat, fig_modelos)
