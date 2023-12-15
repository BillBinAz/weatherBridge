# syntbillbinaz/weatherbridge:latestax=docker/dockerfile:1
FROM python:3.11-slim-bookworm

WORKDIR /weatherBridge
COPY ./src .
ADD ./config/startup.sh /weatherBridge/startup.sh
ADD ./config/cronjobs /weatherBridge/cronjobs


RUN apt update && apt upgrade -y
RUN pip3 install --upgrade pip
RUN chmod 655 startup.sh
RUN chmod 655 update_iox.sh
RUN pip3 install -r requirements.txt

ENV FLASK_APP=get_handler.py
EXPOSE 8080
CMD [ "/weatherBridge/startup.sh" ]