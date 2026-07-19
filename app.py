import streamlit as st
import pandas as pd

st.set_page_config(page_title="NSE Multi-Year Breakout Scanner", layout="wide")
st.title("🔥 Bharat Forge Style - Multi-Year Breakout Scanner")

@st.cache_data
def load_all_nse_symbols():
    # Ye link stable hai aur isme 2000+ stocks ki list hai
    url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
    try:
        df = pd.read_csv(url)
        # 'SYMBOL' column ko nikal rahe hain
        symbols = df['SYMBOL'].dropna().unique().tolist()
        return sorted([str(s).strip() for s in symbols if str(s).strip()])
    except Exception as e:
        return ["BHARATFORG", "RELIANCE", "TCS", "INFY"]

all_symbols = load_all_nse_symbols()
st.sidebar.info(f"📊 Total Stocks in Database: {len(all_symbols)}")
