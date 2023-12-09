import requests
from flask import Flask, render_template, request, make_response, session
import uuid

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta' 

print("Aplicação Flask iniciada!")

api_url = 'http://server:5000'

chat_sessions = {}

@app.route('/')
def index():
    session_id = session.get('session_id') or str(uuid.uuid4())
    session['session_id'] = session_id

    print("Session ID:", session_id)
    content = render_template('index.html', chat_history=chat_sessions.get(session_id, {'chat_history': []})['chat_history'], session_id=session_id)
    
    response = make_response(content)
    
    return response

@app.route('/send_message', methods=['POST'])
def send_message():
    user_input = request.form['user_input']
    session_id = session.get('session_id')
    chatbot_response = get_chatbot_response(session_id, user_input)
    
    chat_history = chat_sessions.get(session_id, {'chat_history': []})['chat_history']
    chat_history.append({'user_input': user_input, 'chatbot_response': chatbot_response})
    chat_sessions[session_id] = {'chat_history': chat_history}
    
    return render_template('index.html', chat_history=chat_history, session_id=session_id)

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