from dotenv import load_dotenv
from flask import Flask, send_from_directory, session
from flask_session import Session
from flask_socketio import SocketIO, emit

from src.domain.models.chat_message import ChatMessage
from src.features.message_router.router import get_action

load_dotenv()

app = Flask(__name__, static_folder='client/build', static_url_path='/')

app.config['SECRET_KEY'] = 'secret!'
app.config['SESSION_TYPE'] = 'filesystem'
socketio = SocketIO(app)
Session(app)


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


@socketio.on('message')
def handle_message(data):
    message = ChatMessage.load_from_dict(data)

    get_action(message.action_name)(emit=emit, message=message, session=session).execute()

if __name__ == '__main__':
    socketio.run(app, allow_unsafe_werkzeug=True)