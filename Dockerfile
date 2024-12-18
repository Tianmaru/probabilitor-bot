FROM python:3-alpine

WORKDIR /app

COPY probabilitor_bot.py .
COPY requirements.txt .

RUN pip install -r requirements.txt
RUN rm requirements.txt

CMD [ "python3", "probabilitor_bot.py" ]