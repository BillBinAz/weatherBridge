#!/bin/bash

readonly SCRIPT_NAME=$(basename $0)

err() {
  echo "$@" >&2
  logger -p user.error -t $SCRIPT_NAME "$@"
}

# make sure the data directory is current
cd /home/admin/weatherBridge/data

# remove the old temp file
rm weather433.temp
/usr/local/bin/rtl_433 -f 433920000 -H 10 -F json:/home/admin/weatherBridge/data/weather433.temp -T 120 -R 40 -d 0 -W 2>&1

# now that we have collected data into temp, make it available.
cp weather433.temp weather433.json

# Syslog the success to stderr
err "433 Weather Updated"
