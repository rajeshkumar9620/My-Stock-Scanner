import streamlit as st
import pandas as pd

st.set_page_config(page_title="NSE Multi-Year Breakout Scanner", layout="wide")
st.title("🔥 Bharat Forge Style - Multi-Year Breakout Scanner")

@st.cache_data
def load_all_nse_symbols():
    url = "https://raw.githubusercontent.com/shanghaobeta/nse-stocks-list/main/nse_stocks.csv"
    try:
        df = pd.read_csv(url)
        # Agar column 'Symbol' hai to wo lelo, nahi to pehla column lelo
        if 'Symbol' in df.columns:
            symbols = df['Symbol'].dropna().unique().tolist()
        else:
            symbols = df.iloc[:, 0].dropna().unique().tolist()
        return [str(s).strip() for s in symbols if str(s).strip()]
    except Exception as e:
        return [f"Error: {str(e)}"]

all_symbols = load_all_nse_symbols()
st.sidebar.info(f"📊 Total Stocks in Database: {len(all_symbols)}")

# Debugging ke liye list dikha do
st.write("List check:", all_symbols[:10])
