# 💼 Exemplos de Uso

Este documento mostra casos de uso práticos do sistema de geração de relatórios.

## 🎯 Caso de Uso 1: Executivo que precisa de relatório mensal

### Cenário:

Você é CFO e precisa apresentar os resultados financeiros de 2024 para a diretoria amanhã.

### Solução:

```bash
# 1. Execute o sistema
python app.py

# 2. Aguarde 60 segundos
# ⏱️ O sistema irá:
#    - Validar dados
#    - Gerar gráficos
#    - Criar análise com IA
#    - Gerar PDF profissional

# 3. Abra o PDF gerado
open reports/financial_report_*.pdf

# ✅ Pronto! Relatório completo com gráficos prontos para apresentar
```

**Tempo total: 2 minutos**

---

## 📊 Caso de Uso 2: Analista que quer customizar os gráficos

### Cenário:

Você quer mudar as cores dos gráficos para combinar com a identidade visual da empresa.

### Solução:

#### Passo 1: Definir suas cores

```python
# Cores da sua empresa
COR_PRINCIPAL = '#1E88E5'    # Azul corporativo
COR_SECUNDARIA = '#FFC107'   # Amarelo destaque
COR_SUCESSO = '#43A047'      # Verde
COR_ALERTA = '#E53935'       # Vermelho
```

#### Passo 2: Editar `app.py`

**Gráfico de barras (linha 108-109):**

```python
# ANTES:
bars1 = ax.bar([i - width/2 for i in x], revenues, width, label='Receita', color='#2ecc71')
bars2 = ax.bar([i + width/2 for i in x], expenses, width, label='Despesa', color='#e74c3c')

# DEPOIS:
bars1 = ax.bar([i - width/2 for i in x], revenues, width, label='Receita', color='#43A047')
bars2 = ax.bar([i + width/2 for i in x], expenses, width, label='Despesa', color='#E53935')
```

**Gráfico de pizza (linha 157):**

```python
# ANTES:
colors = ['#e74c3c', '#3498db', '#f39c12', '#9b59b6', '#1abc9c']

# DEPOIS:
colors = ['#1E88E5', '#43A047', '#FFC107', '#E53935', '#7E57C2']
```

#### Passo 3: Executar

```bash
python app.py
```

**✅ Gráficos agora usam suas cores corporativas!**

---

## 🎨 Caso de Uso 3: Designer quer PDF mais elegante

### Cenário:

Você quer um PDF com fonte diferente e cores mais modernas.

### Solução:

Edite `app.py`, função `convert_md_to_pdf()`, linha ~261:

```css
/* ANTES */
body {
  font-family: "Helvetica", "Arial", sans-serif;
  color: #333;
}

h1 {
  color: #2c3e50;
  border-bottom: 3px solid #3498db;
}

/* DEPOIS */
body {
  font-family: "Georgia", "Times New Roman", serif;
  color: #1a1a1a;
}

h1 {
  color: #1e88e5;
  border-bottom: 4px solid #ffc107;
  text-transform: uppercase;
  letter-spacing: 2px;
}

h2 {
  color: #43a047;
  border-left: 5px solid #1e88e5;
  padding-left: 15px;
}

table th {
  background: linear-gradient(135deg, #1e88e5 0%, #1565c0 100%);
}
```

**✅ PDF agora tem visual mais sofisticado!**

---

## 📈 Caso de Uso 4: Adicionar novo gráfico de tendência

### Cenário:

Você quer adicionar um gráfico de linha mostrando a evolução do lucro ao longo do ano.

### Solução:

Edite `app.py`, adicione na função `generate_charts()` (após linha 178):

```python
# 3. Gráfico: Evolução do Lucro
query_profit = f"""
    SELECT
        strftime('%m', date) as month,
        SUM(CASE WHEN type='REVENUE' THEN amount ELSE 0 END) -
        SUM(CASE WHEN type='EXPENSE' THEN amount ELSE 0 END) as profit
    FROM transactions
    WHERE strftime('%Y', date) = '{year}'
    GROUP BY month
    ORDER BY month
"""

cursor.execute(query_profit)
profit_data = cursor.fetchall()

months_profit = [int(row[0]) for row in profit_data]
profits = [row[1] for row in profit_data]
month_labels_profit = [month_names[m-1] for m in months_profit]

# Plotar gráfico de linha
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(month_labels_profit, profits, marker='o', linewidth=2,
        markersize=8, color='#2ecc71', label='Lucro Mensal')

# Adicionar área preenchida
ax.fill_between(range(len(profits)), profits, alpha=0.3, color='#2ecc71')

# Linha de tendência
z = np.polyfit(range(len(profits)), profits, 1)
p = np.poly1d(z)
ax.plot(month_labels_profit, p(range(len(profits))),
        "--", color='#e74c3c', linewidth=2, label='Tendência')

ax.set_xlabel('Mês', fontsize=12)
ax.set_ylabel('Lucro (R$)', fontsize=12)
ax.set_title(f'Evolução do Lucro - {year}', fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.legend()

# Adicionar valores nos pontos
for i, (month, profit) in enumerate(zip(month_labels_profit, profits)):
    ax.text(i, profit, f'R$ {profit:,.0f}',
            ha='center', va='bottom', fontsize=8)

plt.tight_layout()
chart3_path = output_dir / "profit_trend.png"
plt.savefig(chart3_path, dpi=300, bbox_inches='tight')
plt.close()

# Atualizar o retorno da função
return {
    'monthly_chart': chart1_path,
    'categories_chart': chart2_path,
    'profit_trend_chart': chart3_path,  # NOVO
    'charts_generated': True
}
```

**Adicionar no HTML do PDF (linha ~373):**

```html
<h3>Tendência de Lucro ao Longo do Ano</h3>
<img src="{charts_dir / 'profit_trend.png'}" alt="Tendência de Lucro" />
```

**✅ Novo gráfico de tendência adicionado!**

---

## 🤖 Caso de Uso 5: Ajustar o prompt para mais insights

### Cenário:

Você quer que o relatório inclua análise de sazonalidade e previsões.

### Solução:

Edite `reports/prompt/report_prompt-2.md`, adicione na seção de Insights:

```markdown
#### 5. Insights e Recomendações

Apresente 6-8 insights baseados nos dados:

- Identifique meses com melhor/pior desempenho
- Analise tendências de crescimento
- **NOVO: Identifique padrões sazonais (ex: gastos maiores no fim do ano)**
- **NOVO: Compare primeiro vs segundo semestre**
- Identifique oportunidades de otimização de custos
- Forneça recomendações práticas e acionáveis
- **NOVO: Sugira previsões para os próximos 3 meses baseado nas tendências**
```

**✅ Relatório agora inclui análise sazonal!**

---

## 🔄 Caso de Uso 6: Automatizar geração diária

### Cenário:

Você quer que o relatório seja gerado automaticamente todos os dias às 8h.

### Solução Linux/MacOS (cron):

```bash
# 1. Abrir crontab
crontab -e

# 2. Adicionar linha
0 8 * * * cd /caminho/do/projeto && /caminho/do/venv/bin/python app.py

# 3. Salvar e sair
```

### Solução Windows (Task Scheduler):

```powershell
# Criar tarefa agendada
$action = New-ScheduledTaskAction -Execute "python" -Argument "C:\caminho\do\projeto\app.py" -WorkingDirectory "C:\caminho\do\projeto"
$trigger = New-ScheduledTaskTrigger -Daily -At 8am
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "GerarRelatorioFinanceiro" -Description "Gera relatório financeiro diário"
```

**✅ Relatórios gerados automaticamente!**

---

## 📧 Caso de Uso 7: Enviar relatório por email

### Cenário:

Você quer que o PDF seja enviado automaticamente por email após a geração.

### Solução:

Crie arquivo `send_email.py`:

```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from pathlib import Path

def send_report(pdf_path, recipient_email):
    """Envia relatório por email"""

    # Configuração SMTP (exemplo Gmail)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "seu_email@gmail.com"
    sender_password = "sua_senha_app"  # Use App Password do Gmail

    # Criar mensagem
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = f"Relatório Financeiro - {Path(pdf_path).stem}"

    # Corpo do email
    body = """
    Olá,

    Segue em anexo o relatório financeiro atualizado.

    Este email foi gerado automaticamente.

    Atenciosamente,
    Sistema de Relatórios
    """
    msg.attach(MIMEText(body, 'plain'))

    # Anexar PDF
    with open(pdf_path, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={Path(pdf_path).name}')
        msg.attach(part)

    # Enviar
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)

    print(f"✅ Email enviado para {recipient_email}")

if __name__ == "__main__":
    # Buscar último relatório
    from glob import glob
    pdfs = sorted(glob("reports/financial_report_*.pdf"), reverse=True)
    if pdfs:
        send_report(pdfs[0], "destinatario@empresa.com")
```

**Adicionar em `app.py` após linha 449:**

```python
# Enviar por email (opcional)
try:
    from send_email import send_report
    send_report(pdf_path, "cfo@empresa.com")
    print("📧 Email enviado com sucesso!")
except Exception as e:
    print(f"⚠️  Erro ao enviar email: {e}")
```

**✅ Relatórios enviados automaticamente por email!**

---

## 🔍 Caso de Uso 8: Filtrar por período específico

### Cenário:

Você quer gerar relatório apenas do primeiro trimestre de 2024.

### Solução:

Edite `reports/prompt/report_prompt-2.md`:

```markdown
### Escopo do Relatório:

- **Período**: Primeiro trimestre de 2024 (janeiro a março)
```

**E adicione filtro nas queries do agente:**

```markdown
## FILTROS DE DATA:

- Use WHERE date BETWEEN '2024-01-01' AND '2024-03-31'
- Agrupe apenas pelos meses 01, 02 e 03
```

**✅ Relatório filtrado por trimestre!**

---

## 🎓 Caso de Uso 9: Comparar com ano anterior

### Cenário:

Você tem dados de 2023 e 2024 e quer comparar os anos.

### Solução:

Adicione nova seção no prompt:

```markdown
#### 8. Comparação Ano a Ano (2023 vs 2024)

Crie uma tabela comparando:
| Métrica | 2023 | 2024 | Variação (%) |

- Receita Total
- Despesa Total
- Lucro Líquido
- Margem de Lucro

Calcule o crescimento percentual: ((2024 - 2023) / 2023) \* 100
```

**✅ Análise comparativa entre anos!**

---

## 📊 Caso de Uso 10: Dashboard executivo simples

### Cenário:

Você quer um dashboard interativo básico.

### Solução:

Crie `dashboard.py`:

```python
import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="Dashboard Financeiro", layout="wide")

# Conectar ao banco
conn = sqlite3.connect('data/finance.db')

# KPIs
col1, col2, col3, col4 = st.columns(4)

# Receita Total
receita = pd.read_sql_query(
    "SELECT SUM(amount) FROM transactions WHERE type='REVENUE' AND date LIKE '2024%'",
    conn
).iloc[0, 0]

# Despesa Total
despesa = pd.read_sql_query(
    "SELECT SUM(amount) FROM transactions WHERE type='EXPENSE' AND date LIKE '2024%'",
    conn
).iloc[0, 0]

lucro = receita - despesa
margem = (lucro / receita * 100) if receita > 0 else 0

col1.metric("💰 Receita Total", f"R$ {receita:,.2f}")
col2.metric("💸 Despesa Total", f"R$ {despesa:,.2f}")
col3.metric("📈 Lucro Líquido", f"R$ {lucro:,.2f}")
col4.metric("📊 Margem", f"{margem:.1f}%")

# Gráficos
st.subheader("Evolução Mensal")
df_mensal = pd.read_sql_query("""
    SELECT
        strftime('%m', date) as mes,
        SUM(CASE WHEN type='REVENUE' THEN amount ELSE 0 END) as receita,
        SUM(CASE WHEN type='EXPENSE' THEN amount ELSE 0 END) as despesa
    FROM transactions
    WHERE date LIKE '2024%'
    GROUP BY mes
    ORDER BY mes
""", conn)

st.line_chart(df_mensal.set_index('mes'))

# Categorias
st.subheader("Top Despesas por Categoria")
df_cat = pd.read_sql_query("""
    SELECT category, SUM(amount) as total
    FROM transactions
    WHERE type='EXPENSE' AND date LIKE '2024%'
    GROUP BY category
    ORDER BY total DESC
    LIMIT 5
""", conn)

st.bar_chart(df_cat.set_index('category'))

conn.close()
```

**Executar:**

```bash
pip install streamlit
streamlit run dashboard.py
```

**✅ Dashboard interativo no navegador!**

---

## 🎯 Resumo de Customizações

| O que customizar         | Arquivo                             | Linha aproximada |
| ------------------------ | ----------------------------------- | ---------------- |
| Cores dos gráficos       | `app.py`                            | 108, 157         |
| Estilo do PDF            | `app.py`                            | 261-363          |
| Conteúdo do relatório    | `reports/prompt/report_prompt-2.md` | Todo o arquivo   |
| Modelo LLM               | `app.py`                            | 199              |
| Período de análise       | `reports/prompt/report_prompt-2.md` | 13               |
| Resolução dos gráficos   | `app.py`                            | 134, 177         |
| Adicionar novos gráficos | `app.py`                            | 63-188 (função)  |

---

## 📚 Recursos Adicionais

- 📖 **README.md** - Documentação completa
- 🚀 **QUICKSTART.md** - Instalação em 5 minutos
- 📝 **CHANGELOG.md** - Histórico de mudanças
- 📊 **IMPROVEMENTS_SUMMARY.md** - Resumo das melhorias

---

**🎉 Com esses exemplos, você pode adaptar o sistema para qualquer necessidade!**
