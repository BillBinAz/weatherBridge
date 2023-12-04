# syntbillbinaz/weatherbridge:latestax=docker/dockerfile:1
FROM python

WORKDIR /weatherBridge
COPY ./src .
ADD ./config/startup.sh /weatherBridge/startup.sh
ADD ./config/cronjobs /weatherBridge/cronjobs


RUN apt update && apt upgrade -y
RUN pip3 install --upgrade pip
RUN chmod 655 startup.sh
RUN chmod 655 update_iox.sh
RUN pip3 install -r requirements.txt

# install cron
RUN apt -y install cron

# Add crontab
RUN (crontab -l 2>/dev/null; tr -d '\r' < cronjobs) | crontab -

ENV FLASK_APP=get_handler.py
EXPOSE 8080
CMD [ "/weatherBridge/startup.sh" ]