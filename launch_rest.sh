#!/bin/bash
sudo pgrep python | xargs kill
rm /tmp/weather_bridge_rest.log
cd /home/admin/weatherBridge
export FLASK_APP=get_handler.py
/usr/bin/python3 -m flask run --host='0.0.0.0' --port=8080 --no-reload

