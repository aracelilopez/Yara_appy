FROM python:3.7.1

ENV FLASK_APP "app.py"

RUN mkdir /app
WORKDIR /app
ADD . /app

RUN pip install --upgrade pip && \
    pip install flask yara-python flask_sqlalchemy

EXPOSE 5000

CMD flask run --host=0.0.0.0