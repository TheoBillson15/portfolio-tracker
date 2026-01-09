import streamlit as st
from auth import add_user, delete_user, load_users, get_role

st.title("🔧 Admin Panel")

role = get_role(st.session_state.username)

if role != "admin":
    st.error("You do not have permission to access this page.")
    st.stop()

st.subheader("Add New User")

new_user = st.text_input("Username")
new_pass = st.text_input("Password", type="password")
new_role = st.selectbox("Role", ["admin", "analyst", "user", "viewer"])

if st.button("Create User"):
    add_user(new_user, new_pass, new_role)
    st.success(f"User '{new_user}' created.")

st.subheader("Delete User")

users = load_users()
user_to_delete = st.selectbox("Select user", list(users.keys()))

if st.button("Delete User"):
    delete_user(user_to_delete)
    st.success(f"User '{user_to_delete}' deleted.")
