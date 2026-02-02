from supabase_service import get_employees

employees = get_employees()
print('Lista de funcionários da tabela employees:')
for emp in employees:
    print(f"  - '{emp['name']}'")
