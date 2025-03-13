import os

from dotenv import load_dotenv
load_dotenv()

from flask import Flask, send_from_directory, session
from flask_session import Session
from flask_socketio import SocketIO, emit

from src.domain.models.chat_message import ChatMessage
from src.domain.repositories.chroma_repository import ChromaRepository
from src.domain.services.llms.prompt_guard import is_appropriate
from src.domain.services.message_router.router import get_action
from src.intents.error_intent import ErrorAction

app = Flask(__name__, static_folder='client/build', static_url_path='/')

app.config['SECRET_KEY'] = 'secret!'
app.config['SESSION_TYPE'] = 'filesystem'
socketio = SocketIO(app)
Session(app)

chroma_db = ChromaRepository()

current_dir = os.path.dirname(os.path.abspath(__file__))
documents_path = os.path.join(current_dir, "documents")

chroma_db.upsert(documents_path)


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


@socketio.on('message')
def handle_message(data):
    message = ChatMessage.load_from_dict(data)

    is_appropriate_prompt = is_appropriate(message)

    if not is_appropriate_prompt:
        message = ChatMessage.new_bot_message("I'm sorry, I can't answer that. Please try again.")
        ErrorAction(emit=emit, message=message, session=session).execute()
    else:
        get_action(message.action_name)(emit=emit, message=message, session=session).execute()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8897, allow_unsafe_werkzeug=True)