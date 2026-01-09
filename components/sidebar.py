import streamlit as st
from auth import get_role

def render_sidebar():
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.switch_page("main")

    role = get_role(st.session_state.username)

    st.sidebar.title("📁 Navigation")
    st.sidebar.write(f"Logged in as **{st.session_state.username}** ({role})")
    st.sidebar.write("---")

    pages = ["Dashboard", "Add Position", "Portfolio"]
    if role == "admin":
        pages.append("Admin Panel")

    page = st.sidebar.radio("Go to:", pages)

    st.sidebar.write("---")

    if st.sidebar.button("🚪 Logout"):
        st.session_state.clear()
        st.session_state["logged_out_message"] = True
        st.switch_page("main")

    return page
