import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

print("Aplicação Flask iniciada!")

# URL da API do chatbot
api_url = 'http://127.0.0.1:5000/chat'

# Histórico do chat
chat_history = []

@app.route('/')
def index():
    return render_template('index.html', chat_history=chat_history)

@app.route('/send_message', methods=['POST'])
def send_message():
    user_input = request.form['user_input']
    chatbot_response = get_chatbot_response(user_input)
    chat_history.append({'user_input': user_input, 'chatbot_response': chatbot_response})
    return render_template('index.html', chat_history=chat_history)

def get_chatbot_response(user_input):
    data = {'user_input': user_input}
    response = requests.post(api_url, json=data)
    if response.status_code == 200:
        response_data = response.json()
        return response_data['response']
    else:
        return f"Erro na solicitação: {response.status_code}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5001)
