FROM python:3

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN mkdir -p /opt/src/common
WORKDIR /opt/src
ADD ./common/* ./common/

RUN pip install -r ./common/requirements.txt
