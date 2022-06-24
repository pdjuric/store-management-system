FROM my-python

WORKDIR /opt/src

COPY ./store/migrate.py ./migrate.py
COPY ./store/models.py ./models.py
COPY ./store/configuration.py ./configuration.py

ENV FLASK_APP=migrate.py
