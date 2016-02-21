FROM python:2.7.11

RUN pip install -U praw pymongo

COPY reddit_bot /hc/reddit_bot
COPY common /hc/common
ENV PYTHONPATH=/hc:$PYTHONPATH
CMD python /hc/reddit_bot/reddit_bot.py
