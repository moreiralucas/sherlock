FROM python:3.9.6

RUN apt-get update && apt-get -y install gcc

COPY . /usr/src/app/
WORKDIR /usr/src/app/
RUN mkdir -p submissions/ && make


# WORKDIR /usr/src/app/
# https://stackoverflow.com/questions/30323224/deploying-a-minimal-flask-app-in-docker-server-connection-issues
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

CMD ["python", "main.py"]
