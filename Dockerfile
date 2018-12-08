FROM python:3

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY ./players.py /app/players.py
COPY ./db.py /app/db.py
COPY ./scrape.py /app/scrape.py

CMD python players.py

# docker build -t basketball ./ && docker run -e BASKETBALL_DB=<connection string> -it --rm basketball