FROM my-python

WORKDIR /opt/src

COPY ./store/customer.py ./customer.py
COPY ./store/models.py ./models.py
COPY ./store/configuration.py ./configuration.py
