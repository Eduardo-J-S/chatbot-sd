from flask import Flask, request, jsonify
import spacy
import json
import random
import re

app = Flask(__name__)

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
                    print(text)
                    print(similarity)
                    if similarity > 0.53 and similarity > best_similarity_tag:
                        best_similarity_tag = similarity
                        best_match_tag = intent
                print('--------------------------------------------')
        
        
        if best_match_tag:
            print("Melhor correspondência de tag:", best_match_tag)
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
    
    def encontrar_resposta_por_tags(self, pergunta, intents):
        respostas = []
        # Percorra cada entrada de pergunta-resposta no JSON
        for intent in intents:
            # Converta as tags da entrada atual para minúsculas
            tags = intent["tag"]

            # Verifique se pelo menos uma tag está presente na pergunta
            if any(tag in pergunta for tag in tags):
                respostas.extend(intent["responses"])

        return respostas

# Carregando o modelo do spaCy
nlp = spacy.load("pt_core_news_md")

# Carregando as intenções do arquivo JSON
with open("intents.json", encoding='utf-8')  as f:
    intents = json.load(f)

# Inicializando o chatbot
chatbot = SimpleChatBot(intents)

# Endpoint para receber mensagens do usuário e retornar respostas do chatbot
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data['user_input']
    response = chatbot.get_response(user_input)
    return jsonify({'response': response})

# Executando o aplicativo Flask localmente
if __name__ == '__main__':
    app.run(debug=True, port=5000)
