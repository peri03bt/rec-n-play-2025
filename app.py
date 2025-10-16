import os
import sys
import sqlite3
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_groq import ChatGroq
from langchain.agents import create_sql_agent
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Backend não-interativo para servidores
import markdown2
from weasyprint import HTML, CSS
from io import StringIO

# Configuração de diretórios
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"
CHARTS_DIR = REPORTS_DIR / "charts"
PROMPT_PATH = REPORTS_DIR / "prompt" / "report_prompt-2.md"


def load_env():
    """Carrega variáveis de ambiente do arquivo .env"""
    env_path = BASE_DIR / ".env"
    if not env_path.exists():
        print("⚠️  Arquivo .env não encontrado. Certifique-se de ter a GROQ_API_KEY configurada.")
    load_dotenv(env_path, override=False)
    
    # Validar se a chave existe
    if not os.getenv("GROQ_API_KEY"):
        raise ValueError("❌ GROQ_API_KEY não encontrada no arquivo .env")


def validate_database():
    """Valida se o banco de dados existe e tem as tabelas necessárias"""
    db_path = DATA_DIR / "finance.db"
    
    if not db_path.exists():
        raise FileNotFoundError(f"❌ Banco de dados não encontrado: {db_path}")
    
    # Verificar tabelas
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    required_tables = ['transactions', 'accounts']
    missing_tables = [t for t in required_tables if t not in tables]
    
    conn.close()
    
    if missing_tables:
        raise ValueError(f"❌ Tabelas ausentes no banco: {', '.join(missing_tables)}")
    
    print(f"✅ Banco de dados validado: {db_path}")


def generate_charts(db_path, output_dir, year=2024):
    """
    Gera gráficos visuais a partir dos dados do banco
    
    Args:
        db_path: Caminho para o banco SQLite
        output_dir: Diretório onde salvar os gráficos
        year: Ano para análise (padrão: 2024)
    
    Returns:
        dict: Informações sobre os gráficos gerados
    """
    output_dir.mkdir(exist_ok=True, parents=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 1. Gráfico: Receita vs Despesa Mensal
    query_monthly = f"""
        SELECT 
            strftime('%m', date) as month,
            SUM(CASE WHEN type='REVENUE' THEN amount ELSE 0 END) as revenue,
            SUM(CASE WHEN type='EXPENSE' THEN amount ELSE 0 END) as expense
        FROM transactions
        WHERE strftime('%Y', date) = '{year}'
        GROUP BY month
        ORDER BY month
    """
    
    cursor.execute(query_monthly)
    monthly_data = cursor.fetchall()
    
    months = [int(row[0]) for row in monthly_data]
    revenues = [row[1] for row in monthly_data]
    expenses = [row[2] for row in monthly_data]
    
    month_names = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                   'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    month_labels = [month_names[m-1] for m in months]
    
    # Plotar gráfico de barras
    fig, ax = plt.subplots(figsize=(12, 6))
    x = range(len(months))
    width = 0.35
    
    bars1 = ax.bar([i - width/2 for i in x], revenues, width, label='Receita', color='#2ecc71')
    bars2 = ax.bar([i + width/2 for i in x], expenses, width, label='Despesa', color='#e74c3c')
    
    ax.set_xlabel('Mês', fontsize=12)
    ax.set_ylabel('Valor (R$)', fontsize=12)
    ax.set_title(f'Receita vs Despesa Mensal - {year}', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(month_labels)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    # Adicionar valores nas barras
    for bar in bars1:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'R$ {height:,.0f}',
                ha='center', va='bottom', fontsize=8)
    
    for bar in bars2:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'R$ {height:,.0f}',
                ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    chart1_path = output_dir / "monthly_revenue_expense.png"
    plt.savefig(chart1_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Gráfico: Top Categorias de Despesa (Pizza)
    query_categories = f"""
        SELECT 
            category,
            SUM(amount) as total
        FROM transactions
        WHERE strftime('%Y', date) = '{year}' AND type='EXPENSE'
        GROUP BY category
        ORDER BY total DESC
        LIMIT 5
    """
    
    cursor.execute(query_categories)
    category_data = cursor.fetchall()
    
    categories = [row[0] for row in category_data]
    totals = [row[1] for row in category_data]
    
    # Plotar gráfico de pizza
    fig, ax = plt.subplots(figsize=(10, 8))
    colors = ['#e74c3c', '#3498db', '#f39c12', '#9b59b6', '#1abc9c']
    
    wedges, texts, autotexts = ax.pie(totals, labels=categories, autopct='%1.1f%%',
                                        colors=colors, startangle=90)
    
    # Melhorar aparência
    for text in texts:
        text.set_fontsize(11)
        text.set_fontweight('bold')
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(10)
        autotext.set_fontweight('bold')
    
    ax.set_title(f'Distribuição de Despesas por Categoria - {year}', 
                 fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    chart2_path = output_dir / "expense_categories.png"
    plt.savefig(chart2_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    conn.close()
    
    print(f"✅ Gráficos gerados em: {output_dir}")
    
    return {
        'monthly_chart': chart1_path,
        'categories_chart': chart2_path,
        'charts_generated': True
    }

    
def build_agent():
    """Constrói o agente SQL com LangChain + Groq"""
    try:
        # Conexão com banco
        db_uri = f"sqlite:///{(DATA_DIR / 'finance.db').as_posix()}"
        db = SQLDatabase.from_uri(db_uri)

        # Instanciar o modelo Groq com configurações otimizadas
        llm = ChatGroq(
            model="llama-3.3-70b-versatile", 
            temperature=0,
            max_tokens=4096
        )

        # Criar a ferramenta
        toolkit = SQLDatabaseToolkit(db=db, llm=llm)

        # Criar o agente com configurações mais robustas
        agent = create_sql_agent(
            llm=llm,
            toolkit=toolkit,
            verbose=True,
            agent_type="openai-tools",  # Tipo mais estável
            top_k=10,
            max_iterations=15,  # Mais iterações permitidas
            max_execution_time=120,  # Timeout de 2 minutos
            handle_parsing_errors=True  # Tratar erros de parsing
        )
        
        print("✅ Agente SQL criado com sucesso")
        return agent
    
    except Exception as e:
        raise RuntimeError(f"❌ Erro ao criar agente: {str(e)}")


def generate_report(agent, prompt):
    """
    Gera o relatório usando o agente
    
    Args:
        agent: Agente LangChain
        prompt: Texto do prompt
    
    Returns:
        str: Conteúdo do relatório em Markdown
    """
    try:
        print("🚀 Gerando relatório... (isso pode levar alguns segundos)")
        result = agent.run(prompt)
        print("✅ Relatório gerado com sucesso")
        return result
    
    except Exception as e:
        raise RuntimeError(f"❌ Erro ao gerar relatório: {str(e)}")


def convert_md_to_pdf(md_path, pdf_path, charts_dir):
    """
    Converte arquivo Markdown para PDF com estilização
    
    Args:
        md_path: Caminho do arquivo .md
        pdf_path: Caminho de saída do .pdf
        charts_dir: Diretório dos gráficos
    """
    try:
        # Ler conteúdo Markdown
        md_content = md_path.read_text(encoding='utf-8')
        
        # Converter MD para HTML
        html_content = markdown2.markdown(
            md_content,
            extras=['tables', 'fenced-code-blocks', 'code-friendly']
        )
        
        # CSS para estilização profissional
        css_style = """
        @page {
            size: A4;
            margin: 2cm;
        }
        
        body {
            font-family: 'Helvetica', 'Arial', sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 100%;
        }
        
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-top: 0;
        }
        
        h2 {
            color: #34495e;
            border-bottom: 2px solid #95a5a6;
            padding-bottom: 8px;
            margin-top: 30px;
        }
        
        h3 {
            color: #7f8c8d;
            margin-top: 20px;
        }
        
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
            font-size: 0.9em;
        }
        
        th {
            background-color: #3498db;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
        }
        
        td {
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }
        
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        
        tr:hover {
            background-color: #e8f4f8;
        }
        
        code {
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }
        
        pre {
            background-color: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            font-size: 0.85em;
        }
        
        pre code {
            background-color: transparent;
            color: #ecf0f1;
            padding: 0;
        }
        
        img {
            max-width: 100%;
            height: auto;
            margin: 20px 0;
            display: block;
        }
        
        strong {
            color: #2c3e50;
        }
        
        ul, ol {
            margin: 15px 0;
            padding-left: 30px;
        }
        
        li {
            margin: 8px 0;
        }
        """
        
        # Adicionar referências às imagens dos gráficos
        chart_html = f"""
        <div style="page-break-before: always;">
            <h2>Visualizações Gráficas</h2>
            <h3>Evolução Mensal - Receita vs Despesa</h3>
            <img src="{charts_dir / 'monthly_revenue_expense.png'}" alt="Gráfico Mensal" style="width: 100%;">
            
            <h3>Distribuição de Despesas por Categoria</h3>
            <img src="{charts_dir / 'expense_categories.png'}" alt="Gráfico de Categorias" style="width: 80%; margin: 0 auto;">
        </div>
        """
        
        # Montar HTML completo
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>{css_style}</style>
        </head>
        <body>
            {html_content}
            {chart_html}
        </body>
        </html>
        """
        
        # Gerar PDF
        HTML(string=full_html, base_url=str(BASE_DIR)).write_pdf(
            pdf_path,
            stylesheets=[CSS(string=css_style)]
        )
        
        print(f"✅ PDF gerado com sucesso: {pdf_path}")
        
    except Exception as e:
        print(f"⚠️  Erro ao gerar PDF: {str(e)}")
        print("   O relatório em Markdown foi salvo, mas o PDF não pôde ser criado.")


def main():
    """Função principal que orquestra todo o fluxo"""
    try:
        print("\n" + "="*60)
        print("  GERADOR DE RELATÓRIOS FINANCEIROS")
        print("  Powered by LangChain + Groq + Matplotlib")
        print("="*60 + "\n")
        
        # 1. Carregar variáveis de ambiente
        print("[1/6] Carregando configurações...")
        load_env()
        
        # 2. Validar banco de dados
        print("[2/6] Validando banco de dados...")
        validate_database()
        
        # 3. Criar diretórios necessários
        REPORTS_DIR.mkdir(exist_ok=True)
        CHARTS_DIR.mkdir(exist_ok=True)
        
        # 4. Gerar gráficos
        print("[3/6] Gerando gráficos visuais...")
        db_path = DATA_DIR / "finance.db"
        charts_info = generate_charts(db_path, CHARTS_DIR)
        
        # 5. Construir agente e gerar relatório
        print("[4/6] Construindo agente SQL...")
        agent = build_agent()
        
        print("[5/6] Gerando relatório (aguarde, pode levar 30-60 segundos)...")
        prompt = PROMPT_PATH.read_text(encoding="utf-8")
        report_content = generate_report(agent, prompt)
        
        # 6. Salvar arquivos
        print("[6/6] Salvando arquivos...")
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Salvar Markdown
        md_path = REPORTS_DIR / f"financial_report_{ts}.md"
        md_path.write_text(report_content, encoding="utf-8")
        print(f"✅ Relatório Markdown salvo: {md_path}")
        
        # Converter para PDF
        pdf_path = REPORTS_DIR / f"financial_report_{ts}.pdf"
        convert_md_to_pdf(md_path, pdf_path, CHARTS_DIR)
        
        print("\n" + "="*60)
        print("✅ PROCESSO CONCLUÍDO COM SUCESSO!")
        print("="*60)
        print(f"\n📄 Relatório Markdown: {md_path}")
        print(f"📊 Relatório PDF: {pdf_path}")
        print(f"📈 Gráficos: {CHARTS_DIR}/")
        print("\n")
        
    except Exception as e:
        print("\n" + "="*60)
        print("❌ ERRO NA EXECUÇÃO")
        print("="*60)
        print(f"\n{str(e)}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
