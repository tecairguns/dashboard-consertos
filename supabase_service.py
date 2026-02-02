"""
Serviço de integração com Supabase
Gerencia todas as operações de leitura/escrita no banco de dados
"""

from supabase import create_client, Client
from supabase_config import SUPABASE_URL, SUPABASE_KEY
import pandas as pd
from datetime import datetime


# =====================================================================
# CONEXÃO
# =====================================================================

def get_supabase_client() -> Client:
    """
    Retorna uma instância configurada do cliente Supabase
    
    Returns:
        Client: Cliente Supabase configurado
    """
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        return supabase
    except Exception as e:
        print(f"Erro ao conectar com Supabase: {e}")
        return None


# =====================================================================
# FUNÇÕES DE LEITURA
# =====================================================================

def get_employees():
    """
    Busca todos os funcionários da tabela employees
    
    Returns:
        list: Lista de dicionários com dados dos funcionários
    """
    try:
        supabase = get_supabase_client()
        response = supabase.table('employees').select('*').execute()
        return response.data
    except Exception as e:
        print(f"Erro ao buscar funcionários: {e}")
        return []


def get_functions():
    """
    Busca todas as funções da tabela functions
    
    Returns:
        list: Lista de dicionários com dados das funções
    """
    try:
        supabase = get_supabase_client()
        response = supabase.table('functions').select('*').execute()
        return response.data
    except Exception as e:
        print(f"Erro ao buscar funções: {e}")
        return []


def get_time_records(filtro_funcionarios=None, filtro_funcoes=None, data_inicio=None, data_fim=None):
    """
    Busca registros de tempo da tabela time_records com filtros opcionais
    
    Args:
        filtro_funcionarios (list): Lista de nomes de funcionários para filtrar
        filtro_funcoes (list): Lista de nomes de funções para filtrar
        data_inicio (str): Data inicial no formato 'YYYY-MM-DD'
        data_fim (str): Data final no formato 'YYYY-MM-DD'
        
    Returns:
        list: Lista de dicionários com registros de tempo
    """
    try:
        supabase = get_supabase_client()
        query = supabase.table('time_records').select('*')
        
        # Aplicar filtros se fornecidos
        if filtro_funcionarios and len(filtro_funcionarios) > 0:
            query = query.in_('employee_name', filtro_funcionarios)
        
        if filtro_funcoes and len(filtro_funcoes) > 0:
            query = query.in_('function_name', filtro_funcoes)
        
        if data_inicio:
            query = query.gte('start_time', data_inicio)
        
        if data_fim:
            # Adicionar 1 dia para incluir registros do último dia
            query = query.lte('start_time', data_fim + 'T23:59:59')
        
        response = query.execute()
        return response.data
    except Exception as e:
        print(f"Erro ao buscar registros de tempo: {e}")
        return []


# =====================================================================
# FUNÇÕES DE CÁLCULO
# =====================================================================

def calculate_kpis(records):
    """
    Calcula os KPIs baseados nos registros de tempo
    
    Args:
        records (list): Lista de registros de tempo
        
    Returns:
        dict: Dicionário com os KPIs calculados
    """
    if not records or len(records) == 0:
        return {
            'total_registros': 0,
            'total_horas': 0,
            'qtd_funcionarios': 0,
            'qtd_funcoes': 0
        }
    
    # Converter para DataFrame para facilitar cálculos
    df = pd.DataFrame(records)
    
    # Filtrar apenas registros com duration_ms válido (não nulo e maior que 0)
    if 'duration_ms' in df.columns:
        df = df[df['duration_ms'].notna()]  # Remove valores nulos
        df = df[df['duration_ms'] > 0]  # Remove valores negativos ou zero
    
    # Total de registros (após filtragem)
    total_registros = len(df)
    
    # Total de horas (converter duration_ms para horas)
    # duration_ms / (1000 * 60 * 60) = horas
    if total_registros > 0:
        total_horas = df['duration_ms'].sum() / (1000 * 60 * 60)
    else:
        total_horas = 0
    
    # Quantidade de funcionários únicos
    qtd_funcionarios = df['employee_name'].nunique() if total_registros > 0 else 0
    
    # Quantidade de funções únicas
    qtd_funcoes = df['function_name'].nunique() if total_registros > 0 else 0
    
    return {
        'total_registros': total_registros,
        'total_horas': round(total_horas, 2),
        'qtd_funcionarios': qtd_funcionarios,
        'qtd_funcoes': qtd_funcoes
    }



def get_distribuicao_por_funcao(records):
    """
    Calcula a distribuição de horas por função
    
    Args:
        records (list): Lista de registros de tempo
        
    Returns:
        pd.DataFrame: DataFrame com colunas 'function_name' e 'total_horas'
    """
    if not records or len(records) == 0:
        return pd.DataFrame(columns=['function_name', 'total_horas'])
    
    df = pd.DataFrame(records)
    
    # Filtrar apenas registros com duration_ms válido
    if 'duration_ms' in df.columns:
        df = df[df['duration_ms'].notna()]
        df = df[df['duration_ms'] > 0]
    
    if df.empty:
        return pd.DataFrame(columns=['function_name', 'total_horas'])
    
    # Converter duration_ms para horas
    df['horas'] = df['duration_ms'] / (1000 * 60 * 60)
    
    # Agrupar por função
    df_grouped = df.groupby('function_name')['horas'].sum().reset_index()
    df_grouped.columns = ['function_name', 'total_horas']
    df_grouped = df_grouped.sort_values('total_horas', ascending=False)
    
    return df_grouped


def get_distribuicao_por_funcionario(records):
    """
    Calcula a distribuição de horas por funcionário
    
    Args:
        records (list): Lista de registros de tempo
        
    Returns:
        pd.DataFrame: DataFrame com colunas 'employee_name' e 'total_horas'
    """
    if not records or len(records) == 0:
        return pd.DataFrame(columns=['employee_name', 'total_horas'])
    
    df = pd.DataFrame(records)
    
    # Filtrar apenas registros com duration_ms válido
    if 'duration_ms' in df.columns:
        df = df[df['duration_ms'].notna()]
        df = df[df['duration_ms'] > 0]
    
    if df.empty:
        return pd.DataFrame(columns=['employee_name', 'total_horas'])
    
    # Converter duration_ms para horas
    df['horas'] = df['duration_ms'] / (1000 * 60 * 60)
    
    # Agrupar por funcionário
    df_grouped = df.groupby('employee_name')['horas'].sum().reset_index()
    df_grouped.columns = ['employee_name', 'total_horas']
    df_grouped = df_grouped.sort_values('total_horas', ascending=False)
    
    return df_grouped
