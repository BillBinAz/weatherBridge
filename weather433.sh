#!/bin/bash
cd /home/admin/weatherBridge/data
rm weather433.temp
rtl_433 -f 433920000 -H 15 -F json:/home/admin/weatherBridge/data/weather433.temp -T 50 -R 40 -d 0 -W 2>&1
cp weather433.temp weather433.json
