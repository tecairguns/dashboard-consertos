"""
Módulo de carregamento e processamento de dados
"""

import pandas as pd
from config import NOME_ARQUIVO, NOME_ARQUIVO_EXCEL, MESES_MAP


def carregar_dados():
    """
    Carrega e processa os dados do arquivo Excel/CSV
    
    Returns:
        pd.DataFrame: DataFrame processado com os dados de consertos
    """
    # Tentar carregar CSV primeiro, depois Excel
    try:
        df = pd.read_csv(NOME_ARQUIVO, on_bad_lines='skip')
    except:
        try:
            df = pd.read_excel(NOME_ARQUIVO_EXCEL)
        except Exception as e:
            print(f"Erro ao ler arquivo: {e}")
            df = pd.DataFrame()
    
    # Tratamento de Datas
    df["Dt-Saida"] = pd.to_datetime(df["Dt-Saida"], format="%d/%m/%Y", errors="coerce")
    df = df.dropna(subset=["Dt-Saida"])
    
    # Criando colunas auxiliares
    df["Ano"] = df["Dt-Saida"].dt.year
    df["Mes"] = df["Dt-Saida"].dt.month
    df["Mes_nome"] = df["Mes"].map(MESES_MAP)
    
    # Padronização de Strings
    cols_str = ["Defeito", "Categoria", "Descrição", "Tipo", "Marca", "Garantia", "Reincidencia"]
    for col in cols_str:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.capitalize()
    
    return df


def preparar_opcoes_filtros(df):
    """
    Prepara as opções para os filtros do dashboard
    
    Args:
        df (pd.DataFrame): DataFrame com os dados
        
    Returns:
        dict: Dicionário com as opções de filtros
    """
    anos_unicos = sorted(df["Ano"].dropna().unique())
    opcoes_ano = [{"label": "Todos", "value": "all"}] + [
        {"label": str(int(ano)), "value": int(ano)} for ano in anos_unicos
    ]
    
    opcoes_mes = [{"label": nome, "value": num} for num, nome in MESES_MAP.items()]
    
    cats_unicas = sorted(df["Categoria"].dropna().unique())
    opcoes_categoria = [{"label": c, "value": c} for c in cats_unicas]
    
    opcoes_garantia = [{"label": "Todas", "value": "all"}] + [
        {"label": str(g), "value": g} for g in df["Garantia"].unique() if str(g) != 'nan'
    ]
    
    opcoes_tipo = [{"label": "Todos", "value": "all"}] + [
        {"label": str(t), "value": t} for t in df["Tipo"].unique() if str(t) != 'nan'
    ]
    
    # Opções de funcionários (para dashboard interno - apenas funcionários com consertos internos)
    df_internos = df[df["Tipo"].str.capitalize() == "Interno"]
    funcionarios_unicos = sorted([str(f) for f in df_internos["Nome"].dropna().unique() if str(f) != 'nan'])
    opcoes_funcionario = [{"label": f, "value": f} for f in funcionarios_unicos]
    
    return {
        "ano": opcoes_ano,
        "mes": opcoes_mes,
        "categoria": opcoes_categoria,
        "garantia": opcoes_garantia,
        "tipo": opcoes_tipo,
        "funcionario": opcoes_funcionario
    }


# Carregar dados ao importar o módulo
df = carregar_dados()
opcoes_filtros = preparar_opcoes_filtros(df)
