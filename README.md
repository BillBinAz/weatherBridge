# WeatherBridge
Python3 code to upload weather data from metrohub and metrobridge to isy994

## Dependencies
python3
pip3 install httplib2


## crontab
 */5 *   *   *   *   cd /home/pi/weatherBridge && ./update_isy.py > /tmp/weatherBridge.log 2>&1
