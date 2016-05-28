FROM amancevice/agador
MAINTAINER smallweirdnum@gmail.com

USER root

RUN pip install influxdb

COPY example.py /example.py

ENTRYPOINT ["python"]
CMD ["/example.py"]
