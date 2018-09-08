#!/bin/bash
cd /home/admin/weatherBridge/data
rtl_433 -f 433920000 -H 15 -F json:/home/admin/weatherBridge/data/weather433.json -T 10 -R 40 -d 0 -W 2>&1

