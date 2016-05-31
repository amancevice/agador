FROM alpine
MAINTAINER smallweirdnum@gmail.com

RUN apk add --update curl python-dev py-pip build-base
RUN pip install agador influxdb jupyter redis

ENV AGADOR_HOST=agador.service.com
ENV AGADOR_PORT=9999
ENV AGADOR_SCHEME=http

WORKDIR /example

EXPOSE 8888
