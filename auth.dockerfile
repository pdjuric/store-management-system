FROM python:3

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN mkdir -p /opt/src
WORKDIR /opt/src

COPY auth .

COPY requirements.txt ./requirements.txt
COPY wait-for-it.sh /wait-for-it.sh


RUN pip install -r ./requirements.txt

#ENTRYPOINT ["python", "./app.py"]
