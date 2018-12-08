FROM python:3

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY ./players.py /app/players.py

ENV BASKETBALL_DB ''

CMD python players.py

# docker build -t basketball ./ && docker run -it --rm basketball