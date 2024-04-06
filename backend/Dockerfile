FROM ubuntu:latest

WORKDIR /app

COPY . /app

RUN ls -a
RUN cd app || true
RUN ls -a
RUN cd .. || true

RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install --no-cache-dir -r requirements.txt --verbose

EXPOSE 8080

CMD ["python3", "app.py"]

