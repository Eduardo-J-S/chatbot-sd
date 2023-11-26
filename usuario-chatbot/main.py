import requests

# URL da API do chatbot
api_url = 'http://127.0.0.1:5000/chat' 

# Exemplo de interação com o chatbot via API
while True:
    user_input = input("Você: ")
    if user_input.lower() == 'sair':
        break

    # Enviar pergunta para a API
    data = {'user_input': user_input}
    response = requests.post(api_url, json=data)

    # Verificar se a solicitação foi bem-sucedida
    if response.status_code == 200:
        response_data = response.json()
        chatbot_response = response_data['response']
        print(f"ChatBot: {chatbot_response}")
    else:
        print(f"Erro na solicitação: {response.status_code}")
