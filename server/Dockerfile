FROM python:3.12

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN python -m spacy download pt_core_news_md

COPY package*.json ./
COPY . .

# Exponha a porta do servidor Flask
EXPOSE 5000

CMD ["python", "server.py"]