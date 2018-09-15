# WeatherBridge
Python3 code to upload weather data from metrohub and metrobridge to isy994.


## Dependencies
python3  <br>
pip3 install httplib2  <br>
pip3 install Flask  <br>

### SDR
https://github.com/merbanan/rtl_433

#### Permissions errors:
    1.) enter lsusb - the command should give you a complete list for your USB devices, incl. your RTLSDR

    2.) Note that line which is related to your stick (e.g. Bus 003 Device 018: ID 0bda:2832 Realtek Semiconductor Corp. RTL2832U DVB-T)

    3.) open rtl-sdr.rules file with sudo nano /etc/udev/rules.d/rtl-sdr.rules

    4.) Add the line (e.g.)
    Code:
    SUBSYSTEMS=="usb", ATTRS{idVendor}=="0bda", ATTRS{idProduct}=="2832", MODE:="0666" -
    5.) save the file and restart udev with sudo service udev restart

    6.) restart the Pi

### crontab -e
*/5 * * * *  cd ~/weatherBridge/isy993 && ./update_isy.py > /tmp/weatherBridge.log 2>&1 <br>
*/10 * * * * cd ~/weatherBridge/rtl_433 && ./weather433.sh > /tmp/weather433.log 2>&1


### On a windows box add this to a syslog.py file on the path

```syslog.py stub
import sys

LOG_EMERG, LOG_ALERT, LOG_CRIT, LOG_ERR, LOG_WARNING, \
LOG_NOTICE, LOG_INFO, LOG_DEBUG = range(8)

LOG_KERN, LOG_USER, LOG_MAIL, LOG_DAEMON, LOG_AUTH, \
LOG_SYSLOG, LOG_LPR, LOG_NEWS, LOG_UUCP = range(0,65,8)

LOG_CRON = 120
LOG_LOCAL0 = 128
LOG_LOCAL1 = 136
LOG_LOCAL2 = 144
LOG_LOCAL3 = 152
LOG_LOCAL4 = 160
LOG_LOCAL5 = 168
LOG_LOCAL6 = 176
LOG_LOCAL7 = 184

LOG_PID = 1
LOG_CONS = 2
LOG_NDELAY = 8
LOG_NOWAIT = 16

def syslog(message):
    pass

def syslog(priority, message):
    pass

def openlog(ident=sys.argv[0], logoptions=0, facility=LOG_USER):
    pass

def closelog():
    pass

def setlogmask(maskpri):
    pass
```
