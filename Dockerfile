FROM python:3.8-alpine

ENV FLASK_APP blog.py
ENV FLASK_CONFIG docker
ENV DOCKER_DATABASE_URL mysql+mysqlconnector://cawakowa:cawakowa@mysql/data
ENV SECRET_KEY 58d40f777aff4d8d96df97223c74d217

RUN apk update && apk add alpine-sdk gcc python3-dev libffi-dev openssl-dev

RUN adduser -D cawakowa
USER cawakowa
WORKDIR /home/cawakowa

COPY requirements requirements
RUN python -m venv venv
RUN pip install --upgrade pip \
    && venv/bin/pip install -r requirements/docker.txt

COPY app app
COPY migrations migrations
COPY blog.py config.py boot.sh ./

# run-time configuration
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]