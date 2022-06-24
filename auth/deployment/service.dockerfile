FROM my-python

WORKDIR /opt/src

COPY ./auth/auth.py ./auth.py
COPY ./auth/models.py ./models.py
COPY ./auth/configuration.py ./configuration.py
