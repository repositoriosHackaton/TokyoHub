from flask import Flask, render_template
from flask_socketio import SocketIO, send
import chatbot
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(msg):
    print('Message: ' + msg)
    response = bot_response(msg)  # Función que procesa el mensaje y genera una respuesta
    send(response)

def bot_response(message):
    return chatbot.process_input(message)


if __name__ == '__main__':
    socketio.run(app, debug=True)
