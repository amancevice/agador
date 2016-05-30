FROM alpine
MAINTAINER smallweirdnum@gmail.com

RUN apk add --update curl python-dev py-pip build-base
RUN pip install agador boto3 influxdb jupyter

WORKDIR /example

EXPOSE 8888
