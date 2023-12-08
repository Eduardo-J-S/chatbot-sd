import spacy
import json
import random
from flask import Flask, request, jsonify
from flask_cors import CORS
import socket

app = Flask(__name__)
CORS(app)

# Carregando o modelo do spaCy
nlp = spacy.load("pt_core_news_md")

# Carregando as intenções do arquivo JSON
with open("intents.json", encoding='utf-8') as f:
    intents = json.load(f)

class SimpleChatBot:
    def __init__(self, intents):
        self.intents = intents
    
    def get_response(self, user_input):
        doc = nlp(user_input)
        best_match = None
        best_similarity = 0.0
        best_match_tag = None
        best_similarity_tag = 0.0

        for intent in self.intents["intents"]:
            for tag in intent["tag"]:
                for text in doc:
                    similarity = self.calculate_similarity(text, tag)
                    if similarity > 0.53 and similarity > best_similarity_tag:
                        best_similarity_tag = similarity
                        best_match_tag = intent
        
        if best_match_tag:
            pass
        else:
            return "Desculpe, eu não entendi. Pode reformular?"

        for pattern in best_match_tag["patterns"]:
            similarity = self.calculate_similarity(doc, pattern)
            if similarity > 0.49 and similarity > best_similarity:
                best_similarity = similarity
                best_match = best_match_tag["responses"]    

        if best_match:
            return random.choice(best_match) + f"Container ID: {socket.gethostname()}"
        else:
            return "Desculpe, eu não entendi. Pode reformular?"

    def calculate_similarity(self, doc, pattern):
        pattern_tokens = nlp(pattern)
        return max(doc.similarity(pattern_tokens), pattern_tokens.similarity(doc))

# Dicionário para armazenar instâncias individuais de chatbot e histórico por sessão
chat_sessions = {}

# Endpoint para receber mensagens do usuário e retornar respostas do chatbot
@app.route('/', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data['user_input']
    session_id = data['session_id']

    # Verifica se já existe uma instância de chatbot para a sessão
    if session_id not in chat_sessions:
        chat_sessions[session_id] = {'chatbot': SimpleChatBot(intents), 'chat_history': []}

    chatbot = chat_sessions[session_id]['chatbot']
    response = chatbot.get_response(user_input)

    # Atualiza o histórico da sessão
    chat_sessions[session_id]['chat_history'].append({'user_input': user_input, 'chatbot_response': response})

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
