import streamlit as st
import plotly.express as px
import pandas as pd
from coletor_fundamentos import buscar_dados_empresa, buscar_comparativo_empresas

# --- BASE DE DADOS DE SETORES E SEGMENTOS (B3) ---
EMPRESAS_B3 = {
    "PETR4": {"nome": "Petrobras", "setor": "Energia", "segmento": "Petróleo, Gás e Biocombustíveis"},
    "VALE3": {"nome": "Vale", "setor": "Materiais Básicos", "segmento": "Mineração"},
    "WEGE3": {"nome": "WEG", "setor": "Bens Industriais", "segmento": "Máquinas e Equipamentos"},
    "ITUB4": {"nome": "Itaú Unibanco", "setor": "Financeiro", "segmento": "Bancos"},
    "BBDC4": {"nome": "Bradesco", "setor": "Financeiro", "segmento": "Bancos"},
    "BBAS3": {"nome": "Banco do Brasil", "setor": "Financeiro", "segmento": "Bancos"},
    "ABEV3": {"nome": "Ambev", "setor": "Consumo não Cíclico", "segmento": "Bebidas"},
    "PRIO3": {"nome": "PRIO", "setor": "Energia", "segmento": "Petróleo, Gás e Biocombustíveis"},
    "RENT3": {"nome": "Localiza", "setor": "Bens Industriais", "segmento": "Aluguel de Carros"},
    "LREN3": {"nome": "Lojas Renner", "setor": "Consumo Cíclico", "segmento": "Comércio / Varejo"},
    "MGLU3": {"nome": "Magazine Luiza", "setor": "Consumo Cíclico", "segmento": "Comércio / Varejo"},
    "EQTL3": {"nome": "Equatorial", "setor": "Utilidade Pública", "segmento": "Energia Elétrica"},
    "RAIL3": {"nome": "Rumo", "setor": "Bens Industriais", "segmento": "Transporte e Logística"},
    "JBSS3": {"nome": "JBS", "setor": "Consumo não Cíclico", "segmento": "Alimentos Processados"},
    "SUZB3": {"nome": "Suzano", "setor": "Materiais Básicos", "segmento": "Papel e Celulose"},
    "GGBR4": {"nome": "Gerdau", "setor": "Materiais Básicos", "segmento": "Siderurgia"},
    "CSAN3": {"nome": "Cosan", "setor": "Energia", "segmento": "Petróleo, Gás e Biocombustíveis"},
    "CPLE6": {"nome": "Copel", "setor": "Utilidade Pública", "segmento": "Energia Elétrica"},
    "EGIE3": {"nome": "Engie", "setor": "Utilidade Pública", "segmento": "Energia Elétrica"},
    "VBBR3": {"nome": "Vibra", "setor": "Energia", "segmento": "Petróleo, Gás e Biocombustíveis"}
}

st.set_page_config(
    page_title="Terminal Fundamentalista B3",
    page_icon="📈",
    layout="wide"
)

# --- MOTOR DE DIAGNÓSTICO FINANCEIRO (O "E DAÍ?") ---
def gerar_diagnostico(roe, margem, dy):
    insights = []
    
    # Análise de Rentabilidade (ROE)
    if roe >= 15:
        insights.append("✅ **Excelente Rentabilidade (ROE):** A empresa gera mais de 15% de retorno sobre o capital próprio, indicando alta eficiência na alocação de recursos.")
    elif roe > 8:
        insights.append("🟡 **Rentabilidade Moderada (ROE):** Retorno razoável, mas alinhado à média de mercado. Vale monitorar a evolução dos custos.")
    else:
        insights.append("⚠️ **Rentabilidade Pressionada (ROE):** ROE abaixo de 8%. O negócio enfrenta dificuldades para entregar margens atrativas aos acionistas.")

    # Análise de Eficiência (Margem Líquida)
    if margem >= 15:
        insights.append("🛡️ **Forte Margem Líquida:** A companhia possui alta proteção operacional e bom poder de precificação frente aos custos.")
    elif margem < 5:
        insights.append("🔻 **Margem Apertada:** Opera com margens estreitas (abaixo de 5%). Qualquer variação nos custos operacionais pode impactar o lucro.")

    # Análise de Proventos (Dividend Yield)
    if dy >= 8:
        insights.append("💰 **Perfil Pagador de Proventos:** Yield expressivo nos últimos 12 meses. Atentar se os pagamentos são recorrentes ou não.")
    elif dy == 0:
        insights.append("🔄 **Foco em Reinvestimento/Crescimento:** Sem histórico recente de proventos relevantes, indicando foco em retenção de caixa ou expansão.")

    return insights

# --- TEMA VISUAL ---
st.markdown("""
    <style>
    div[data-testid="stMetric"] {
        background-color: #1E212B !important;
        padding: 12px;
        border-radius: 8px;
    }
    .stAlert {
        border-left: 4px solid #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📈 Terminal de Análise Fundamentalista & Valuation")
st.caption("Inteligência financeira aplicada: dados históricos, filtros setoriais e diagnósticos automatizados.")

# --- BARRA LATERAL: FILTROS CORPORATIVOS ---
st.sidebar.header("🔍 Filtros de Mercado")

df_meta = pd.DataFrame.from_dict(EMPRESAS_B3, orient='index')

setores_disponiveis = ["Todos"] + sorted(list(df_meta["setor"].unique()))
setor_sel = st.sidebar.selectbox("1. Filtrar por Setor:", setores_disponiveis)

if setor_sel != "Todos":
    df_filtrado = df_meta[df_meta["setor"] == setor_sel]
else:
    df_filtrado = df_meta

segmentos_disponiveis = ["Todos"] + sorted(list(df_filtrado["segmento"].unique()))
segmento_sel = st.sidebar.selectbox("2. Filtrar por Segmento:", segmentos_disponiveis)

if segmento_sel != "Todos":
    df_filtrado = df_filtrado[df_filtrado["segmento"] == segmento_sel]

tickers_filtrados = list(df_filtrado.index)

st.sidebar.divider()
st.sidebar.header("⚙️ Modo de Análise")
modo = st.sidebar.radio("Escolha a Visão:", ["Análise Profunda (Individual)", "⚔️ Benchmarking Temporal"])

# --- MODO 1: ANÁLISE INDIVIDUAL ---
if modo == "Análise Profunda (Individual)":
    ticker_input = st.sidebar.selectbox("3. Selecione a Empresa:", options=tickers_filtrados)
    
    with st.spinner(f"Processando demonstrativos financeiros de {ticker_input}..."):
        df_historico, dy = buscar_dados_empresa(ticker_input)
        
    if df_historico is not None and not df_historico.empty:
        ultimo = df_historico.iloc[-1]
        info_empresa = EMPRESAS_B3.get(ticker_input, {"nome": ticker_input, "setor": "N/A", "segmento": "N/A"})
        
        st.subheader(f"📌 {ticker_input} — {info_empresa['nome']}")
        st.caption(f"**Setor:** {info_empresa['setor']} | **Segmento:** {info_empresa['segmento']}")
        
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("ROE (Último)", f"{ultimo['ROE (%)']}%")
        c2.metric("Margem Líquida", f"{ultimo['Margem Líquida (%)']}%")
        c3.metric("Dividend Yield (12M)", f"{dy}%")
        c4.metric(f"Receita ({ultimo['Ano']})", f"R$ {ultimo['Receita']/1e9:.2f} Bi")
        c5.metric(f"Lucro Líquido ({ultimo['Ano']})", f"R$ {ultimo['Lucro']/1e9:.2f} Bi")
        
        st.divider()
        
        # --- BLOCO DE DIAGNÓSTICO (O "E DAÍ?") ---
        st.markdown("### 🧠 Diagnóstico Financeiro Automático")
        insights = gerar_diagnostico(ultimo['ROE (%)'], ultimo['Margem Líquida (%)'], dy)
        
        texto_diag = "\n\n".join(insights)
        st.info(f"**Interpretação do Painel para {ticker_input}:**\n\n{texto_diag}")
        
        st.divider()
        
        # --- HISTÓRICO VISUAL ---
        st.markdown("### 📜 Evolução Histórica (Linha do Tempo)")
        
        tab1, tab2 = st.tabs(["📊 DRE (Receita x Lucro x EBITDA)", "📈 Eficiência Operacional (ROE e Margem)"])
        
        with tab1:
            df_plot = df_historico.copy()
            df_plot['Receita (Mi)'] = df_plot['Receita'] / 1e6
            df_plot['EBITDA (Mi)'] = df_plot['EBITDA'] / 1e6
            df_plot['Lucro (Mi)'] = df_plot['Lucro'] / 1e6
            
            fig_dre = px.bar(
                df_plot, x='Ano', y=['Receita (Mi)', 'EBITDA (Mi)', 'Lucro (Mi)'],
                barmode='group', title="DRE Histórica (R$ Milhões)", template="plotly_dark",
                color_discrete_sequence=['#1f77b4', '#2ca02c', '#ff7f0e']
            )
            st.plotly_chart(fig_dre, use_container_width=True)
            
        with tab2:
            fig_ef = px.line(
                df_historico, x='Ano', y=['ROE (%)', 'Margem Líquida (%)'], markers=True,
                title="Histórico de ROE vs Margem Líquida (%)", template="plotly_dark",
                color_discrete_sequence=['#d62728', '#9467bd']
            )
            st.plotly_chart(fig_ef, use_container_width=True)
            
        # Exportação
        csv_ind = df_historico.to_csv(index=False, sep=';').encode('utf-8-sig')
        st.download_button(f"📥 Baixar Relatório Completo de {ticker_input} (.CSV)", csv_ind, f"analise_{ticker_input}.csv", "text/csv")

# --- MODO 2: BENCHMARKING (COMPARATIVO TEMPORAL) ---
else:
    st.subheader("⚔️ Comparativo Temporal Multi-Empresas")
    
    empresas_selecionadas = st.sidebar.multiselect(
        "Selecione as Empresas para Comparar:",
        options=tickers_filtrados,
        default=tickers_filtrados[:3] if len(tickers_filtrados) >= 3 else tickers_filtrados
    )
    
    if len(empresas_selecionadas) < 2:
        st.warning("Selecione pelo menos duas empresas para comparar.")
    else:
        dados_empresas = []
        with st.spinner("Compilando histórico comparativo..."):
            for t in empresas_selecionadas:
                df_h, _ = buscar_dados_empresa(t)
                if df_h is not None and not df_h.empty:
                    df_h['Empresa'] = t
                    dados_empresas.append(df_h)
                    
        if dados_empresas:
            df_comp_hist = pd.concat(dados_empresas)
            
            st.markdown("#### Evolução Comparativa do ROE (%) ao longo dos anos")
            fig_comp_roe = px.line(
                df_comp_hist, x='Ano', y='ROE (%)', color='Empresa', markers=True,
                title="Histórico Comparativo de ROE (%)", template="plotly_dark"
            )
            st.plotly_chart(fig_comp_roe, use_container_width=True)
            
            st.markdown("#### Evolução Comparativa da Margem Líquida (%)")
            fig_comp_margem = px.line(
                df_comp_hist, x='Ano', y='Margem Líquida (%)', color='Empresa', markers=True,
                title="Histórico Comparativo de Margem Líquida (%)", template="plotly_dark"
            )
            st.plotly_chart(fig_comp_margem, use_container_width=True)

# Rodapé
st.sidebar.divider()
st.sidebar.markdown("""
    **Desenvolvido por:**  
    🔗 [GitHub](https://github.com/Rafaelmsemprini) | 💼 [LinkedIn](https://www.linkedin.com/in/rafael-moret-semprini-088b582b8/)
""")