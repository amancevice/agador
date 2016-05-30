FROM alpine
MAINTAINER smallweirdnum@gmail.com

RUN apk add --update python-dev py-pip
RUN pip install pip==8.1.2 agador[server]==0.0.3

RUN addgroup agador && adduser -h /home/agador -G agador -D agador
USER agador
WORKDIR /home/agador

EXPOSE 9999

ENTRYPOINT ["agador"]
