import streamlit as st
from app.database import add_position
from app.auth import get_role

st.title("➕ Add Position")

role = get_role(st.session_state.username)

if role == "viewer" or role == "analyst":
    st.error("You do not have permission to add positions.")
    st.stop()

ticker = st.text_input("Ticker (e.g., AAPL)")
qty = st.number_input("Quantity", min_value=0.0)
price = st.number_input("Purchase Price", min_value=0.0)
fair_value = st.number_input("DCF Fair Value", min_value=0.0)

if st.button("Add Position"):
    add_position(ticker, qty, price, fair_value)
    st.success(f"Added {ticker} to portfolio")
