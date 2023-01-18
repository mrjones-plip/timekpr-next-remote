FROM python:3.8-slim-buster
RUN mkdir /app
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
CMD [ "python3", "./timekpr-next-web.py"]
