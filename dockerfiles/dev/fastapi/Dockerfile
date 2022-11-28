FROM python:3.9-slim-buster

WORKDIR /user/src

COPY ./requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY ./src .
