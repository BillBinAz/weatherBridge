FROM python:3.13-slim-bookworm

WORKDIR /weatherBridge
COPY requirements.txt .
COPY ./src .
ADD ./config/startup.sh /weatherBridge/startup.sh
RUN chmod +x /weatherBridge/startup.sh

RUN apt update && apt upgrade -y
RUN pip3 install --upgrade pip
RUN chmod 755 startup.sh
RUN chmod 755 update_iox.sh
RUN pip3 install -r requirements.txt

ENV FLASK_APP=get_handler.py
EXPOSE 8080
ENTRYPOINT [ "/weatherBridge/startup.sh" ]
