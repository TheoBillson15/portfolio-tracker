import json
import hashlib
from pathlib import Path

USERS_FILE = Path(__file__).parent / "users.json"

# -------------------------
# LOAD & SAVE USERS
# -------------------------
def load_users():
    if not USERS_FILE.exists():
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

# -------------------------
# PASSWORD HASHING
# -------------------------
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# -------------------------
# AUTHENTICATION
# -------------------------
def authenticate(username, password):
    users = load_users()
    if username in users:
        hashed = hash_password(password)
        return hashed == users[username]["password"]
    return False

# -------------------------
# ROLES
# -------------------------
def get_role(username):
    users = load_users()
    return users.get(username, {}).get("role", "viewer")

# -------------------------
# USER MANAGEMENT
# -------------------------
def add_user(username, password, role="user"):
    users = load_users()
    users[username] = {
        "password": hash_password(password),
        "role": role
    }
    save_users(users)

def delete_user(username):
    users = load_users()
    if username in users:
        del users[username]
        save_users(users)
