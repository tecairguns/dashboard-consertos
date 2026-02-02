"""
Script de debug para investigar discrepâncias nos dados
Execute este script para analisar os dados do Supabase
"""

from supabase_service import get_time_records
import pandas as pd

# Buscar todos os registros
print("Buscando dados do Supabase...")
all_records = get_time_records()

print(f"\n{'='*60}")
print(f"Total de registros no banco: {len(all_records)}")
print(f"{'='*60}\n")

# Converter para DataFrame
df = pd.DataFrame(all_records)

# Verificar valores nulos em duration_ms
null_duration = df[df['duration_ms'].isna()]
print(f"Registros com duration_ms NULO: {len(null_duration)}")

# Verificar valores zero ou negativos
zero_negative = df[df['duration_ms'] <= 0]
print(f"Registros com duration_ms <= 0: {len(zero_negative)}")

# Filtrar apenas válidos
df_valid = df[(df['duration_ms'].notna()) & (df['duration_ms'] > 0)]
print(f"Registros VÁLIDOS: {len(df_valid)}")

# Converter para horas
df_valid['horas'] = df_valid['duration_ms'] / (1000 * 60 * 60)

print(f"\n{'='*60}")
print("ANÁLISE POR FUNCIONÁRIO")
print(f"{'='*60}\n")

# Agrupar por funcionário
funcionarios = df_valid.groupby('employee_name').agg({
    'horas': 'sum',
    'id': 'count'
}).reset_index()
funcionarios.columns = ['Funcionário', 'Total Horas', 'Qtd Registros']
funcionarios = funcionarios.sort_values('Total Horas', ascending=False)

print(funcionarios.to_string(index=False))

print(f"\n{'='*60}")
print("TOTAL GERAL")
print(f"{'='*60}\n")
print(f"Total de Horas (todos funcionários): {df_valid['horas'].sum():.2f}h")
print(f"Total de Registros (todos funcionários): {len(df_valid)}")

# Verificar se há nomes duplicados com espaços ou diferenças
print(f"\n{'='*60}")
print("VERIFICAR POSSÍVEIS DUPLICAÇÕES DE NOMES")
print(f"{'='*60}\n")

unique_names = df_valid['employee_name'].unique()
for name in unique_names:
    # Verificar se há variações do mesmo nome
    similar = [n for n in unique_names if name.lower().strip() in n.lower().strip() or n.lower().strip() in name.lower().strip()]
    if len(similar) > 1:
        print(f"Possível duplicação: {similar}")
        for variant in similar:
            count = len(df_valid[df_valid['employee_name'] == variant])
            total_h = df_valid[df_valid['employee_name'] == variant]['horas'].sum()
            print(f"  '{variant}': {count} registros, {total_h:.2f}h")
