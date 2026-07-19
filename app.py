import streamlit as st
import pandas as pd
import yfinance as yf

# Web page settings
st.set_page_config(page_title="NSE Breakout Scanner", page_icon="📈", layout="wide")

st.title("🔥 NSE All Stocks All-Time High (ATH) Scanner")
st.write("Yeh web-app automatically NSE ke stocks ko scan karke breakout stocks dhundti hai.")

# Scan button
if st.button("🚀 Start Full Market Scan"):
    with st.spinner("NSE Master List download ho rahi hai... Kripya 2-3 minute rukein!"):
        try:
            # NSE ke stocks ki live list download karna
            url = "https://raw.githubusercontent.com/anirbanghoshsbi/NSE-LIST-OF-LISTED-SECURITIES/master/NSE_ALL_STOCKS.csv"
            df_nse = pd.read_csv(url)
            
            tickers = [str(symbol).strip() + ".NS" for symbol in df_nse['SYMBOL'].dropna().unique()]
            
            breakout_stocks = []
            near_ath_stocks = []
            
            # Shuruat me test karne ke liye top 150 stocks scan kar rahe hain
            for ticker in tickers[:150]: 
                try:
                    stock = yf.Ticker(ticker)
                    hist = stock.history(period="max", interval="1mo")
                    
                    if len(hist) < 2:
                        continue
                        
                    current_close = hist['Close'].iloc[-1]
                    past_data = hist.iloc[:-1]
                    if past_data.empty:
                        continue
                    ath = past_data['High'].max()
                    
                    # Breakout Condition
                    if current_close >= ath:
                        breakout_stocks.append({
                            "Stock": ticker.replace(".NS", ""),
                            "Current Price (₹)": round(current_close, 2),
                            "All-Time High (₹)": round(ath, 2),
                            "Status": "🔥 Breakout"
                        })
                    # Near ATH Condition (2%)
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
                st.success("🎉 Scan Poora Ho Gaya!")
                st.dataframe(df_result, use_container_width=True)
            else:
                st.warning("Filhal koi breakout stock nahi mila.")
                
        except Exception as e:
            st.error(f"Kuch dikkat aayi: {e}")
