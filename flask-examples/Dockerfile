FROM python:3
LABEL maintainer="Amol Shinde <samshinde23290@gmail.com>"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD FLASK_APP=sample.py flask run
