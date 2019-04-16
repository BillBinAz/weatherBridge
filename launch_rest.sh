#!/bin/bash
sudo pgrep python | xargs kill
cd /home/admin/weatherBridge
/usr/bin/python3 /home/admin/weatherBridge/get_handler.py &>> /tmp/weatherBridge.getHandler.log 
