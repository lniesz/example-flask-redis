FROM python:3.8

RUN apt-get clean \
    && apt-get -y update

RUN mkdir -p /app/logs

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

COPY app.py /app/app.py
COPY templates /app/templates

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

CMD [ "python3", "app.py" ]