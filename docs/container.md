# bambu-printer-manager Client Container
This container is a Material UI / React application for monitoring and administering Bambu Lab printers.  It runs on an `Alpine Linux` image with `HAPROXY` working as a reverse proxy for the frontend, backend, and webcam services.

The frontend is written in `nodejs` and uses the `React Material UI` library for producing a content rich user experience.  The backend is written in `Python` and uses a `Flask Waitress` server for responding to frontend api calls with the help of a [custom python library](https://github.com/synman/bambu-printer-manager) developed specifically for interacting with `Bambu Lab` printers. The webcam service is a [custom python daemon](https://github.com/synman/webcamd/tree/bambu) that decodes the printer's built-in webcam data and produces a `MJPEG` stream that  is served by the frontend.

## Installation
```
# Configure the host, access code, serial # environment variables and 
# map the HAPROXY listener to a host port to launch the container

docker run \
       -e BAMBU_HOSTNAME='PRINTER_HOSTNAME_OR_IP' \
       -e BAMBU_ACCESS_CODE='PRINTER_ACCESS_CODE' \
       -e BAMBU_SERIAL_NUMBER='PRINTER_SERIAL_NUMBER' \
       -p 80:8080 \
       --name bambu-printer-manager synman/bambu-printer-manager
```
## Usage
To use `bambu-printer-manager` you only need to pull the image, configure a couple environment variables, and map the `HAPROXY` listener (port 8080) to a usable port on the host machine.  You then access it like you would any other web based application.

<p float="center">
  <img src="https://github.com/synman/bambu-printer-manager/assets/1299716/a1c170e5-f332-4ec9-b35d-6b773c67eac8" width="300px" />
  <img src="https://github.com/synman/bambu-printer-manager/assets/1299716/1bdfec3a-4379-4c8f-b93b-3bfdb06de3a6" width="300px" /> 
  <img src="https://github.com/synman/bambu-printer-manager/assets/1299716/b7f5af63-2340-4e56-9d65-4821b5911782" width="300px" /> 
</p>

## External Chamber Heating
This is an `advanced` feature of the container that allows you to use a [heater](https://www.amazon.com/Safety-Energy-saving-Portable-Desktop-Electric/dp/B07573FKSG?th=1) to control the atmosphere within your printer's enclosure. This is very helpful if you have an A1 in an enclosure and want to use 
exotic filaments such as ABS, ASA, Polycarbonite, and Nylon.

You connect the heater to a Wi-Fi enabled power plug (tplink / tasmota / esphome / tuya / etc) for power delivery and configure the plug to respond to 
power state commands and power state requests over MQTT.  Some plugs, such as tasmota and esphome flashed one can do this directly while others will
likely require something like Home Assistant.

You also need a Wi-Fi enabled temperature sensor that can do similar as the Wi-Fi power plug to publish environmental data, specifically the temperature, 
to an MQTT topic.  The easiest way to do this is to build one [yourself](https://github.com/synman/bme280).  However, I'm sure there are a number of pre-assembled ones you could use too.

The final step is configuring the `bambu-printer-manager` container to interact with the temperature sensor and power plug:
```dockerfile
ENV INTEGRATED_EXTERNAL_HEATER="TRUE"

ENV CHAMBER_MQTT_HOST="MQTT_SERVER_HOST_OR_IP"
ENV CHAMBER_MQTT_PORT="1883"
ENV CHAMBER_MQTT_USER="MQTT_USER_NAME"
ENV CHAMBER_MQTT_PASS="MQTT_PASSWORD"
ENV CHAMBER_TARGET_TOPIC="bambu-printer-manager/chamber_target"
ENV CHAMBER_TEMPERATURE_TOPIC="CHAMBER_TEMPERATURE_TOPIC"
ENV CHAMBER_REQUESTED_STATE_TOPIC="HEATER_REQUESTED_STATE_TOPIC"
ENV CHAMBER_CURRENT_STATE_TOPIC="HEATER_CURRENT_STATE_TOPIC"
ENV CHAMBER_STATE_ON_VALUE="on"
ENV CHAMBER_STATE_OFF_VALUE="off"
```
Once everything is configured properly, you will be able to monitor your chamber's temperature and set a target temperature for it the same 
way you monitor temperature and set target values for the tool (extruder), the bed, and, the part cooling fan.
<p float="center">
  <img src="https://github.com/synman/bambu-printer-manager/assets/1299716/56f011c4-2fa5-44de-8f2d-6f1a3abb89a9" />
</p>

## Troubleshooting
If you are geting a `port is already in use` type error, it is likely because you are trying to run the container using the host's 
network.  It is recommended that you run the `bambu-printer-manager` container on a bridged network.  Behind the "public" port exposed by
HAPROXY (`8080`), it also requires exclusive access to ports `3000` (nodejs react frontend), `5000` (flask waitress backend), and 
`8090` (webcamd).  Some hosts, such as Synology DSM use ports like `5000` and this will cause problems.

Verify your printer's information.  You must know its routable IP Address, access code, and serial #. You can find each of these on 
your printer's display.  These must match your Docker container's applicable environment variable values.
```docker
ENV BAMBU_HOSTNAME="PRINTER_HOST_OR_IP"
ENV BAMBU_ACCESS_CODE="PRINTER_ACCESS_CODE"
ENV BAMBU_SERIAL_NUMBER="PRINTER_SERIAL_NUMBER"
```
So long as the backend api (api/api.py) is running, there a number of useful http endpoints you can call to assist with troubleshooting.

* `http://{container_host_ip}:{container_host_port}/api/health_check` - This service route dumps the entire `BambuPrinter` attribute 
structure as a `json` document and adds a general success / failure node at the bottom.

* `http://{container_host_ip}:{container_host_port}/api/toggle_verbosity` - This service route toggles the underlying log level of all components between `WARNING` and `DEBUG`.  

* `http://{container_host_ip}:{container_host_port}/api/trigger_printer_refresh` - This service route requests the printer send full status and version 
reports.

* `http://{container_host_ip}:{container_host_port}/api/dump_log` - This service route serves the entire contents of the application log.

* `http://{container_host_ip}:{container_host_port}/api/truncate_log` - This service route deletes the current application log.  A restart may be 
required for logging to resume.

* `http://{container_host_ip}:{container_host_port}/api/toggle_session` - This service route pauses or resumes the `BambuPrinter` session.  This may be 
helpful on machines such as the `A1` where only one client can be connected at a time.

If you encounter an issue you need help with, feel free to open a ticket at [GitHub](https://github.com/synman/bambu-printer-manager/issues).