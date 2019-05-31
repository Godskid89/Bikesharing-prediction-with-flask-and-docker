FROM python:3

LABEL Joseph Oladokun

COPY . /usr/src
WORKDIR /usr/src

RUN python -m pip install -U pip \
    && pip install -r requirements.txt

CMD [ "python", "server.py" ]