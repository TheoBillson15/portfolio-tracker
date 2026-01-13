import streamlit as st
from components.sidebar import render_sidebar

page = render_sidebar()
if page == "Home":
    st.stop()

import yfinance as yf
import pandas as pd
from database import get_positions

st.title("📁 Portfolio")

# -----------------------------
# CACHED HELPERS
# -----------------------------
@st.cache_data(ttl=300)
def get_price(ticker):
    try:
        t = yf.Ticker(ticker)
        return t.fast_info.get("lastPrice", None)
    except Exception:
        return None

# -----------------------------
# LOAD POSITIONS
# -----------------------------
positions = get_positions()

if not positions:
    st.info("No positions added yet.")
    st.stop()

# -----------------------------
# BUILD TABLE
# -----------------------------
rows = []
for p in positions:
    price = get_price(p.ticker)

    if price is None:
        st.warning(f"Could not fetch price for {p.ticker}.")
        continue

    value = p.quantity * price
    cost = p.quantity * p.purchase_price
    gain = value - cost
    upside = (p.fair_value - price) / price * 100
    signal = "BUY" if upside > 10 else "HOLD" if upside > 0 else "SELL"

    rows.append({
        "Ticker": p.ticker,
        "Quantity": p.quantity,
        "Purchase Price": p.purchase_price,
        "Fair Value": p.fair_value,
        "Current Price": round(price, 2),
        "Value": round(value, 2),
        "Gain/Loss": round(gain, 2),
        "Upside (%)": round(upside, 2),
        "Signal": signal
    })

df = pd.DataFrame(rows)

# -----------------------------
# HIGHLIGHT SIGNALS
# -----------------------------
def highlight_signal(row):
    if row["Signal"] == "BUY":
        return ["background-color: lightgreen"] * len(row)
    elif row["Signal"] == "SELL":
        return ["background-color: lightcoral"] * len(row)
    else:
        return [""] * len(row)

st.dataframe(df.style.apply(highlight_signal, axis=1))
