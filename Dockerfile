FROM python:3.12-slim
RUN mkdir /app
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
CMD [ "python3", "./timekpr-next-web.py"]
