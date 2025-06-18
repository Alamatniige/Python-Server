from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
from pyngrok import ngrok
import time

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/templates/static')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

PUBLIC_URL = None

@app.route('/')
def index():
    return render_template('chat.html')

@socketio.on('connect')
def handle_connect():
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', 'unknown'))
    print(f'✅ Client connected from {client_ip}')
    emit('status', {'msg': 'Connected to chat server!', 'timestamp': time.time()})

@socketio.on('disconnect')
def handle_disconnect():
    print(f'❌ Client disconnected')

@socketio.on('message')
def handle_message(data):
    print(f"📨 Message received: {data}")
    send(data, broadcast=True)

if __name__ == '__main__':
    tunnel = None
    try:
        print("="*60)
        print("🎯 STARTING CHAT SERVER")
        print("="*60)
        ngrok.kill()  # Kill any existing tunnels
        time.sleep(2)
        print("🚀 Creating ngrok tunnel...")
        tunnel = ngrok.connect(5000)
        PUBLIC_URL = tunnel.public_url
        print(f"🌐 Ngrok tunnel created: {PUBLIC_URL}")
        print(f"   🏠 Local URL:     http://localhost:5000")
        print(f"   📊 Ngrok Dashboard: http://localhost:4040")
        print(f"\n📤 SHARE THIS URL WITH OTHERS:\n   {PUBLIC_URL}")
        print("="*60)
        print("🎉 Starting Flask-SocketIO server...")
        print("="*60)
        socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
    finally:
        print("\n🧹 Cleaning up...")
        if tunnel:
            try:
                ngrok.disconnect(tunnel.public_url)
            except:
                pass
        ngrok.kill()
        print("✅ Cleanup complete!")