FROM python:3.11-slim

RUN pip install scrapy sqlalchemy psycopg2-binary

COPY . /app
WORKDIR /app


CMD ["scrapy", "crawl", "weatherParser", "-O", "1.json"]

RUN python3.11 convertData.py
RUN python3.11 toDatabase.py 
