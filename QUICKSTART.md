# 🚀 Guia Rápido de Instalação

Este guia mostra como configurar e executar o projeto em **5 minutos**.

## ⚡ Instalação Rápida

### Passo 1: Clonar/Baixar o Projeto

Se ainda não tiver o projeto, baixe-o ou clone do repositório.

```bash
cd /caminho/do/projeto/REC-N-PLAY-2025-main
```

### Passo 2: Criar Ambiente Virtual (Recomendado)

```bash
# Linux/MacOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### Passo 3: Instalar Dependências

```bash
pip install -r requirements.txt
```

**⏱️ Tempo estimado**: 1-2 minutos

### Passo 4: Configurar Chave da API Groq

1. **Obter chave gratuita**:

   - Acesse: [console.groq.com](https://console.groq.com)
   - Faça login/cadastro
   - Vá em "API Keys"
   - Clique em "Create API Key"
   - Copie a chave gerada

2. **Criar arquivo `.env`**:

```bash
# Linux/MacOS
echo "GROQ_API_KEY=cole_sua_chave_aqui" > .env

# Windows (PowerShell)
Set-Content .env "GROQ_API_KEY=cole_sua_chave_aqui"

# Ou criar manualmente
# Crie um arquivo chamado .env na raiz do projeto com:
GROQ_API_KEY=sua_chave_aqui
```

### Passo 5: Executar!

```bash
python app.py
```

**⏱️ Tempo de execução**: 30-60 segundos

## 📊 Resultados

Após a execução, você verá:

```
============================================================
  GERADOR DE RELATÓRIOS FINANCEIROS
  Powered by LangChain + Groq + Matplotlib
============================================================

[1/6] Carregando configurações...
[2/6] Validando banco de dados...
✅ Banco de dados validado: /path/to/data/finance.db
[3/6] Gerando gráficos visuais...
✅ Gráficos gerados em: /path/to/reports/charts
[4/6] Construindo agente SQL...
✅ Agente SQL criado com sucesso
[5/6] Gerando relatório (aguarde, pode levar 30-60 segundos)...
🚀 Gerando relatório... (isso pode levar alguns segundos)
✅ Relatório gerado com sucesso
[6/6] Salvando arquivos...
✅ Relatório Markdown salvo: /path/to/reports/financial_report_20251016_123456.md
✅ PDF gerado com sucesso: /path/to/reports/financial_report_20251016_123456.pdf

============================================================
✅ PROCESSO CONCLUÍDO COM SUCESSO!
============================================================

📄 Relatório Markdown: reports/financial_report_20251016_123456.md
📊 Relatório PDF: reports/financial_report_20251016_123456.pdf
📈 Gráficos: reports/charts/
```

### Arquivos Gerados

Verifique a pasta `reports/`:

```
reports/
├── charts/
│   ├── monthly_revenue_expense.png    # Gráfico de barras
│   └── expense_categories.png          # Gráfico de pizza
├── financial_report_20251016_123456.md # Relatório Markdown
└── financial_report_20251016_123456.pdf # Relatório PDF (principal)
```

**🎯 Abra o arquivo PDF para visualizar o relatório completo!**

## 🐛 Solução Rápida de Problemas

### ❌ Erro: "GROQ_API_KEY não encontrada"

**Solução**:

```bash
# Verifique se o arquivo .env existe
ls -la .env  # Linux/MacOS
dir .env     # Windows

# Se não existir, crie-o:
echo "GROQ_API_KEY=sua_chave_aqui" > .env
```

### ❌ Erro: "Banco de dados não encontrado"

**Solução**:

```bash
# Verificar se o arquivo existe
ls data/finance.db

# Se não existir, popular o banco:
sqlite3 data/finance.db < seed_db.sql
```

### ❌ Erro: "No module named 'weasyprint'"

**Solução**:

```bash
# Reinstalar dependências
pip install -r requirements.txt --force-reinstall

# Se persistir, instalar manualmente:
pip install weasyprint
```

### ❌ PDF não gerado (mas MD foi criado)

**Causa**: WeasyPrint requer bibliotecas do sistema.

**Solução Ubuntu/Debian**:

```bash
sudo apt-get update
sudo apt-get install libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
```

**Solução MacOS**:

```bash
brew install pango gdk-pixbuf libffi
```

**Solução Windows**:

- Baixe e instale GTK3: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer

### ❌ Gráficos não aparecem

**Causa**: Matplotlib não configurado corretamente.

**Solução**:

```bash
pip uninstall matplotlib
pip install matplotlib
```

## 🎨 Personalização Rápida

### Mudar Modelo do Groq

Edite `app.py`, linha 199:

```python
# Mais rápido (padrão)
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)

# Mais preciso
llm = ChatGroq(model="llama-3.1-70b-versatile", temperature=0)

# Contexto maior
llm = ChatGroq(model="mixtral-8x7b-32768", temperature=0)
```

### Modificar Período de Análise

Edite `reports/prompt/report_prompt-2.md`, linha 13:

```markdown
- **Período**: Todo o ano de 2024 (janeiro a dezembro)

# Mude para:

- **Período**: Primeiro semestre de 2024
```

### Alterar Cores dos Gráficos

Edite `app.py`, linhas 108-109 (gráfico de barras):

```python
bars1 = ax.bar([i - width/2 for i in x], revenues, width, label='Receita', color='#2ecc71')  # Verde
bars2 = ax.bar([i + width/2 for i in x], expenses, width, label='Despesa', color='#e74c3c')  # Vermelho
```

Edite `app.py`, linha 157 (gráfico de pizza):

```python
colors = ['#e74c3c', '#3498db', '#f39c12', '#9b59b6', '#1abc9c']
```

## 📚 Próximos Passos

Agora que o sistema está funcionando:

1. **Explore o relatório PDF** gerado
2. **Leia o README.md** completo para funcionalidades avançadas
3. **Customize o prompt** em `reports/prompt/report_prompt-2.md`
4. **Modifique os gráficos** para suas necessidades
5. **Adicione seus próprios dados** no banco SQLite

## 🆘 Precisa de Ajuda?

- 📖 Leia o **README.md** para documentação completa
- 📝 Veja o **CHANGELOG.md** para detalhes das melhorias
- 🔍 Confira a seção de troubleshooting no README

---

**🎉 Pronto! Seu gerador de relatórios está funcionando!**
