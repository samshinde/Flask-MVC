FROM python:3.6

RUN mkdir /entity_mgmt_app

WORKDIR /entity_mgmt_app

ADD requirements.txt /entity_mgmt_app

RUN pip3.6 install --requirement requirements.txt

ADD . /entity_mgmt_app

EXPOSE 5000

CMD ["python3.6", "run.py"]