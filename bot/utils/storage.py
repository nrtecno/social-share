import json
import os

# In-memory storage
user_data = {}
link_cache = {}
victim_data_store = {}
user_username_cache = {}

# File for active users
ACTIVE_USERS_FILE = "active_users.json"

def load_active_users():
    if os.path.exists(ACTIVE_USERS_FILE):
        try:
            with open(ACTIVE_USERS_FILE, 'r') as f:
                return set(json.load(f))
        except:
            return set()
    return set()

def save_active_users(users_set):
    try:
        with open(ACTIVE_USERS_FILE, 'w') as f:
            json.dump(list(users_set), f)
    except Exception as e:
        print(f"Save error: {e}")

active_users = load_active_users()
