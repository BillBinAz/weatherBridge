#! /bin/bash
(crontab -l 2>/dev/null; cat cronjobs) | crontab -
cron -n
python3 -m flask run --host=0.0.0.0 --port=8080 --no-reload