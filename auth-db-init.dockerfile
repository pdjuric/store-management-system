FROM python:3

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN mkdir -p /opt/src/auth
RUN mkdir -p /opt/src/common
WORKDIR /opt/src

COPY auth ./auth
COPY common ./common

ENV FLASK_APP=migrate.py

RUN pip install -r ./common/requirements.txt
