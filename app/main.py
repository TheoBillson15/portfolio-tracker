import streamlit as st
from app.auth import authenticate, get_role
import streamlit as st

st.set_page_config(page_title="Portfolio Tracker", page_icon="📈", layout="wide")

# -------------------------
# BEAUTIFUL LOGIN UI
# -------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None

if not st.session_state.logged_in:
    st.markdown(
        """
        <style>
        .login-container {
            max-width: 380px;
            margin: 80px auto;
            padding: 30px;
            border-radius: 12px;
            background: #ffffff;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            text-align: center;
            font-family: 'Segoe UI', sans-serif;
        }
        .login-title {
            font-size: 28px;
            font-weight: 600;
            margin-bottom: 10px;
        }
        .login-subtitle {
            font-size: 14px;
            color: #666;
            margin-bottom: 25px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='login-container'>", unsafe_allow_html=True)
    st.markdown("<div class='login-title'>📈 Portfolio Tracker</div>", unsafe_allow_html=True)
    st.markdown("<div class='login-subtitle'>Welcome back — please sign in</div>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Invalid username or password")

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# -------------------------
# SIDEBAR (logout + role)
# -------------------------
role = get_role(st.session_state.username)

st.sidebar.title("📁 Navigation")
st.sidebar.write(f"Logged in as **{st.session_state.username}** ({role})")

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.username = None
    st.rerun()

# -------------------------
# PAGE ROUTING
# -------------------------
st.sidebar.write("---")

page = st.sidebar.radio(
    "Go to:",
    [
        "Dashboard",
        "Add Position",
        "Portfolio",
        "Admin Panel" if role == "admin" else None
    ],
)

# -------------------------
# LOAD PAGES
# -------------------------
if page == "Dashboard":
    st.switch_page("pages/1_Dashboard.py")

elif page == "Add Position":
    st.switch_page("pages/2_Add_Position.py")

elif page == "Portfolio":
    st.switch_page("pages/3_Portfolio.py")

elif page == "Admin Panel":
    st.switch_page("pages/4_Admin.py")
