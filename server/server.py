import spacy
import json
import random
from flask import Flask, request, jsonify, session
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_session import Session

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['JWT_SECRET_KEY'] = 'your-secret-key' 
app.config['SESSION_PERMANENT'] = False
jwt = JWTManager(app)
Session(app)

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
            return random.choice(best_match)
        else:
            return "Desculpe, eu não entendi. Pode reformular?"

    def calculate_similarity(self, doc, pattern):
        pattern_tokens = nlp(pattern)
        return max(doc.similarity(pattern_tokens), pattern_tokens.similarity(doc))


class User:
    def __init__(self, users):
        self.users = users

    def verify_credentials(self, username, password):
        print(f"Verificando credenciais para usuário: {username}")

        user = self.users.get(username)

        if user and user["password"] == password:
            print(f"Credenciais válidas para {username}")
            return user
        else:
            print(f"Credenciais inválidas para {username}")
            return None


@app.route('/login', methods=['POST'])
def login():
    try:
        print("Entrou na rota de login")
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        print(f"Recebido username: {username}, password: {password}")

        # Verifica as credenciais no banco de dados
        user = userStart.verify_credentials(username, password)

        print("Verificou credenciais")

        if user:
            # Gera um token JWT com o identificador do usuário
            access_token = create_access_token(identity=username)
            print(f"Login bem-sucedido para {username}. Token: {access_token}")
            return jsonify(access_token=access_token)
        else:
            print(f"Credenciais inválidas para {username}")
            return jsonify({'error': 'Credenciais inválidas'}), 401
    except Exception as e:
        print(f"Erro durante o login: {str(e)}")
        return jsonify({'error': 'Erro interno durante o login'}), 500


# Carregando o modelo do spaCy
nlp = spacy.load("pt_core_news_md")

# Carregando as intenções do arquivo JSON
with open("intents.json", encoding='utf-8')  as f:
    intents = json.load(f)

# Carregando os usuários do arquivo JSON
with open("users.json", encoding='utf-8') as f:
    users = json.load(f)

# Inicializando o user
userStart = User(users)

# Endpoint para receber mensagens do usuário e retornar respostas do chatbot
@app.route('/chat', methods=['POST'])
@jwt_required()  # Protege este endpoint com autenticação JWT
def chat():
    current_user = get_jwt_identity()
    user_input = request.get_json()['user_input']
    # Use o nome de usuário como parte da chave da sessão para manter instâncias separadas
    chatbot_instance = f"chatbot_{current_user}"
    # Verifica se a instância do chatbot já existe na sessão
    if chatbot_instance not in session:
        # Se não existir, cria uma nova instância do chatbot
        session[chatbot_instance] = SimpleChatBot(intents)
    # Obtém a resposta usando a instância do chatbot específica do usuário
    response = session[chatbot_instance].get_response(user_input)
    return jsonify({'response': response})

# Executando o aplicativo Flask localmente
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)
