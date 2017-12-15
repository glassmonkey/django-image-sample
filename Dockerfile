FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /var/www
WORKDIR /var/www
ENV PYTHONDONTWRITEBYTECODE 1
ENV DEBIAN_FRONTEND noninteractive
ENV DOCKER true
ADD requirements.txt .
RUN apt-get update
RUN apt-get install -y build-essential cmake pkg-config
RUN apt-get install -y libx11-dev libatlas-base-dev
RUN apt-get install -y libgtk-3-dev libboost-python-dev
RUN pip install -r requirements.txt
