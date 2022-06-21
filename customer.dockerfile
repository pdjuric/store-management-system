FROM python:3

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN mkdir -p /opt/src/common
WORKDIR /opt/src

COPY app/customer.py ./customer.py
COPY app/models.py ./models.py
COPY app/configuration.py ./configuration.py
COPY common ./common

RUN pip install -r ./common/requirements.txt
