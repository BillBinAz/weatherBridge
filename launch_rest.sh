#!/bin/bash
sudo pgrep python | xargs kill
cd /home/admin/weatherBridge
export FLASK_APP=get_handler.py
flask run

