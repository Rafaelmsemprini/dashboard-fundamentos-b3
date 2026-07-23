# 📊 Painel de Fundamentos B3 & Benchmarking

Aplicação interativa desenvolvida em Python para análise fundamentalista de empresas listadas na bolsa brasileira (B3), permitindo comparação direta de indicadores financeiros por ano de exercício.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)
![Status](https://img.shields.io/badge/Status-Concluído-brightgreen.svg)

---

## 🎯 Funcionalidades

* **Filtros Avançados por Matriz B3:** Busca e seleção hierárquica por Setor, Segmento e Empresa.
* **Diagnóstico Fundamentalista Automático:** Algoritmo que interpreta indicadores (ROE, Margem Líquida, Dividend Yield) e gera análises qualitativas do negócio.
* **Análise Individual & DRE Histórica:** Visualização de DRE (Receita, EBITDA e Lucro) e eficiência operacional ao longo dos anos.
* **Benchmarking & Comparativo Temporal:** Cruzamento do histórico de múltiplos tickers no mesmo gráfico para análise comparativa de tendências.
* **Exportação de Dados:** Download de relatórios completos em formato CSV.

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** Python
- **Interface:** Streamlit
- **Visualização de Dados:** Plotly Express
- **Manipulação de Dados:** Pandas
- **Fonte de Dados:** Yahoo Finance (`yfinance`)

---

## 🚀 Como Executar o Projeto

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/SEU_USUARIO/dashboard-fundamentos-b3.git](https://github.com/SEU_USUARIO/dashboard-fundamentos-b3.git)
   cd dashboard-fundamentos-b3
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Rode a aplicação:**
   ```bash
   streamlit run app.py
   ```