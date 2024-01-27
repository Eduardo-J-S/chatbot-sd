
# Projeto de Sistemas Distribuídos

Este é um projeto de sistemas distribuídos composto por uma aplicação de cliente em Flask (Python) e um servidor em Flask também (Python), ambos contidos em contêineres Docker, e um serviço de proxy Nginx para facilitar a comunicação entre o cliente e o servidor.

## Cliente

O cliente é responsável por fornecer uma interface web interativa para os usuários interagirem com o ChatBot. O script `client.py` utiliza o framework Flask para criar um servidor web que se comunica com o servidor do ChatBot e exibe as mensagens em uma página HTML simples. O Dockerfile permite a fácil construção e execução do cliente em um contêiner isolado.

## Servidor

O servidor é responsável por processar as solicitações do cliente e interagir com um ChatBot simples. O script server.py utiliza Flask para criar um servidor web que recebe mensagens do cliente, processa essas mensagens com base em padrões definidos no arquivo intents.json e retorna as respostas correspondentes. O Dockerfile facilita a construção e execução do servidor em um contêiner isolado.

## Nginx (Proxy)

O serviço Nginx é utilizado como um proxy para facilitar a comunicação entre o cliente e o servidor.

## Requisitos Gerais

- Docker
- Docker Compose

### Observação Importante

As configurações padrão no arquivo docker-compose.yml assumem que as portas 80, 5000 e 5001 em seu host não estão em uso por outros serviços. Se essas portas estiverem ocupadas, você pode precisar ajustar as configurações no arquivo docker-compose.yml.

## Instruções de Uso

1. Certifique-se de ter o Docker instalado.
2. Execute o seguinte comando na raiz do projeto para criar e iniciar os serviços:

```
docker-compose up
```
3. Abra o navegador e acesse http://localhost:5001 para interagir com o ChatBot.
4. O servidor estará disponível em http://localhost:5000 para receber as solicitações do cliente.
5. O Nginx estará disponível em http://localhost e encaminhará as solicitações para o servidor Flask na porta 5000.
