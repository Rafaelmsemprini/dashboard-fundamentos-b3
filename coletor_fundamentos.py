import yfinance as yf
import pandas as pd

def tratar_ticker(ticker_codigo):
    ticker = ticker_codigo.strip().upper()
    return f"{ticker}.SA" if not ticker.endswith(".SA") else ticker

def buscar_dados_empresa(ticker_codigo):
    ticker_busca = tratar_ticker(ticker_codigo)
    empresa = yf.Ticker(ticker_busca)
    
    try:
        dre = empresa.financials
        balanco = empresa.balance_sheet
        
        if dre.empty or balanco.empty:
            return None, None
            
        dados_historicos = []
        
        for data in dre.columns:
            ano = data.strftime('%Y')
            
            receita = dre.loc['Total Revenue', data] if 'Total Revenue' in dre.index else 0
            lucro = dre.loc['Net Income', data] if 'Net Income' in dre.index else 0
            ebitda = dre.loc['EBITDA', data] if 'EBITDA' in dre.index else 0
            patrimonio = balanco.loc['Stockholders Equity', data] if 'Stockholders Equity' in balanco.index else 0
            
            margem_liquida = (lucro / receita * 100) if receita != 0 else 0
            roe = (lucro / patrimonio * 100) if patrimonio != 0 else 0
            
            dados_historicos.append({
                'Ano': ano,
                'Receita': receita,
                'Lucro': lucro,
                'EBITDA': ebitda,
                'Margem Líquida (%)': round(margem_liquida, 2),
                'ROE (%)': round(roe, 2)
            })
            
        df_historico = pd.DataFrame(dados_historicos).sort_values('Ano').reset_index(drop=True)
        
        info_geral = empresa.info
        dy = info_geral.get('dividendYield', 0)
        
        if dy:
            dy_percentual = round(dy, 2) if dy > 1 else round(dy * 100, 2)
            if dy_percentual > 100:
                dy_percentual = round(dy_percentual / 100, 2)
        else:
            dy_percentual = 0.0
        
        return df_historico, dy_percentual

    except Exception as e:
        print(f"Erro ao processar dados de {ticker_codigo}: {e}")
        return None, None


def buscar_comparativo_empresas(lista_tickers, ano_alvo=None):
    """
    Busca os dados e permite filtrar por um ano específico do histórico (ex: '2024').
    """
    resumo_comparativo = []
    
    for t in lista_tickers:
        df, dy = buscar_dados_empresa(t)
        if df is not None and not df.empty:
            if ano_alvo and str(ano_alvo) in df['Ano'].astype(str).values:
                registro = df[df['Ano'].astype(str) == str(ano_alvo)].iloc[0]
            else:
                registro = df.iloc[-1]
                
            resumo_comparativo.append({
                'Empresa': t.strip().upper().replace('.SA', ''),
                'Ano Referência': registro['Ano'],
                'Receita (R$ Mi)': round(registro['Receita'] / 1e6, 2),
                'Lucro Líquido (R$ Mi)': round(registro['Lucro'] / 1e6, 2),
                'EBITDA (R$ Mi)': round(registro['EBITDA'] / 1e6, 2),
                'Margem Líquida (%)': registro['Margem Líquida (%)'],
                'ROE (%)': registro['ROE (%)'],
                'Dividend Yield (%)': dy
            })
            
    return pd.DataFrame(resumo_comparativo)