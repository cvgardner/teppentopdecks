FROM python:3.10-alpine

COPY config.py /bots/
COPY retweet.py /bots/
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

WORKDIR /bots
CMD ["python3", "retweet.py"]