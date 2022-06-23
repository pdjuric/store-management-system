FROM my-python

WORKDIR /opt/src

COPY ./app/migrate.py ./migrate.py
COPY ./app/models.py ./models.py
COPY ./app/configuration.py ./configuration.py

ENV FLASK_APP=migrate.py
