FROM alpine
MAINTAINER smallweirdnum@gmail.com

RUN apk add --update curl python-dev py-pip build-base
RUN pip install pip==8.1.2 influxdb jupyter redis agador

ENV AGADOR_ENDPOINT=http://consul.service.com:8500/v1/kv/agador/python

WORKDIR /example

EXPOSE 8888
