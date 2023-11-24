import spacy
import json
import random

class SimpleChatBot:
    def __init__(self, intents):
        self.intents = intents

    def get_response(self, user_input):
        doc = nlp(user_input)
        best_match = None
        best_similarity = 0.0

        for intent in self.intents["intents"]:
            #tag_similarity = intent["tag"].lower()
            #similarity_tag = self.calculate_similarity(doc, tag_similarity)
            #print(tag_similarity)
            #print(doc)
            #print(similarity_tag)
            #if similarity_tag > 0.65:
            for pattern in intent["patterns"]:
                similarity = self.calculate_similarity(doc, pattern)
                print(pattern)
                print(similarity)
                if similarity > 0.49 and similarity > best_similarity:
                    best_similarity = similarity
                    print(best_similarity)
                    best_match = intent["responses"]

        if best_match:
            return random.choice(best_match)
        else:
            return "Desculpe, eu não entendi. Pode reformular?"

    def calculate_similarity(self, doc, pattern):
        pattern_tokens = nlp(pattern)
        return max(doc.similarity(pattern_tokens), pattern_tokens.similarity(doc))

# Carregando o modelo do spaCy
nlp = spacy.load("pt_core_news_md")

# Carregando as intenções do arquivo JSON
with open("intents.json") as f:
    intents = json.load(f)

# Inicializando o chatbot
chatbot = SimpleChatBot(intents)

# Exemplo de interação
while True:
    user_input = input("Você: ")
    if user_input.lower() == 'sair':
        break

    response = chatbot.get_response(user_input)
    print(f"ChatBot: {response}")
