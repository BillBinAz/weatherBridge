##weatherBridge.service

[Unit]
Description=Weather Bridge Service
After=multi-user.target

[Service]
Type=idle
Restart=always
ExecStart=/home/admin/weatherBridge/launch_rest.sh

[Install]
WantedBy=multi-user.target

##nodelink.service

[Unit]
Description=NodeLink ISY Service

[Service]
Restart=always
ExecStart=/home/admin/node/nodelink.sh
StandardOutput=syslog+console

[Install]
WantedBy=multi-user.target
Alias=nodelink.service

##weatherBridgeRest.service

[Unit]
Description=Rest WeatherBridge Service

[Service]
ExecStart=/home/admin/weatherBridge/launch_rest.sh
StandardOutput=syslog+console

[Install]
WantedBy=multi-user.target
Alias=weatherBridgeRest.service

