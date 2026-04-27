FROM python:3-alpine

WORKDIR /weatherBridge
COPY requirements.txt .
COPY ./src .
ADD ./config/startup.sh /weatherBridge/startup.sh
RUN chmod +x /weatherBridge/startup.sh

RUN apk update && apk upgrade && apk add --no-cache bash
RUN pip3 install --upgrade pip
RUN chmod 755 startup.sh
RUN pip3 install -r requirements.txt

ENV FLASK_APP=get_handler.py
EXPOSE 8080
ENTRYPOINT [ "/weatherBridge/startup.sh" ]
