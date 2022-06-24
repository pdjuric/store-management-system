FROM my-python

WORKDIR /opt/src

COPY ./store/configuration.py ./configuration.py
ADD ./store/worker.py ./worker.py

ENTRYPOINT ["python", "worker.py"]
