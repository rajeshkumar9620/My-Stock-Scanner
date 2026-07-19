import streamlit as st
import pandas as pd
import yfinance as yf

# Page setup
st.set_page_config(page_title="NSE Multi-Year Breakout Scanner", page_icon="🔥", layout="wide")

st.title("🔥 Bharat Forge Style - Multi-Year Breakout Scanner")
st.write("Yeh scanner poore 2,000+ NSE stocks ko check karta hai aur sirf unhe dikhata hai jo apne All-Time High/Multi-Year High ko tod kar upar nikal chuke hain.")

# 1. Poore 2000+ Stocks ki List load karna
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

st.sidebar.header("⚙️ Scanner Settings")
st.sidebar.info(f"📊 Total Stocks in Database: {len(all_symbols)}")

buffer_pct = st.sidebar.slider("ATH se kitne paas ya upar hona chahiye? (%)", min_value=0, max_value=5, value=1)

# Scan Button
if st.button("🚀 Start Full 2000+ Market Scan"):
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    breakout_stocks = []
    total_to_scan = len(all_symbols)
    
    status_text.write("🔄 Poore NSE market ka Multi-Year data scan ho raha hai... Please wait...")
    
    for i, sym in enumerate(all_symbols):
        if i % 50 == 0:
            progress_bar.progress(i / total_to_scan)
            
        ticker = f"{sym}.NS"
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="max") 
            
            if hist.empty or len(hist) < 200:
                continue
                
            current_price = hist['Close'].iloc[-1]
            past_data = hist.iloc[:-1]
            all_time_high = past_data['High'].max()
            
            # Bharat Forge Breakout Condition
            if current_price >= (all_time_high * (1 - buffer_pct/100)):
                breakout_stocks.append({
                    "Symbol Name": sym,
                    "Live Price (₹)": round(current_price, 2),
                    "All-Time High (₹)": round(all_time_high, 2),
                    "Distance from ATH": f"{round(((current_price - all_time_high)/all_time_high)*100, 2)}%",
                    "Status": "🔥 Multi-Year Breakout" if current_price >= all_time_high else "👀 Hovering Near ATH"
                })
        except:
            continue
            
    progress_bar.progress(1.0)
    status_text.empty()
    
    if breakout_stocks:
        df_breakout = pd.DataFrame(breakout_stocks)
        st.success(f"🎉 Scan Complete! Pure market me se {len(df_breakout)} stocks mile jo Bharat Forge jaise chart bana rahe hain:")
        st.dataframe(df_breakout, use_container_width=True, height=600)
    else:
        st.warning("Filhal market me koi bhi stock is condition ko match nahi kar raha hai.")
