FROM python:3.12

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN python -m spacy download pt_core_news_md
RUN pip install gunicorn

COPY package*.json ./
COPY . .

CMD gunicorn --bind 0.0.0.0:5000 server:app