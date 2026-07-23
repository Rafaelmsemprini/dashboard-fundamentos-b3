import streamlit as st
import plotly.express as px
import pandas as pd
from coletor_fundamentos import buscar_dados_empresa, buscar_comparativo_empresas

EMPRESAS_B3 = [
    "PETR4", "VALE3", "WEGE3", "ITUB4", "BBDC4", "BBAS3", "ABEV3", 
    "PRIO3", "RENT3", "LREN3", "MGLU3", "EQTL3", "RAIL3", "JBSS3", 
    "SUZB3", "GGBR4", "CSAN3", "CPLE6", "EGIE3", "VBBR3"
]

st.set_page_config(
    page_title="Fundamentos B3 — Dashboard & Comparador",
    page_icon="📊",
    layout="wide"
)

# --- BARRA LATERAL (TEMAS & CONFIGURAÇÕES) ---
st.sidebar.header("🎨 Aparência & Tema")

tema_escolhido = st.sidebar.selectbox(
    "Escolha o tema do painel:",
    options=["Escuro (Dark Mode)", "Claro (Light Mode)", "Azul Finance"],
    index=0
)

# Definição das paletas de cores
if tema_escolhido == "Claro (Light Mode)":
    bg_color = "#FFFFFF"
    sec_bg_color = "#F0F2F6"
    text_color = "#31333F"
    card_bg = "#EAEAEA"
    plotly_template = "plotly_white"
elif tema_escolhido == "Azul Finance":
    bg_color = "#0E1E25"
    sec_bg_color = "#050E12"
    text_color = "#E0E6ED"
    card_bg = "#162C35"
    plotly_template = "plotly_dark"
else:  # Escuro Padrão
    bg_color = "#0E1117"
    sec_bg_color = "#1E212B"
    text_color = "#FFFFFF"
    card_bg = "#262730"
    plotly_template = "plotly_dark"

st.markdown(f"""
    <style>
    :root {{
        --background-color: {bg_color} !important;
        --secondary-background-color: {sec_bg_color} !important;
        --text-color: {text_color} !important;
    }}
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}
    [data-testid="stSidebar"] {{
        background-color: {sec_bg_color};
        color: {text_color};
    }}
    [data-testid="stSidebar"] * {{
        color: {text_color} !important;
    }}
    div[data-testid="stMetric"] {{
        background-color: {card_bg} !important;
        padding: 12px;
        border-radius: 8px;
    }}
    div[data-testid="stMetric"] * {{
        color: {text_color} !important;
    }}
    </style>
""", unsafe_allow_html=True)

st.title("📊 Painel de Fundamentos — Empresas da B3")
st.caption("Análise fundamentalista e benchmarking interativo com dados oficiais de mercado.")

st.sidebar.divider()
st.sidebar.header("🔍 Configurações do Painel")

aba_selecionada = st.sidebar.radio(
    "Escolha o Modo de Análise:",
    ["Análise Individual", "⚔️ Comparador (Benchmarking)"]
)

# --- ABA 1: ANÁLISE INDIVIDUAL ---
if aba_selecionada == "Análise Individual":
    ticker_input = st.sidebar.selectbox(
        "Selecione ou digite a Empresa:",
        options=EMPRESAS_B3,
        index=0
    )
    
    with st.spinner(f"Coletando demonstrativos financeiros de {ticker_input}..."):
        df_historico, dy = buscar_dados_empresa(ticker_input)
        
    if df_historico is not None and not df_historico.empty:
        ultimo = df_historico.iloc[-1]
        
        st.subheader(f"📌 Resumo Executivo — {ticker_input.upper()}")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Dividend Yield (12M)", f"{dy}%")
        col2.metric("ROE (Último Ano)", f"{ultimo['ROE (%)']}%")
        col3.metric("Margem Líquida", f"{ultimo['Margem Líquida (%)']}%")
        col4.metric(f"Receita ({ultimo['Ano']})", f"R$ {ultimo['Receita']/1e9:.2f} Bi")
        col5.metric(f"Lucro Líquido ({ultimo['Ano']})", f"R$ {ultimo['Lucro']/1e9:.2f} Bi")
        
        st.divider()
        
        tab_dre, tab_eficiencia, tab_tabela = st.tabs([
            "💰 DRE (Receita x Lucro x EBITDA)", 
            "🎯 Eficiência (ROE e Margem)", 
            "📄 Tabela Completa"
        ])
        
        with tab_dre:
            df_plot = df_historico.copy()
            df_plot['Receita (Mi)'] = df_plot['Receita'] / 1e6
            df_plot['EBITDA (Mi)'] = df_plot['EBITDA'] / 1e6
            df_plot['Lucro (Mi)'] = df_plot['Lucro'] / 1e6
            
            fig_dre = px.bar(
                df_plot,
                x='Ano',
                y=['Receita (Mi)', 'EBITDA (Mi)', 'Lucro (Mi)'],
                barmode='group',
                title="Evolução da Receita, EBITDA e Lucro Líquido (em R$ Milhões)",
                labels={'value': 'R$ Milhões', 'variable': 'Indicador'},
                template=plotly_template,
                color_discrete_sequence=['#1f77b4', '#2ca02c', '#ff7f0e']
            )
            fig_dre.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_dre, use_container_width=True)
            
        with tab_eficiencia:
            fig_ef = px.line(
                df_historico,
                x='Ano',
                y=['ROE (%)', 'Margem Líquida (%)'],
                markers=True,
                title="Histórico de Rentabilidade e Margem (%)",
                labels={'value': 'Percentual (%)', 'variable': 'Métrica'},
                template=plotly_template,
                color_discrete_sequence=['#d62728', '#9467bd']
            )
            fig_ef.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_ef, use_container_width=True)
            
        with tab_tabela:
            st.dataframe(df_historico, use_container_width=True)
            
            # Botão de Exportação CSV
            csv_ind = df_historico.to_csv(index=False, sep=';').encode('utf-8-sig')
            st.download_button(
                label=f"📥 Baixar Dados de {ticker_input} (.CSV)",
                data=csv_ind,
                file_name=f"fundamentos_{ticker_input.lower()}.csv",
                mime="text/csv"
            )
    else:
        st.error(f"Não foi possível carregar os dados para {ticker_input}.")

# --- ABA 2: BENCHMARKING (COMPARADOR) ---
else:
    st.subheader("⚔️ Comparativo Direto entre Empresas")
    
    empresas_selecionadas = st.sidebar.multiselect(
        "Selecione as Empresas para comparar:",
        options=EMPRESAS_B3,
        default=["PETR4", "PRIO3", "VALE3"]
    )
    
    ano_selecionado = st.sidebar.selectbox(
        "Selecione o Ano de Referência:",
        options=["Mais Recente (2025)", "2024", "2023", "2022", "2021"],
        index=0
    )
    
    ano_filtro = None if "Mais Recente" in ano_selecionado else ano_selecionado
    
    if len(empresas_selecionadas) < 2:
        st.warning("Selecione pelo menos duas empresas para realizar o comparativo.")
    else:
        with st.spinner("Buscando e filtrando indicadores comparativos..."):
            df_comp = buscar_comparativo_empresas(empresas_selecionadas, ano_alvo=ano_filtro)
            
        if not df_comp.empty:
            st.dataframe(df_comp, use_container_width=True)
            
            # Botão de Exportação CSV
            csv_comp = df_comp.to_csv(index=False, sep=';').encode('utf-8-sig')
            st.download_button(
                label="📥 Baixar Tabela Comparativa (.CSV)",
                data=csv_comp,
                file_name="comparativo_empresas_b3.csv",
                mime="text/csv"
            )
            
            st.divider()
            col_g1, col_g2 = st.columns(2)
            
            with col_g1:
                fig_roe = px.bar(
                    df_comp,
                    x='Empresa',
                    y='ROE (%)',
                    color='Empresa',
                    title=f"Comparativo de ROE (%) — Ano {df_comp['Ano Referência'].iloc[0]}",
                    template=plotly_template,
                    text_auto=True
                )
                fig_roe.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_roe, use_container_width=True)
                
            with col_g2:
                fig_dy = px.bar(
                    df_comp,
                    x='Empresa',
                    y='Dividend Yield (%)',
                    color='Empresa',
                    title="Comparativo de Dividend Yield (%)",
                    template=plotly_template,
                    text_auto=True
                )
                fig_dy.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_dy, use_container_width=True)
                
            fig_margem = px.bar(
                df_comp,
                x='Empresa',
                y='Margem Líquida (%)',
                color='Empresa',
                title=f"Comparativo de Margem Líquida (%) — Ano {df_comp['Ano Referência'].iloc[0]}",
                template=plotly_template,
                text_auto=True
            )
            fig_margem.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_margem, use_container_width=True)
        else:
            st.error("Erro ao buscar dados das empresas selecionadas.")

# --- RODAPÉ DA SIDEBAR (CRÉDITOS & CONTATO) ---
st.sidebar.divider()
st.sidebar.markdown("""
    **Desenvolvido por:**
    
    🔗 [GitHub](https://github.com/Rafaelmsemprini)  
    💼 [LinkedIn](https://www.linkedin.com/in/rafael-moret-semprini-088b582b8/)
""")