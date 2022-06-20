FROM python:3

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN mkdir -p /opt/src/worker
RUN mkdir -p /opt/src/common
WORKDIR /opt/src

COPY worker ./worker
COPY common ./common

RUN pip install -r ./common/requirements.txt

ENTRYPOINT ['python', '/opt/src/worker/app.py']
