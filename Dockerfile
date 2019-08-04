FROM ubuntu:latest
MAINTAINER FlakkenTime "Flakkentime gmail"
RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev build-essential
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENTRYPOINT ["gunicorn"]
CMD ["-c", "resources/config.py", "src.fang_service:app"]
