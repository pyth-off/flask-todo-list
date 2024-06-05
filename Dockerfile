FROM python:3.6-alpine

# Run commands before changin the user to avoid permission problems
RUN apk update
RUN apk add --no-cache bash
RUN apk add --no-cache nano
RUN apk add --no-cache py-pip
RUN pip install flask gunicorn

ENV FLASK_APP flasky.py
ENV FLASK_CONFIG production

RUN adduser -D flasky
USER flasky

WORKDIR /home/flasky



COPY requirements requirements
RUN python -m venv venv
RUN venv/bin/pip install -r requirements/docker.txt

COPY app app
COPY migrations migrations
COPY flasky.py config.py boot.sh ./

# run-time configuration
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
