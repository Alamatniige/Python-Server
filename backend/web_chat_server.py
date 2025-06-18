from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
import time

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/templates/static')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

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
    print("="*60)
    print("🎯 STARTING CHAT SERVER (LOCAL)")
    print("="*60)
    print(f"   🏠 Local URL:     http://localhost:5000")
    print("="*60)
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)