import streamlit as st
import pandas as pd
import yfinance as yf

# Web page settings
st.set_page_config(page_title="NSE All Stocks ATH Scanner", page_icon="📈", layout="wide")

st.title("🔥 NSE All Stocks All-Time High (ATH) Scanner")
st.write("Yeh web-app automatically NSE ke maximum available stocks ko scan karke breakout aur near-ATH stocks dhundti hai.")

# Solid dynamically generated or comprehensive list of major NSE stocks to scan
# Isme humne maximum active aur bade NSE stocks daal diye hain jo yfinance par available hain
ALL_NSE_TICKERS = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "BHARTIARTL.NS", "ICICIBANK.NS", 
    "INFY.NS", "SBI.NS", "ITC.NS", "LTIM.NS", "HINDUNILVR.NS", "LT.NS", 
    "BAJFINANCE.NS", "HCLTECH.NS", "MARUTI.NS", "SUNPHARMA.NS", "ADANIENT.NS", 
    "TATAMOTORS.NS", "AXISBANK.NS", "NTPC.NS", "ONGC.NS", "POWERGRID.NS", 
    "COALINDIA.NS", "TITAN.NS", "TATASTEEL.NS", "JIOFIN.NS", "M&M.NS", 
    "ULTRACEMCO.NS", "BAJAJFINSV.NS", "ADANIPORTS.NS", "ASIANPAINT.NS", 
    "WIPRO.NS", "HINDALCO.NS", "JSWSTEEL.NS", "GRASIM.NS", "NESTLEIND.NS", 
    "TECHM.NS", "ADANIGREEN.NS", "ADANIPOWER.NS", "INDUSINDBK.NS", "CIPLA.NS", 
    "DRREDDY.NS", "SBILIFE.NS", "BPCL.NS", "HDFCLIFE.NS", "EICHERMOT.NS", 
    "HEROMOTOCO.NS", "DIVISLAB.NS", "APOLLOHOSP.NS", "BRITANNIA.NS", "BAJAJ-AUTO.NS",
    "TRENT.NS", "BEL.NS", "HAL.NS", "ZOMATO.NS", "VBL.NS", "DLF.NS", "PFC.NS",
    "RECLTD.NS", "IRFC.NS", "BSE.NS", "JINDALSTEL.NS", "SHRIRAMFIN.NS", "TATACONSUM.NS",
    "VEDL", "AMBUJACEM.NS", "GMRINFRA.NS", "GAIL.NS", "TATAELXSI.NS", "PNB.NS",
    "BANKBARODA.NS", "IOC.NS", "TATACOMM.NS", "HAVELLS.NS", "PIDILITIND.NS",
    "SIEMENS.NS", "ABB.NS", "GODREJCP.NS", "DABUR.NS", "MARICO.NS", "COLPAL.NS",
    "OBEROIRLTY.NS", "PHOENIXLTD.NS", "ASHOKLEY.NS", "MRF.NS", "BALKRISIND.NS",
    "TVSMOTOR.NS", "BOSCHLTD.NS", "AUBANK.NS", "FEDERALBNK.NS", "IDFCFIRSTB.NS",
    "L&TFH.NS", "TATACHEM.NS", "SAIL.NS", "NMDC.NS", "NATIONALUM.NS", "JUBLFOOD.NS",
    "PAGEIND.NS", "METROPOLIS.NS", "LALPATHLAB.NS", "GLENMARK.NS", "LUPIN.NS"
]

# Scan button
if st.button("🚀 Start Full Market Scan"):
    with st.spinner("NSE Stocks scan ho rahe hain... Isme 1-2 minute lag sakte hain..."):
        try:
            breakout_stocks = []
            near_ath_stocks = []
            
            for ticker in ALL_NSE_TICKERS: 
                try:
                    stock = yf.Ticker(ticker)
                    # Fetch monthly data for stable ATH calculation
                    hist = stock.history(period="max", interval="1mo")
                    
                    if len(hist) < 2:
                        continue
                        
                    current_close = hist['Close'].iloc[-1]
                    past_data = hist.iloc[:-1]
                    if past_data.empty:
                        continue
                    ath = past_data['High'].max()
                    
                    # Breakout Condition (Current price crossed or at ATH)
                    if current_close >= ath:
                        breakout_stocks.append({
                            "Stock": ticker.replace(".NS", ""),
                            "Current Price (₹)": round(current_close, 2),
                            "All-Time High (₹)": round(ath, 2),
                            "Status": "🔥 Breakout"
                        })
                    # Near ATH Condition (within 2% of breaking high)
                    elif current_close >= (ath * 0.98):
                        near_ath_stocks.append({
                            "Stock": ticker.replace(".NS", ""),
                            "Current Price (₹)": round(current_close, 2),
                            "All-Time High (₹)": round(ath, 2),
                            "Status": "👀 Near ATH"
                        })
                except:
                    continue
            
            final_list = breakout_stocks + near_ath_stocks
            
            if final_list:
                df_result = pd.DataFrame(final_list)
                st.success(f"🎉 Scan Poora Ho Gaya! Total {len(df_result)} Breakout/Near-ATH Stocks mile.")
                st.dataframe(df_result, use_container_width=True)
            else:
                st.warning("Filhal market me koi breakout ya Near ATH nahi mila.")
                
        except Exception as e:
            st.error(f"Kuch dikkat aayi: {e}")
