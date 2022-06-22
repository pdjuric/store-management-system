FROM my-python

WORKDIR /opt/src

COPY ./app/customer.py ./customer.py
COPY ./app/models.py ./models.py
COPY ./app/configuration.py ./configuration.py
