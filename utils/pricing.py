import streamlit as st
import yfinance as yf

@st.cache_data(ttl=300)
def get_price(ticker: str):
    try:
        t = yf.Ticker(ticker)
        return t.fast_info.get("lastPrice", None)
    except Exception:
        return None

