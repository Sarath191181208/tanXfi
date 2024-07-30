FROM python:3.12-alpine as base 

# setting up env 
ENV LANG C.UTF-8 
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1 

COPY requirements.txt .

RUN pip install -r requirements.txt
COPY . /app
