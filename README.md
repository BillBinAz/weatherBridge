# WeatherBridge

Gather residential data from Ecobee, Davis Weather Station, Honeywell Alarm, and SensorPush, and serve it up via REST API for display.

## Features

- Collects weather data from various sources
- RESTful API to access the data
- Dockerized for easy deployment

## Installation

### Prerequisites

- Docker
- Python 3.13+

### Docker Build and Run

```bash
docker build -t weatherbridge:latest .
docker run -p 8080:8080 weatherbridge:latest
```

### Manual Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python -m flask run --host=0.0.0.0 --port=8080
   ```

## API Endpoints

- `GET /weather`: Returns weather data in JSON format

## Windows Syslog Stub

On Windows, create a `syslog.py` file with the following content to stub syslog functionality:

```python
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
