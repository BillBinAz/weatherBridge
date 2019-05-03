#!/bin/bash
sudo pgrep python | xargs kill
cd ~/weatherBridge/rtl_433
/usr/bin/python3 ~/weatherBridge/rtl_433/get_handler.py
