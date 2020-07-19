# pull official base image
FROM python:3.8

# set work directory
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY . .

# run scrapy
CMD [ "scrapy", "shell", "--nolog" ]
