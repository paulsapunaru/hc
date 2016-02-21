FROM python:2.7.11

RUN pip install -U pymongo flask

COPY server /hc/server
COPY common /hc/common
ENV PYTHONPATH=/hc:$PYTHONPATH
CMD python /hc/server/web_server.py
