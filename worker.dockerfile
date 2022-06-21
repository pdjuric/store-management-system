FROM python:3

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN mkdir -p /opt/src/common
WORKDIR /opt/src

COPY app/worker.py ./worker.py
COPY app/configuration.py ./configuration.py
COPY common ./common

RUN pip install -r ./common/requirements.txt

ENTRYPOINT ['python', '/opt/src/worker.py']
