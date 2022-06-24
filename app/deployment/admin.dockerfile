FROM my-python

WORKDIR /opt/src

COPY ./app/admin.py ./admin.py
COPY ./app/models.py ./models.py
COPY ./app/configuration.py ./configuration.py
