# EDA · Vitaliza grupo 08 (artefato de Tecnologia, semana 5)

Análise exploratória da saída de assinantes: carrega, limpa e visualiza os dados, mostra os padrões ligados à saída e dá a base empírica da segmentação.

## O que tem aqui

| Arquivo | O que é |
|---|---|
| `notebooks/eda_vitaliza.ipynb` | O caderno da EDA, já executado: dados e limpeza → churn → padrões e correlações → segmentos → limitações |
| `saidas/eda/*.png` | Os 10 gráficos do caderno, prontos para o *Customer Segmentation Report* |
| `src/eda_graficos.py` | Estilo único dos gráficos (paleta, títulos, formato brasileiro de números) |
| `src/eda_segmentos_cortes.py` | Aplica a segmentação de referência aos cortes de 30/04, 31/05 e 30/06 para medir a saída por segmento |

| Gráfico | Mensagem |
|---|---|
| `01_limpeza_linhas_removidas.png` | A limpeza remove pouco (0,75% dos treinos no máximo); o resto é corrigido ou marcado |
| `02_churn_mensal.png` | O churn subiu em 2026 e chegou a 8,1% em abril |
| `03_churn_mensal_por_plano.png` | Depois do reajuste, o churn do mensal sobe (9,0% → 13,0%); o do anual não (2,9% → 3,0%) |
| `04_saida_por_caracteristica.png` | Renovação desligada (31,5% × 8,0%) e plano mensal (19,3% × 6,6%) separam mais |
| `05_consistencia_entre_cortes.png` | Os mesmos grupos de risco aparecem em 30/04, 31/05 e 30/06 |
| `06_uso_saiu_x_ficou.png` | Quem sai treina menos (mediana 18 × 24 treinos em 90 dias) e abre menos o app |
| `07_correlacao_com_saida.png` | Recência e queda de uso andam com a saída; correlações fracas, uma a uma |
| `08_correlacao_entre_variaveis.png` | As variáveis de uso são redundantes entre si (por isso o VIF na segmentação) |
| `09_segmentos_tamanho_e_saida.png` | Esfriando sai 18,6% em 60 dias, contra 10,6% dos engajados |
| `10_perfil_dos_segmentos.png` | O que define cada um dos 4 segmentos |

## Como reproduzir

O caderno lê `dados/brutos/` (só leitura) e as tabelas de `dados/processados/`, que ficam fora do Git. Com o `.venv` ativo e o `requirements.txt` instalado, gere as tabelas nesta ordem (a partir da raiz do projeto):

```
python src/padronizar_onboarding.py
python src/marcas_completude_onboarding.py
python src/base_conta_onboarding.py
python src/preparar_atividades.py
python src/limpar_outliers_atividades.py
python src/contas_treinos.py
python src/churn_mensal.py
python src/base_assinantes.py
python src/base_master.py
python src/segmentacao_kmeans.py --k 4
python src/segmentacao_ampliada.py --k 3 --k-final 4
python src/eda_segmentos_cortes.py
```

Esses scripts reescrevem os relatórios de `saidas/*.md`; os números não mudam. Depois, rode o caderno inteiro:

```
python -m jupyter nbconvert --to notebook --execute --inplace notebooks/eda_vitaliza.ipynb
```

O caderno confere o SHA-256 de `dados/brutos/` no início e no fim e falha se algum arquivo bruto mudar.

## Conferências feitas

- As linhas dos 12 arquivos batem com o dicionário de dados.
- Churn mensal: média de 5,6% em 2025, 6,6% em jan–set/2026, abril/2026 = 1.154 ÷ 14.237 = 8,1% (iguais ao case).
- A soma do churn por plano (mensal + anual) é igual à série oficial, mês a mês.
- Saída em 60 dias: 14.119 / 14.102 / 14.059 ativos em 30/04 / 31/05 / 30/06, com 12,63% / 12,08% / 11,91% de saída (iguais a `saidas/base_assinantes.md`).
- Segmentos: o modelo de referência foi reproduzido em 14.753 de 14.753 contas; a saída por segmento em 30/06 (9,9% / 10,6% / 18,4% / 16,1%) é a mesma de `saidas/segmentacao_ampliada.md`.
- Nenhuma decisão de limpeza nova: o caderno usa as 47 decisões do `decisoes.md`.
