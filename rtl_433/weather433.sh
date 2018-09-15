#!/bin/bash

readonly SCRIPT_NAME=$(basename $0)

err() {
  echo "$@" >&2
  logger -p user.error -t $SCRIPT_NAME "$@"
}

# make sure the data directory is current
cd ~/weatherBridge

# See if it is running
if ! pgrep -x "rtl_433" > /dev/null
then

    # remove the old temp file
    rm /tmp/weather433.temp

    # collect the sensor data
    /usr/local/bin/rtl_433 -F json:/tmp/weather433.temp -T 530 -R 40 -d 0 -W 2>&1

    # now that we have collected data into temp, make it available.
    ~/weatherBridge/rtl_433/filterJsonBySensor.py
    cp /tmp/weather433.json ~/weatherBridge/rtl_433/data/weather433.json

    # Syslog the success to stderr
    err "weather433.json Updated"
else
    err "rtl_433 already running"
fi
