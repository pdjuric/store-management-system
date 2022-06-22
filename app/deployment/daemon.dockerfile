FROM my-python

WORKDIR /opt/src

COPY ./app/daemon.py ./daemon.py
COPY ./app/models.py ./models.py
COPY ./app/configuration.py ./configuration.py
