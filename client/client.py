import requests
from flask import Flask, render_template, request, jsonify
import uuid
from flask import make_response

app = Flask(__name__)

print("Aplicação Flask iniciada!")

# URL da API do chatbot
api_url = 'http://localhost:61543'

# Dicionário para armazenar instâncias individuais de chatbot e histórico por sessão
chat_sessions = {}

@app.route('/')
def index():
    # Gera um identificador de sessão para o usuário
    session_id = request.cookies.get('session_id')
    if session_id is None:
        session_id = str(uuid.uuid4())
        chat_sessions[session_id] = {'chat_history': []}

    content = render_template('index.html', chat_history=chat_sessions[session_id]['chat_history'], session_id=session_id)
    
    # Define o cookie para a sessão
    response = make_response(content)
    response.set_cookie('session_id', session_id)
    
    return response

@app.route('/send_message', methods=['POST'])
def send_message():
    user_input = request.form['user_input']
    session_id = request.cookies.get('session_id')
    chatbot_response = get_chatbot_response(session_id, user_input)
    chat_sessions[session_id]['chat_history'].append({'user_input': user_input, 'chatbot_response': chatbot_response})
    return render_template('index.html', chat_history=chat_sessions[session_id]['chat_history'], session_id=session_id)

def get_chatbot_response(session_id, user_input):
    data = {'user_input': user_input, 'session_id': session_id}
    response = requests.post(api_url, json=data)
    if response.status_code == 200:
        response_data = response.json()
        return response_data['response']
    else:
        return f"Erro na solicitação: {response.status_code}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)
