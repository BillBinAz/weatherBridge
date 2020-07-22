#!/bin/bash
sudo pgrep python | xargs kill
cd /home/admin/weatherBridge
export FLASK_APP=get_handler.py
/usr/bin/python3 -m flask run --host='0.0.0.0' --port=8080

