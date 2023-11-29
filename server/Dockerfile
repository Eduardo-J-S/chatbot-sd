FROM python:3.12

WORKDIR /app

COPY package*.json ./

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install spacy==3.7.2 flask
RUN python -m spacy download pt_core_news_md

COPY . .

# Exponha a porta do servidor Flask
EXPOSE 5000

CMD ["python", "server.py"]