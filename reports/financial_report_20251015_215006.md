## Resumo Executivo
- Receita Total: R$ 763.500,00
- Despesa Total: R$ 514.700,00
- Lucro Líquido: R$ 248.800,00
- Margem de Lucro: 32,56%

## Análise Mensal
| Mês | Receita (R$) | Despesa (R$) | Lucro (R$) | Margem (%) |
| --- | --- | --- | --- | --- |
| Janeiro | R$ 52.000,00 |  |  |  |
| Fevereiro | R$ 61.000,00 |  |  |  |
| Março | R$ 58.000,00 |  |  |  |
| Abril | R$ 64.000,00 |  |  |  |
| Maio | R$ 72.000,00 |  |  |  |
| Junho | R$ 56.000,00 |  |  |  |
| Julho | R$ 60.000,00 |  |  |  |
| Agosto | R$ 67.500,00 |  |  |  |
| Setembro | R$ 59.000,00 |  |  |  |
| Outubro | R$ 70.500,00 |  |  |  |
| Novembro | R$ 68.500,00 |  |  |  |
| Dezembro | R$ 75.000,00 |  |  |  |

## Top 5 Categorias de Despesa
| Posição | Categoria | Total (R$) | % do Total |
| --- | --- | --- | --- |
| 1 | Folha | R$ 362.000,00 | 70,42% |
| 2 | Operacional | R$ 84.600,00 | 16,45% |
| 3 | Marketing | R$ 37.400,00 | 7,28% |
| 4 | Impostos | R$ 30.700,00 | 5,97% |

## Análise por Conta
Não foi possível realizar a análise por conta devido à falta de informações sobre o tipo de conta.

## Insights e Recomendações
- O mês de maio apresentou a maior receita, enquanto o mês de janeiro apresentou a menor receita.
- A categoria "Folha" apresentou o maior valor de despesa, correspondendo a 70,42% do total de despesas.
- A empresa pode considerar otimizar os custos da categoria "Folha" para aumentar a margem de lucro.
- A empresa pode considerar investir em marketing para aumentar a receita.

## Referências aos Gráficos
Foram gerados gráficos visuais complementares para ilustrar a evolução mensal da receita e despesa, bem como a distribuição de despesas por categoria.

## Consultas SQL Utilizadas
```sql
SELECT SUM(amount) as "receita_total" 
FROM transactions 
WHERE type='REVENUE' AND date LIKE '2024%';

SELECT SUM(amount) as "despesa_total" 
FROM transactions 
WHERE type='EXPENSE' AND date LIKE '2024%';

SELECT 
    strftime('%m', date) AS "mes", 
    SUM(amount) AS "total" 
FROM 
    transactions 
WHERE 
    type = 'REVENUE' 
    AND date LIKE '2024%' 
GROUP BY 
    strftime('%m', date);

SELECT "category", SUM("amount") as "total" 
FROM "transactions" 
WHERE "type" = 'EXPENSE' 
AND "date" LIKE '2024%' 
GROUP BY "category" 
ORDER BY "total" DESC 
LIMIT 5;
```