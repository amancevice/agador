FROM alpine
MAINTAINER smallweirdnum@gmail.com

RUN apk add --update python-dev py-pip && pip install pip --upgrade
RUN pip install agador[server]==0.0.1

RUN addgroup agador && adduser -h /home/agador -G agador -D agador
USER agador
WORKDIR /home/agador

EXPOSE 9999

ENTRYPOINT ["agador"]
