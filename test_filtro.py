from supabase_service import get_time_records
import pandas as pd

print("Testando filtro por Mikael...")
records_mikael = get_time_records(filtro_funcionarios=['Mikael'])
df_m = pd.DataFrame(records_mikael)
print(f"Registros: {len(df_m)}")
print(f"Total horas: {(df_m['duration_ms'].sum() / (1000*60*60)):.2f}h")

print("\nTestando filtro por Maurício...")
records_mauricio = get_time_records(filtro_funcionarios=['Maurício'])
df_ma = pd.DataFrame(records_mauricio)
print(f"Registros: {len(df_ma)}")
print(f"Total horas: {(df_ma['duration_ms'].sum() / (1000*60*60)):.2f}h")

print("\nSem filtro (todos)...")
records_all = get_time_records()
df_all = pd.DataFrame(records_all)
print(f"Registros: {len(df_all)}")
print(f"Total horas Mikael: {(df_all[df_all['employee_name']=='Mikael']['duration_ms'].sum() / (1000*60*60)):.2f}h")
print(f"Total horas Maurício: {(df_all[df_all['employee_name']=='Maurício']['duration_ms'].sum() / (1000*60*60)):.2f}h")
