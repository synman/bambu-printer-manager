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
  <img src="https://github.com/synman/bambu-printer-manager/assets/1299716/87d484eb-2ea0-44d0-9711-ddf91ccd8edd" width="400px" />
  <img src="https://github.com/synman/bambu-printer-manager/assets/1299716/3a089d35-5c30-4eb0-b5e2-849ca076c632" width="400px" /> 
</p>

## Troubleshooting
So long as the backend api (api/api.py) is running, there a number of useful http endpoints you can call to assist with troubleshooting.

* `http://{container_host_ip}:{container_host_port}/api/health_check` - This service route dumps the entire `BambuPrinter` attribute 
structure as a `json` document and adds a general success / failure node at the bottom.

* `http://{container_host_ip}:{container_host_port}/api/toggle_verbosity` - This service route toggles the underlying log level of all components between `WARNING` and `DEBUG`.  

* `http://{container_host_ip}:{container_host_port}/api/trigger_printer_refresh` - This service route requests the printer send full status and version 
reports.

* `http://{container_host_ip}:{container_host_port}/api/dump_log` - This service route dumps the entire contents of the application log.

* `http://{container_host_ip}:{container_host_port}/api/truncate_log` - This service route deletes the current application log.  A restart may be 
required for logging to resume.

* `http://{container_host_ip}:{container_host_port}/api/toggle_session` - This service route pauses or resumes the `BambuPrinter` session.  This may be 
helpful on machines such as the `A1` where only one client can be connected at a time.
