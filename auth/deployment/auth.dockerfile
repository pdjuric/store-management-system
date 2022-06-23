FROM my-python

WORKDIR /opt/src

COPY ./auth/app.py ./app.py
COPY ./auth/models.py ./models.py
COPY ./auth/configuration.py ./configuration.py
