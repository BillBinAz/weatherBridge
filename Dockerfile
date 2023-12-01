# syntax=docker/dockerfile:1
FROM python

WORKDIR /weatherBridge
COPY . .

RUN apt-get update && apt-get upgrade -y && apt-get install cron -y
RUN chmod 655 startup.sh
RUN pip3 install -r requirements.txt

ENV FLASK_APP=get_handler.py
EXPOSE 8080
CMD [ "/weatherBridge/startup.sh" ]