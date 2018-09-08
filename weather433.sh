#!/bin/bash

readonly SCRIPT_NAME=$(basename $0)

err() {
  echo "$@" >&2
  logger -p user.error -t $SCRIPT_NAME "$@"
}

# make sure the data directory is current
cd /home/admin/weatherBridge

# See if it is running
if ! pgrep -x "rtl_433" > /dev/null
then

    # remove the old temp file
    rm weather433.temp

    # collect the sensor data
    /usr/local/bin/rtl_433 -F json:/home/admin/weatherBridge/data/weather433.temp -T 300 -R 40 -d 0 -W 2>&1

    # now that we have collected data into temp, make it available.
    ./filterJsonBySensor.py

    # Syslog the success to stderr
    err "weather433.json Updated"
else
    err "rtl_433 already running"
fi
