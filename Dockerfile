FROM mcr.microsoft.com/playwright/python:v1.55.0-noble

WORKDIR /app

COPY pages /app/pages
COPY tests /app/tests
COPY utilities /app/utilities

COPY requirements.txt /app/

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt