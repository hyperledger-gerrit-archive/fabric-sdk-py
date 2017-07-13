FROM python:3.5
MAINTAINER fabric-sdk-py "https://github.com/hyperledger/fabric-sdk-py"

COPY . /fabric-sdk-py

WORKDIR /fabric-sdk-py

RUN pip install tox pytest \
    && python setup.py install

CMD ["bash", "-c", "while true; do sleep 1000; done"]