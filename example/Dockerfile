FROM alpine
MAINTAINER smallweirdnum@gmail.com

RUN apk add --update curl python-dev py-pip build-base
RUN pip install pip==8.1.2 agador influxdb jupyter redis

ENV AGADOR_HOST=consul.service.com
ENV AGADOR_PORT=8500
ENV AGADOR_SCHEME=http

WORKDIR /example

EXPOSE 8888
