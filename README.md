# 📊 Painel de Fundamentos B3 & Benchmarking

Aplicação interativa desenvolvida em Python para análise fundamentalista de empresas listadas na bolsa brasileira (B3), permitindo comparação direta de indicadores financeiros por ano de exercício.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)
![Status](https://img.shields.io/badge/Status-Concluído-brightgreen.svg)

---

## 🎯 Funcionalidades

- **Análise Individual:** DRE (Receita, EBITDA e Lucro), rentabilidade (ROE) e margens históricas por empresa.
- **Comparador (Benchmarking):** Seleção múltipla de tickers com filtro por ano de referência.
- **Temas Customizáveis:** Alternância dinâmica de modo visual (Dark, Light e Azul Finance).
- **Dados em Tempo Real:** Coleta automatizada via `yfinance`.

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