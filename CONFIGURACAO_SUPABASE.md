# INSTRUÇÕES DE CONFIGURAÇÃO - Dashboard de Atividades

## 📋 Próximos Passos

A implementação do dashboard "Atividades" está completa! Agora você precisa configurar as credenciais do Supabase.

## 🔑 Configurar Keys do Supabase

1. **Abra o arquivo** `supabase_config.py` no diretório do projeto

2. **Localize as linhas com as credenciais:**
   ```python
   SUPABASE_URL = "YOUR_SUPABASE_URL_HERE"
   SUPABASE_KEY = "YOUR_SUPABASE_ANON_KEY_HERE"
   ```

3. **Substitua pelos valores reais do seu projeto Supabase:**
   - `SUPABASE_URL`: A URL do seu projeto (ex: `https://xxxxxxxxxxx.supabase.co`)
   - `SUPABASE_KEY`: A chave anônima (anon/public key) do seu projeto

### Como encontrar suas credenciais no Supabase:

1. Acesse [supabase.com](https://supabase.com) e faça login
2. Selecione seu projeto
3. No menu lateral, clique em **Settings** (⚙️)
4. Clique em **API**
5. Você encontrará:
   - **Project URL** → cole em `SUPABASE_URL`
   - **anon public** (na seção API Keys) → cole em `SUPABASE_KEY`

### Exemplo de configuração:
```python
SUPABASE_URL = "https://abcdefghijklmnop.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTY5MDAwMDAwMCwiZXhwIjoyMDA1NTc2MDAwfQ.exemplo-de-token-aqui"
```

## 📦 Instalar Dependências

Antes de executar, instale as novas dependências:

```bash
pip install -r requirements.txt
```

Ou instalar apenas as novas bibliotecas:

```bash
pip install supabase python-dotenv
```

## 🚀 Executar o Dashboard

Após configurar as credenciais, execute o dashboard:

```bash
python app.py
```

Acesse no navegador: `http://127.0.0.1:8050/atividades`

## ✅ Verificação

Para testar se a conexão está funcionando:

1. Execute o dashboard
2. Navegue para a aba "Atividades" na sidebar
3. Os filtros de funcionários e funções devem ser carregados automaticamente do Supabase
4. Selecione um período e verifique se os dados são exibidos

Se houver erro, verifique:
- ✔️ As credenciais estão corretas no `supabase_config.py`
- ✔️ As tabelas `employees`, `functions` e `time_records` existem no seu banco Supabase
- ✔️ As tabelas têm as colunas corretas conforme o SQL fornecido
