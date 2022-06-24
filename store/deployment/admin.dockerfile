FROM my-python

WORKDIR /opt/src

COPY ./store/admin.py ./admin.py
COPY ./store/models.py ./models.py
COPY ./store/configuration.py ./configuration.py
