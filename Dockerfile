
FROM node:14.3.0-alpine as build
WORKDIR /usr/src
COPY web-app/package.json web-app/package.json
COPY web-app/package-lock.json web-app/package-lock.json

WORKDIR /usr/src/web-app
RUN npm ci --silent
COPY web-app/src src
COPY web-app/rollup.config.js rollup.config.js
RUN npm run build
COPY web-app/public public


FROM python:3.7.3-slim

WORKDIR /usr/src

COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY --from=build /usr/src/web-app/public /usr/src/web-app/public

COPY app app
COPY gunicorn_starter.sh .

EXPOSE 5000
RUN chmod +x gunicorn_starter.sh

ENTRYPOINT ["./gunicorn_starter.sh"]