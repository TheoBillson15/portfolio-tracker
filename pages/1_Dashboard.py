import streamlit as st
from components.sidebar import render_sidebar

page = render_sidebar()

if page == "Home":
    st.stop()



import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
from database import get_positions

st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
    .dashboard-bg {
        background-color: #f2f2f7;
        padding: 20px;
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📊 Dashboard Overview")

positions = get_positions()

if not positions:
    st.info("No positions yet. Add some in the 'Add Position' page.")
    st.stop()

# Convert to DataFrame
rows = []
for p in positions:
    current_price = yf.Ticker(p.ticker).info["regularMarketPrice"]
    value = p.quantity * current_price
    rows.append({
        "Ticker": p.ticker,
        "Quantity": p.quantity,
        "Current Price": current_price,
        "Value": value
    })

df = pd.DataFrame(rows)

# Total portfolio value
total_value = df["Value"].sum()

st.subheader(f"💰 Total Portfolio Value: ${total_value:,.2f}")

# Allocation pie chart
fig_alloc = px.pie(
    df,
    names="Ticker",
    values="Value",
    title="Portfolio Allocation",
    hole=0.4
)

# Price movement chart
price_data = {}
for p in positions:
    hist = yf.Ticker(p.ticker).history(period="1mo")["Close"]
    price_data[p.ticker] = hist

price_df = pd.DataFrame(price_data)

fig_prices = px.line(
    price_df,
    title="📈 30-Day Price Movement"
)

# Layout
col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='dashboard-bg'>", unsafe_allow_html=True)
    st.plotly_chart(fig_alloc, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='dashboard-bg'>", unsafe_allow_html=True)
    st.plotly_chart(fig_prices, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
