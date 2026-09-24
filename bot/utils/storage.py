import json
import os

# In-memory storage
user_data = {}
link_cache = {}
victim_data_store = {}

# File for active users
ACTIVE_USERS_FILE = "active_users.json"

def load_active_users():
    """Load active users from file"""
    if os.path.exists(ACTIVE_USERS_FILE):
        try:
            with open(ACTIVE_USERS_FILE, 'r') as f:
                data = json.load(f)
                return set(data)
        except:
            return set()
    return set()

def save_active_users(users_set):
    """Save active users to file"""
    try:
        with open(ACTIVE_USERS_FILE, 'w') as f:
            json.dump(list(users_set), f)
    except Exception as e:
        print(f"Save active users error: {e}")

# Load active users on startup
active_users = load_active_users()
