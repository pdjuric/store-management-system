FROM my-python

WORKDIR /opt/src

COPY ./store/daemon.py ./daemon.py
COPY ./store/models.py ./models.py
COPY ./store/configuration.py ./configuration.py
