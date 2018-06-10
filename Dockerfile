FROM python:3-alpine

ADD probabilitor_bot.py /
ADD requirements.txt /

RUN pip install -r requirements.txt
RUN rm requirements.txt

CMD [ "python", "./probabilitor_bot.py" ]