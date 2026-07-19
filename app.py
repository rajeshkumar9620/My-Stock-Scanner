import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="NSE Multi-Year Breakout Scanner", page_icon="🔥", layout="wide")
st.title("🔥 Bharat Forge Style - Multi-Year Breakout Scanner")

@st.cache_data
def load_all_nse_symbols():
    try:
        url = "https://raw.githubusercontent.com/shanghaobeta/nse-stocks-list/main/nse_stocks.csv"
        df = pd.read_csv(url)
        if 'Symbol' in df.columns:
            symbols = df['Symbol'].dropna().unique().tolist()
        else:
            symbols = df.iloc[:, 0].dropna().unique().tolist()
        return sorted([str(s).strip() for s in symbols if str(s).strip()])
    except:
        return ["BHARATFORG", "RELIANCE", "TCS", "INFY", "TATAMOTORS", "SBIN"]

all_symbols = load_all_nse_symbols()
st.sidebar.info(f"📊 Total Stocks in Database: {len(all_symbols)}")
