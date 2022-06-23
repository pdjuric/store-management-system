FROM my-python

WORKDIR /opt/src

COPY ./auth/migrate.py ./migrate.py
COPY ./auth/models.py ./models.py
COPY ./auth/configuration.py ./configuration.py

ENV FLASK_APP=migrate.py
