from database import add_position, get_positions

import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd

st.title("📈 Portfolio Tracker")

ticker = st.text_input("Enter a stock ticker (e.g., AAPL)")

if ticker:
    ticker_obj = yf.Ticker(ticker)
    hist = ticker_obj.history(period="1y")

    st.write(hist.tail()) 

    fig = px.line(hist, x=hist.index, y="Close", title=f"{ticker} Closing Price")
    st.plotly_chart(fig)


st.subheader("Add to Portfolio")

qty = st.number_input("Quantity", min_value=0.0)
price = st.number_input("Purchase Price", min_value=0.0)
fair_value = st.number_input("DCF Fair Value", min_value=0.0)

if st.button("Add Position"):
    add_position(ticker, qty, price, fair_value)
    st.success(f"Added {ticker} to portfolio")

st.subheader("📊 Current Portfolio")

positions = get_positions()

if positions:
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


else:
    st.info("No positions added yet.")

