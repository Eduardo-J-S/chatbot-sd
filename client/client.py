import requests
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

# URL da API do chatbot
api_url = 'http://127.0.0.1:5000'

# Histórico do chat
chat_history = []

@app.route('/')
def index():
    return render_template('index.html', chat_history=chat_history)

@socketio.on('message')
def handle_message(data):
    chat_history.append({'user_input': data['user_input'], 'chatbot_response': data['response']})
    socketio.emit('update_chat', {'chat_history': chat_history})

@socketio.on('connect')
def handle_connect():
    socketio.emit('update_chat', {'chat_history': chat_history})

# Adicione esta rota para lidar com mensagens enviadas pelo cliente
@app.route('/send_message', methods=['POST'])
def send_message():
    user_input = request.form.get('user_input')

    # Faz uma requisição interna para obter a resposta do chatbot
    chatbot_response = get_chatbot_response(user_input)

    # Adiciona a mensagem do usuário e a resposta do chatbot ao histórico do chat
    chat_history.append({'user_input': user_input, 'chatbot_response': 'ChatBot: ' + chatbot_response})
    return render_template('index.html', chat_history=chat_history)

def get_chatbot_response(user_input):
    # Faz uma requisição interna para o endpoint /chat
    response = requests.post(f'{api_url}/chat', json={'user_input': user_input})
    # Obtém a resposta do chatbot a partir da resposta da requisição
    chatbot_response = response.json().get('response', '')
    return chatbot_response

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001)
