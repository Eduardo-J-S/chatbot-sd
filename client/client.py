import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# URL da API do chatbot
api_url = 'https://chatbot-sd-server.onrender.com'

# Histórico do chat
chat_history = []

# Token de autenticação
token = None

@app.route('/login', methods=['GET'])
def show_login():
    return render_template('login.html')

@app.route('/')
def index():
    return render_template('index.html', chat_history=chat_history)

# No client.py, altere a função login
@app.route('/login', methods=['POST'])
def login():
    global token
    username = request.form['username']
    password = request.form['password']

    data = {'username': username, 'password': password}
    response = requests.post(f'{api_url}/login', json=data, timeout=30)

    if response.status_code == 200:
        token = response.json()['access_token']
        return 'Login realizado com sucesso.'
    else:
        try:
            # Tente fazer o parsing da resposta como JSON apenas se a requisição for bem-sucedida
            response_data = response.json()
            return f'Erro no login: {response.status_code} - {response_data}'
        except:
            # Se ocorrer um erro ao fazer o parsing, retorne uma mensagem genérica de erro
            return f'Erro no login: {response.status_code} - Resposta inválida'

@app.route('/send_message', methods=['POST'])
def send_message():
    global token
    if not token:
        return 'Faça o login primeiro.'

    user_input = request.form['user_input']
    headers = {'Authorization': f'Bearer {token}'}
    data = {'user_input': user_input}
    response = requests.post(f'{api_url}/chat', json=data, headers=headers)
    
    if response.status_code == 200:
        response_data = response.json()
        chat_history.append({'user_input': user_input, 'chatbot_response': response_data['response']})
        return render_template('index.html', chat_history=chat_history)
    else:
        return f"Erro na solicitação: {response.status_code}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5001)
