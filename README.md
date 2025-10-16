# 📊 Gerador de Relatórios Financeiros com IA

Sistema inteligente de geração de relatórios financeiros usando **LangChain**, **Groq (Llama)**, **Matplotlib** e conversão automática para PDF.

## ✨ Funcionalidades

- 🤖 **Análise Inteligente**: Agente SQL com LangChain + Groq para análise automática de dados
- 📈 **Gráficos Visuais**: Geração automática de gráficos com Matplotlib
  - Receita vs Despesa mensal (barras)
  - Distribuição de despesas por categoria (pizza)
- 📄 **Relatórios Profissionais**: Geração de relatórios em Markdown e PDF
- 🎨 **PDF Estilizado**: Conversão com CSS profissional e gráficos incorporados
- ✅ **Validações**: Tratamento robusto de erros e validações de dados
- 🔍 **KPIs Automáticos**: Receita, Despesa, Lucro Líquido e Margem de Lucro

## 📁 Estrutura do Projeto

```
REC-N-PLAY-2025-main/
├── data/
│   └── finance.db              # Banco de dados SQLite
├── reports/
│   ├── charts/                 # Gráficos PNG gerados
│   ├── prompt/
│   │   └── report_prompt-2.md  # Prompt para o agente IA
│   ├── financial_report_*.md   # Relatórios Markdown
│   └── financial_report_*.pdf  # Relatórios PDF
├── app.py                      # Aplicação principal
├── seed_db.sql                 # Script para popular o banco
├── requirements.txt            # Dependências Python
└── README.md
```

## 🚀 Como Usar

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

**Dependências instaladas:**

- `langchain` e `langchain-community` - Framework para agentes IA
- `langchain-groq` - Integração com Groq (Llama)
- `matplotlib` - Geração de gráficos
- `markdown2` - Conversão Markdown → HTML
- `weasyprint` - Conversão HTML → PDF
- `sqlalchemy` - Manipulação de banco de dados
- `python-dotenv` - Gerenciamento de variáveis de ambiente

### 2. Configurar Chave da API Groq

```bash
# Criar arquivo .env na raiz do projeto
echo "GROQ_API_KEY=sua_chave_aqui" > .env
```

> 🔑 Obtenha sua chave gratuita em: [console.groq.com](https://console.groq.com)

### 3. Executar o Gerador

```bash
python app.py
```

**O sistema irá:**

1. ✅ Validar banco de dados e configurações
2. 📊 Gerar gráficos visuais (PNG)
3. 🤖 Executar agente SQL para análise
4. 📝 Criar relatório em Markdown
5. 📄 Converter para PDF com gráficos incorporados

### 4. Resultados

Os arquivos gerados estarão em:

- `reports/financial_report_YYYYMMDD_HHMMSS.md` - Relatório Markdown
- `reports/financial_report_YYYYMMDD_HHMMSS.pdf` - Relatório PDF
- `reports/charts/` - Gráficos PNG

## 📊 Estrutura do Banco de Dados

### Tabela `accounts`

```sql
id INTEGER PRIMARY KEY
name TEXT           -- Nome da conta
type TEXT           -- 'bank', 'credit', 'cash'
```

### Tabela `transactions`

```sql
id INTEGER PRIMARY KEY
date TEXT           -- Data ISO (YYYY-MM-DD)
type TEXT           -- 'REVENUE' ou 'EXPENSE'
category TEXT       -- Categoria da transação
description TEXT    -- Descrição
amount REAL         -- Valor (sempre positivo)
account_id INTEGER  -- FK para accounts
```

## 🎨 Personalização

### Modificar o Prompt do Relatório

Edite `reports/prompt/report_prompt-2.md` para ajustar:

- KPIs exibidos
- Estrutura do relatório
- Nível de detalhamento
- Insights solicitados

### Alterar Modelo do Groq

No arquivo `app.py`, linha 199:

```python
llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
```

Modelos disponíveis:

- `llama-3.1-8b-instant` - Rápido e econômico
- `llama-3.1-70b-versatile` - Mais preciso
- `mixtral-8x7b-32768` - Contexto maior

### Customizar Gráficos

Na função `generate_charts()` (linha 63 de `app.py`), você pode:

- Alterar cores dos gráficos
- Adicionar novos tipos de visualização
- Modificar tamanho e resolução (DPI)

### Estilizar o PDF

Na função `convert_md_to_pdf()` (linha 241), edite a variável `css_style` para:

- Alterar fontes e cores
- Ajustar margens e espaçamento
- Modificar aparência de tabelas

## 🔧 Funções Principais

| Função                | Descrição                                        |
| --------------------- | ------------------------------------------------ |
| `load_env()`          | Carrega variáveis de ambiente e valida chave API |
| `validate_database()` | Verifica existência e estrutura do banco         |
| `generate_charts()`   | Gera gráficos PNG com matplotlib                 |
| `build_agent()`       | Cria agente SQL com LangChain + Groq             |
| `generate_report()`   | Executa análise e gera relatório MD              |
| `convert_md_to_pdf()` | Converte MD → PDF com estilização                |
| `main()`              | Orquestra todo o fluxo de execução               |

## 🛡️ Tratamento de Erros

O sistema inclui validações robustas para:

- ✅ Verificar existência do banco de dados
- ✅ Validar presença de tabelas necessárias
- ✅ Confirmar chave da API Groq
- ✅ Capturar erros na geração de relatórios
- ✅ Mensagens de erro claras e acionáveis

## 📝 Exemplo de Relatório Gerado

O relatório inclui:

1. **Resumo Executivo** - KPIs principais
2. **Análise Mensal** - Tabela com receita/despesa por mês
3. **Top 5 Categorias de Despesa** - Maiores gastos
4. **Análise por Conta** - Distribuição por tipo de conta
5. **Insights e Recomendações** - Análise qualitativa da IA
6. **Visualizações Gráficas** - Gráficos incorporados no PDF
7. **Consultas SQL** - Queries utilizadas na análise

## 🐛 Solução de Problemas

### Erro: "GROQ_API_KEY não encontrada"

```bash
# Criar arquivo .env com a chave
echo "GROQ_API_KEY=sua_chave_aqui" > .env
```

### Erro: "Banco de dados não encontrado"

```bash
# Verificar se o arquivo existe
ls data/finance.db

# Se necessário, popular o banco
sqlite3 data/finance.db < seed_db.sql
```

### PDF não gerado

O WeasyPrint requer dependências do sistema:

```bash
# Ubuntu/Debian
sudo apt-get install libpango-1.0-0 libpangocairo-1.0-0

# MacOS
brew install pango
```

## 📄 Licença

Projeto educacional para demonstração de IA aplicada a análise de dados financeiros.
