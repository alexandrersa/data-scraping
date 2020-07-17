# pull official base image
FROM python:3.8

# install system dependencies
RUN apt-get update

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# run scrapy
CMD [ "python3", "../crawler/scrapy.py" ]
