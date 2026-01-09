import streamlit as st
import yfinance as yf
import pandas as pd
from app.database import get_positions

st.title("📁 Portfolio")

positions = get_positions()

if not positions:
    st.info("No positions added yet.")
    st.stop()

rows = []
for p in positions:
    current_price = yf.Ticker(p.ticker).info["regularMarketPrice"]
    value = p.quantity * current_price
    cost = p.quantity * p.purchase_price
    gain = value - cost
    upside = (p.fair_value - current_price) / current_price * 100
    signal = "BUY" if upside > 10 else "HOLD" if upside > 0 else "SELL"

    rows.append({
        "Ticker": p.ticker,
        "Quantity": p.quantity,
        "Purchase Price": p.purchase_price,
        "Fair Value": p.fair_value,
        "Current Price": round(current_price, 2),
        "Value": round(value, 2),
        "Gain/Loss": round(gain, 2),
        "Upside (%)": round(upside, 2),
        "Signal": signal
    })

df = pd.DataFrame(rows)

def highlight_signal(row):
    if row["Signal"] == "BUY":
        return ["background-color: lightgreen"] * len(row)
    elif row["Signal"] == "SELL":
        return ["background-color: lightcoral"] * len(row)
    else:
        return [""] * len(row)

st.dataframe(df.style.apply(highlight_signal, axis=1))
