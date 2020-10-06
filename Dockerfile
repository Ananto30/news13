FROM python:3.7.3-slim

WORKDIR /user/src

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .
COPY ./gunicorn_starter.sh ./

EXPOSE 8000
RUN chmod +x ./gunicorn_starter.sh

ENTRYPOINT ["./gunicorn_starter.sh"]