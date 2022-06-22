FROM my-python

WORKDIR /opt/src

COPY ./app/configuration.py ./configuration.py
ADD ./app/worker.py ./worker.py

ENTRYPOINT ["python", "worker.py"]
