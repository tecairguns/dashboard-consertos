from supabase_service import get_supabase_client
import pandas as pd

supabase = get_supabase_client()

# Verificar ongoing_activities
print("Verificando tabela ongoing_activities...")
try:
    response = supabase.table('ongoing_activities').select('*').execute()
    ongoing = response.data
    print(f"Registros em ongoing_activities: {len(ongoing)}")
    
    if len(ongoing) > 0:
        df_ongoing = pd.DataFrame(ongoing)
        print("\nFuncionários em ongoing_activities:")
        print(df_ongoing['employee_name'].unique())
        
        print("\nHoras por funcionário (se tiver duration):")
        if 'duration_ms' in df_ongoing.columns:
            totals = df_ongoing.groupby('employee_name')['duration_ms'].apply(lambda x: x.sum() / (1000*60*60)).round(2)
            print(totals)
except Exception as e:
    print(f"Erro: {e}")

print("\n" + "="*60)
print("Resumo:")
print("="*60)
print("time_records:")
response_tr = supabase.table('time_records').select('employee_name,duration_ms').execute()
df_tr = pd.DataFrame(response_tr.data)
print(f"  Mikael: {df_tr[df_tr['employee_name']=='Mikael']['duration_ms'].sum() / (1000*60*60):.2f}h")
print(f"  Maurício: {df_tr[df_tr['employee_name']=='Maurício']['duration_ms'].sum() / (1000*60*60):.2f}h")
