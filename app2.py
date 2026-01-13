import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, no_update
import dash_bootstrap_components as dbc

# =====================================================================
# CONFIGURAÇÃO E CARREGAMENTO DE DADOS
# =====================================================================

NOME_ARQUIVO = "CONSERTOS 20242025.xlsx - rci3040.xls 1.csv"

try:
    df = pd.read_csv(NOME_ARQUIVO, on_bad_lines='skip')
except:
    try:
        df = pd.read_excel("CONSERTOS 20242025.xlsx")
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        df = pd.DataFrame()

# Tratamento de Datas
df["Dt-Saida"] = pd.to_datetime(df["Dt-Saida"], format="%d/%m/%Y", errors="coerce")
df = df.dropna(subset=["Dt-Saida"])

# Criando colunas auxiliares
df["Ano"] = df["Dt-Saida"].dt.year
df["Mes"] = df["Dt-Saida"].dt.month
meses_map = {
    1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
    7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
}
df["Mes_nome"] = df["Mes"].map(meses_map)

# Padronização de Strings
cols_str = ["Defeito", "Categoria", "Descrição", "Tipo", "Marca", "Garantia", "Reincidencia"]
for col in cols_str:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip().str.capitalize()

# =====================================================================
# PALETA DE CORES
# =====================================================================

COLOR_ASIDE_BG = "#445569"
COLOR_TEXT_TITLE = "#445569"
COLOR_GRAPH_MAIN = "#E8D166"
COLOR_SEQUENCE = ["#E8D166", "#C9B250", "#F0E290", "#9C8A35", "#E8D166"]

# =====================================================================
# PREPARAÇÃO DAS OPÇÕES DOS FILTROS
# =====================================================================

anos_unicos = sorted(df["Ano"].dropna().unique())
opcoes_ano = [{"label": "Todos", "value": "all"}] + [{"label": str(int(ano)), "value": int(ano)} for ano in anos_unicos]

opcoes_mes = [{"label": nome, "value": num} for num, nome in meses_map.items()]

cats_unicas = sorted(df["Categoria"].dropna().unique())
opcoes_categoria = [{"label": c, "value": c} for c in cats_unicas]

opcoes_garantia = [{"label": "Todas", "value": "all"}] + [{"label": str(g), "value": g} for g in df["Garantia"].unique() if str(g) != 'nan']

opcoes_tipo = [{"label": "Todos", "value": "all"}] + [{"label": str(t), "value": t} for t in df["Tipo"].unique() if str(t) != 'nan']

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

app = Dash(__name__, external_stylesheets=[dbc.themes.SPACELAB])

# =====================================================================
# LAYOUT
# =====================================================================

sidebar = html.Div(
    [
        html.H3("Dashboard", className="display-6", style={"color": "#ffffff", "fontWeight": "bold"}),
        html.Hr(style={"borderColor": "white"}),

        html.Label("Buscar Modelo", className="fw-bold"),
        dcc.Input(
            id="filtro-busca",
            type="text",
            placeholder="Digite ou clique no gráfico...",
            debounce=True, 
            style={"width": "100%", "marginBottom": "15px", "borderRadius": "5px", "border": "none", "padding": "5px"}
        ),
        
        html.Label("Ano", className="fw-bold mt-2"),
        dcc.Dropdown(id="filtro-ano", options=opcoes_ano, value="all", clearable=False, style={"color": "#333"}),

        html.Label("Mês(es)", className="fw-bold mt-3"),
        dcc.Dropdown(id="filtro-mes", options=opcoes_mes, value=[], multi=True, placeholder="Selecione meses...", style={"color": "#333"}),

        html.Label("Categoria(s)", className="fw-bold mt-3"),
        dcc.Dropdown(id="filtro-categoria", options=opcoes_categoria, value=[], multi=True, placeholder="Selecione categorias...", style={"color": "#333"}),

        html.Label("Garantia", className="fw-bold mt-3"),
        dcc.Dropdown(id="filtro-garantia", options=opcoes_garantia, value="all", clearable=False, style={"color": "#333"}),

        html.Label("Tipo", className="fw-bold mt-3"),
        dbc.RadioItems(id="filtro-tipo", options=opcoes_tipo, value="all", inline=False, className="mt-1"),
        
        html.Hr(className="mt-5", style={"borderColor": "white"}),
        html.Small("Dica: Clique nas barras do gráfico de modelos para filtrar.", style={"color": "#ccc"})
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(
    [
        dbc.Row([
            dbc.Col(html.H2("Performance de Consertos", style={"color": COLOR_TEXT_TITLE, "fontWeight": "600"}), width=12)
        ], className="mb-4"),

        # KPIs
        dbc.Row([
            dbc.Col(dbc.Card([
                html.H6("Total Consertos", className="text-muted"),
                html.H3(id="kpi-total", className="fw-bold", style={"color": COLOR_TEXT_TITLE})
            ], style=CARD_STYLE), width=12, md=3, className="mb-3"),
            
            dbc.Col(dbc.Card([
                html.H6("Tempo Médio (Dias)", className="text-muted"),
                html.H3(id="kpi-media", style={"color": COLOR_TEXT_TITLE, "fontWeight": "bold"})
            ], style=CARD_STYLE), width=12, md=3, className="mb-3"),
            
            dbc.Col(dbc.Card([
                html.H6("Modelo Crítico", className="text-muted"),
                html.H4(id="kpi-modelo", style={"color": COLOR_TEXT_TITLE, "fontWeight": "bold", "fontSize": "1.2rem"})
            ], style=CARD_STYLE), width=12, md=3, className="mb-3"),
            
            dbc.Col(dbc.Card([
                html.H6("Taxa Reincidência", className="text-muted"),
                html.H3(id="kpi-reincidencia", style={"color": COLOR_TEXT_TITLE, "fontWeight": "bold"})
            ], style=CARD_STYLE), width=12, md=3, className="mb-3"),
        ]),

        # Linha 1: Gráfico Principal
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H5("Evolução de Consertos", className="mb-3", style={"color": COLOR_TEXT_TITLE}),
                    dcc.Graph(id="grafico-principal", style={"height": "350px"}, config={"displayModeBar": False})
                ], style=CARD_STYLE), 
                width=12, className="mb-4"
            )
        ]),

        # Linha 2: NOVO GRÁFICO - Ranking de Modelos
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H5("Ranking de Incidência por Modelo (Top 20)", className="mb-3", style={"color": COLOR_TEXT_TITLE}),
                    html.Small("Clique em uma barra para filtrar o dashboard por este modelo.", className="text-muted mb-2 d-block"),
                    dcc.Graph(id="grafico-modelos", style={"height": "600px"}, config={"displayModeBar": False})
                ], style=CARD_STYLE),
                width=12, className="mb-4"
            )
        ]),

        # Linha 3: Secundários
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H5("Top Categorias", className="mb-3", style={"color": COLOR_TEXT_TITLE}),
                    dcc.Graph(id="grafico-categorias", style={"height": "350px"}, config={"displayModeBar": False})
                ], style=CARD_STYLE), 
                width=12, lg=6, className="mb-3"
            ),
            
            dbc.Col(
                html.Div([
                    html.H5("Distribuição por Tipo", className="mb-3", style={"color": COLOR_TEXT_TITLE}),
                    dcc.Graph(id="grafico-tipo", style={"height": "350px"}, config={"displayModeBar": False})
                ], style=CARD_STYLE), 
                width=12, lg=6, className="mb-3"
            )
        ]),

        # Linha 4: Tabela
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H5("Tabela de Defeitos", className="mb-3", style={"color": COLOR_TEXT_TITLE}),
                    html.Div(id="tabela-defeitos-container", style={"maxHeight": "400px", "overflowY": "auto"})
                ], style=CARD_STYLE),
                width=12, className="mb-4"
            )
        ])
    ],
    style=CONTENT_STYLE
)

app.layout = html.Div([sidebar, content])

# =====================================================================
# CALLBACKS
# =====================================================================

# Callback de Interatividade: Clique no Gráfico de Modelos -> Filtro de Busca
@app.callback(
    Output("filtro-busca", "value"),
    Input("grafico-modelos", "clickData"),
    prevent_initial_call=True
)
def selecionar_modelo_grafico(clickData):
    if clickData:
        # Pega o rótulo do eixo Y (nome do modelo) onde ocorreu o clique
        modelo_selecionado = clickData['points'][0]['y']
        return modelo_selecionado
    return no_update

# Callback Principal
@app.callback(
    [Output("kpi-total", "children"),
     Output("kpi-media", "children"),
     Output("kpi-modelo", "children"),
     Output("kpi-reincidencia", "children"),
     Output("grafico-principal", "figure"),
     Output("grafico-modelos", "figure"), # Novo Output
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
    
    # 1. Copia e Filtros
    dff = df.copy()
    
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

    # --- KPIs ---
    total = len(dff)
    
    if not dff.empty and "Dias" in dff.columns:
        media_val = dff["Dias"].mean()
        media_diaria = f"{media_val:.1f} dias"
    else:
        media_diaria = "0 dias"
    
    if not dff.empty:
        top_modelo = dff["Descrição"].value_counts().idxmax()
        if len(top_modelo) > 25: top_modelo = top_modelo[:25] + "..."
    else:
        top_modelo = "-"
        
    if not dff.empty and "Reincidencia" in dff.columns:
        qtd_reincidencia = dff[dff["Reincidencia"] == "Sim"].shape[0]
        perc_r = (qtd_reincidencia / total) * 100
        reincidencia_txt = f"{perc_r:.1f}%"
    else:
        reincidencia_txt = "0%"

    # --- GRÁFICO PRINCIPAL ---
    df_chart = dff.groupby(["Ano", "Mes", "Mes_nome"]).size().reset_index(name="Quantidade")
    df_chart = df_chart.sort_values(["Ano", "Mes"])
    df_chart["Ano"] = df_chart["Ano"].astype(str)

    fig_main = px.bar(
        df_chart, x="Mes_nome", y="Quantidade", color="Ano", barmode="group",
        text_auto=True, template="plotly_white", color_discrete_sequence=COLOR_SEQUENCE
    )
    fig_main.update_layout(
        xaxis={"title": ""}, yaxis={"title": "Qtd Consertos"},
        margin=dict(l=20, r=20, t=30, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        font={"color": COLOR_TEXT_TITLE}
    )

    # --- NOVO: GRÁFICO DE MODELOS ---
    # Mostra Top 10 para caber na tela
    df_modelos = dff["Descrição"].value_counts().head(10).reset_index()
    df_modelos.columns = ["Modelo", "Quantidade"]
    df_modelos = df_modelos.sort_values("Quantidade", ascending=True) # Ordem para barra horizontal

    fig_modelos = px.bar(
        df_modelos, x="Quantidade", y="Modelo", orientation='h', text="Quantidade",
        template="plotly_white"
    )
    fig_modelos.update_traces(marker_color=COLOR_GRAPH_MAIN, textposition="outside")
    fig_modelos.update_layout(
        yaxis={"title": ""}, xaxis={"title": ""},
        margin=dict(l=20, r=20, t=20, b=20),
        font={"color": COLOR_TEXT_TITLE}
    )

    # --- GRÁFICO CATEGORIAS ---
    df_cat = dff["Categoria"].value_counts().head(10).reset_index()
    df_cat.columns = ["Categoria", "Quantidade"]
    df_cat = df_cat.sort_values("Quantidade", ascending=True)

    fig_cat = px.bar(
        df_cat, x="Quantidade", y="Categoria", orientation="h",
        text="Quantidade", template="plotly_white"
    )
    fig_cat.update_traces(marker_color=COLOR_GRAPH_MAIN, textposition="outside")
    fig_cat.update_layout(
        yaxis={"title": ""}, xaxis={"title": ""},
        margin=dict(l=20, r=20, t=20, b=20),
        font={"color": COLOR_TEXT_TITLE}
    )

    # --- GRÁFICO TIPO ---
    df_tipo_chart = dff["Tipo"].value_counts().reset_index()
    df_tipo_chart.columns = ["Tipo", "Quantidade"]
    
    fig_tipo = px.pie(
        df_tipo_chart, values="Quantidade", names="Tipo", hole=0.6,
        template="plotly_white", color_discrete_sequence=COLOR_SEQUENCE
    )
    fig_tipo.update_layout(
        margin=dict(l=20, r=20, t=20, b=20), 
        showlegend=True,
        font={"color": COLOR_TEXT_TITLE}
    )

    # --- TABELA DE DEFEITOS ---
    if not dff.empty:
        df_defeitos = dff["Defeito"].value_counts().reset_index()
        df_defeitos.columns = ["Defeito", "Quantidade"]
        table = dbc.Table.from_dataframe(df_defeitos, striped=True, bordered=True, hover=True, style={"color": "#333"})
    else:
        table = html.P("Sem dados para os filtros.", className="text-muted")

    return total, media_diaria, top_modelo, reincidencia_txt, fig_main, fig_modelos, fig_cat, fig_tipo, table

if __name__ == "__main__":
    app.run(debug=True)