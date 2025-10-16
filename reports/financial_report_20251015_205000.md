# Relatório Executivo
## Período Alvo
O período alvo para este relatório é o ano de 2024.

## KPIs
Os KPIs principais para este relatório são:

* Receita Total: R$ 127.820,00
* Despesa Total: R$ -127.820,00

## Análises
Abaixo, está apresentada a análise da receita e despesa por mês:

| Data | Receita | Despesa |
| --- | --- | --- |
| 2024-01-05 | R$ 52.000,00 | R$ -52.000,00 |
| 2024-01-10 | R$ 28.000,00 | R$ -28.000,00 |
| 2024-01-12 | R$ 3.000,00 | R$ -3.000,00 |
| 2024-01-20 | R$ 6.000,00 | R$ -6.000,00 |
| 2024-01-25 | R$ 2.500,00 | R$ -2.500,00 |

Abaixo, está apresentada a análise das 3 categorias de despesa com maior valor:

| Categoria | Despesa Total |
| --- | --- |
| Operacional | R$ -84.600,00 |
| Marketing | R$ -37.400,00 |
| Impostos | R$ -30.700,00 |

## Insights
Abaixo, estão apresentados 3-5 insights que explicam os principais movimentos e recomendações práticas:

* A receita total do ano é de R$ 127.820,00, enquanto a despesa total é de R$ -127.820,00, o que indica um resultado negativo para o ano.
* A categoria de despesa com maior valor é a Operacional, com R$ -84.600,00.
* A categoria de despesa com menor valor é a Impostos, com R$ -30.700,00.
* É recomendável reduzir as despesas operacionais e marketing para melhorar o resultado financeiro.
* É recomendável aumentar a receita para melhorar o resultado financeiro.

## SQL Utilizados
```sql
SELECT SUM(amount) AS receita_total, SUM(-amount) AS despesa_total FROM transactions WHERE date LIKE '2024-%';

SELECT date, SUM(amount) AS receita, SUM(-amount) AS despesa FROM transactions WHERE date LIKE '2024-%' GROUP BY date LIMIT 5;

SELECT category, SUM(-amount) AS despesa_total FROM transactions WHERE date LIKE '2024-%' GROUP BY category ORDER BY despesa_total DESC LIMIT 3;
```