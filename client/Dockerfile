# Use uma imagem base do Python
FROM python:3.12

# Defina o diretório de trabalho como /app
WORKDIR /app

# Copie o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt requirements.txt

# Instale as dependências
RUN pip install -r requirements.txt

# Copie o conteúdo do diretório atual para o diretório de trabalho
COPY . .

# Exponha a porta 5001
#EXPOSE 5001

# Inicie a aplicação Flask quando o contêiner for iniciado
CMD ["python", "client.py"]
