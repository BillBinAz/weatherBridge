#! /bin/bash

# set timezone
rm -rf /etc/localtime
ln -s /usr/share/zoneinfo/America/Phoenix /etc/localtime

# start cron
service cron start

# start flask
python3 -m flask run --host=0.0.0.0 --port=8080 --no-reload
