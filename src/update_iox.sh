#!/bin/bash -l

 cd /weatherBridge
 /usr/local/bin/python3 /weatherBridge/update_iox.py > /var/log/weather_bridge_cron.log 2>&1