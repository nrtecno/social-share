import json
import os

# In-memory storage
user_data = {}
link_cache = {}
victim_data_store = {}
user_username_cache = {}

# ===== PERSISTENT FILE STORAGE =====
DATA_DIR = "/tmp/data"
os.makedirs(DATA_DIR, exist_ok=True)

REDIRECT_FILE = os.path.join(DATA_DIR, "redirects.json")
PHOTO_FILE = os.path.join(DATA_DIR, "photos.json")
ACTIVE_USERS_FILE = os.path.join(DATA_DIR, "active_users.json")


def load_persistent_data():
    global victim_data_store
    if os.path.exists(REDIRECT_FILE):
        try:
            with open(REDIRECT_FILE, 'r') as f:
                redirects = json.load(f)
                for k, v in redirects.items():
                    victim_data_store[k] = v
                print(f"✅ Loaded {len(redirects)} redirects")
        except Exception as e:
            print(f"Load redirects error: {e}")

    if os.path.exists(PHOTO_FILE):
        try:
            with open(PHOTO_FILE, 'r') as f:
                photos = json.load(f)
                for k, v in photos.items():
                    victim_data_store[k] = v
                print(f"✅ Loaded {len(photos)} photos")
        except Exception as e:
            print(f"Load photos error: {e}")


def save_redirect(victim_id, url):
    key = f"redirect_{victim_id}"
    victim_data_store[key] = url
    try:
        redirects = {}
        if os.path.exists(REDIRECT_FILE):
            with open(REDIRECT_FILE, 'r') as f:
                redirects = json.load(f)
        redirects[key] = url
        with open(REDIRECT_FILE, 'w') as f:
            json.dump(redirects, f)
        print(f"✅ REDIRECT SAVED: {key} = {url}")
    except Exception as e:
        print(f"Save redirect error: {e}")


def save_photo(victim_id, url):
    key = f"photo_{victim_id}"
    victim_data_store[key] = url
    try:
        photos = {}
        if os.path.exists(PHOTO_FILE):
            with open(PHOTO_FILE, 'r') as f:
                photos = json.load(f)
        photos[key] = url
        with open(PHOTO_FILE, 'w') as f:
            json.dump(photos, f)
        print(f"✅ PHOTO SAVED: {key}")
    except Exception as e:
        print(f"Save photo error: {e}")


def get_redirect(victim_id):
    key = f"redirect_{victim_id}"
    if key in victim_data_store:
        return victim_data_store[key]
    try:
        if os.path.exists(REDIRECT_FILE):
            with open(REDIRECT_FILE, 'r') as f:
                redirects = json.load(f)
            if key in redirects:
                victim_data_store[key] = redirects[key]
                return redirects[key]
    except Exception as e:
        print(f"Get redirect error: {e}")
    return None


def get_photo(victim_id):
    key = f"photo_{victim_id}"
    if key in victim_data_store:
        return victim_data_store[key]
    try:
        if os.path.exists(PHOTO_FILE):
            with open(PHOTO_FILE, 'r') as f:
                photos = json.load(f)
            if key in photos:
                victim_data_store[key] = photos[key]
                return photos[key]
    except Exception as e:
        print(f"Get photo error: {e}")
    return None


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


load_persistent_data()
active_users = load_active_users()
