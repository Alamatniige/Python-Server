from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/templates/static')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

users = {}

@app.route('/')
def index():
    return render_template('chat.html')

@socketio.on('join')
def handle_join(username):
    users[request.sid] = username

@socketio.on('message')
def handle_message(data):
    user = users.get(request.sid, 'Anonymous')
    msg = data.get('msg', '')
    emit('message', {'user': user, 'msg': msg}, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    users.pop(request.sid, None)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)