# bambu-printer-manager Client Container
This container is a Material UI / React application for monitoring and administering Bambu Lab printers.  It runs on an `Alpine Linux` image with `NGINX` working as a reverse proxy for the frontend, backend, and camera stream.

The frontend is written in `nodejs` and uses the `React Material UI` library for producing a content rich user experience.  The backend is written in `Python` and uses `Flask` + `Flask-SocketIO`, served by `gunicorn` (`gthread` worker class — plain WSGI servers such as waitress do not support the WebSocket upgrade Socket.IO needs), together with a [custom python library](https://github.com/synman/bambu-printer-manager) developed specifically for interacting with `Bambu Lab` printers.

The camera stream is produced by an embedded, multi-threaded Python MJPEG server built into the backend itself (`api/camera/`) — there is no separate webcam sidecar process. It dispatches per printer model: A1/P1/P1S speak the printer's proprietary TCP+TLS protocol on port 6000, while H2D/X1/P2S are read over RTSPS (port 322) via PyAV. Either way the backend re-encodes frames to MJPEG and serves them on an internal port (`8091`), which NGINX proxies at `/webcam/`. This replaces an earlier architecture built on a `webcamd` sidecar (A1/P1) plus `go2rtc` + `ffmpeg` (P2/H2/X1) — do not configure `webcamd` or `go2rtc` for a current image.

## Become a Sponsor
While caffiene and sleepness nights drive the delivery of this project, they unfortunately do not cover the financial expense necessary to further its development.  Please consider becoming a `bambu-printer-manager` sponsor today!

[![Sponsor](https://img.shields.io/badge/Sponsor-%E2%9D%A4-red?style=for-the-badge&logo=github)](https://github.com/sponsors/synman)

## Installation
```
# Configure the host, access code, and serial # environment variables and
# map the NGINX listener to a host port to launch the container

docker run \
       -e BAMBU_HOSTNAME='PRINTER_HOSTNAME_OR_IP' \
       -e BAMBU_ACCESS_CODE='PRINTER_ACCESS_CODE' \
       -e BAMBU_SERIAL_NUMBER='PRINTER_SERIAL_NUMBER' \
       -p 80:8080 \
       --name bambu-printer-manager synman/bambu-printer-manager
```
`BAMBU_SERIAL_NUMBER` must contain only letters and digits — the container validates this at startup (it exits immediately if not) since the value is also used as a directory name for staged uploads/downloads (see [Volumes](#volumes) below).

## Usage
To use `bambu-printer-manager` you only need to pull the image, configure a couple environment variables, and map the `NGINX` listener (port 8080) to a usable port on the host machine.  You then access it like you would any other web based application.

![Cards](https://github.com/synman/bambu-printer-manager/assets/1299716/5015c3ff-dbde-4427-8e6c-ba0ec9a18588)
![Charts](https://github.com/synman/bambu-printer-manager/assets/1299716/9e1aae05-9fca-4e42-a8d4-8d53c5db53de)
![Control](https://github.com/synman/bambu-printer-manager/assets/1299716/ac99d2b5-0df0-465e-a505-5d7be5828514)
![Filament](https://github.com/synman/bambu-printer-manager/assets/1299716/f410b8f0-16c0-4db2-84d2-d85314cf688d)
![Files](https://github.com/synman/bambu-printer-manager/assets/1299716/22f0d7c9-5812-4475-8cbe-5eea73b63bef)

<p float="center">
  <img src="https://github.com/synman/bambu-printer-manager/assets/1299716/a1c170e5-f332-4ec9-b35d-6b773c67eac8" width="300px" />
  <img src="https://github.com/synman/bambu-printer-manager/assets/1299716/1bdfec3a-4379-4c8f-b93b-3bfdb06de3a6" width="300px" />
  <img src="https://github.com/synman/bambu-printer-manager/assets/1299716/b7f5af63-2340-4e56-9d65-4821b5911782" width="300px" />
</p>

## Volumes

Run one container per printer. Three folders are worth mounting, and several containers may share the host folders:

| Container path | Mode | Holds | Sharing between containers |
|---|---|---|---|
| `/bambu-printer-app/api/uploads` | rw | files uploaded from your computer, and files downloaded from the printer, staged before they are sent on | Safe. BPA stages under `uploads/<BAMBU_SERIAL_NUMBER>/`, so two printers' files with the same name can no longer overwrite each other or be sent to the wrong printer. |
| `/nginx` | ro | custom NGINX confs and `.htpasswd` (see [Custom NGINX Configuration](#custom-nginx-configuration)) | Safe. Each container picks its own conf with `BAMBU_CUSTOM_NGINX_CONF`. |
| `/root/.bpm` | rw | `bambu-printer-manager`'s cache: the current job's record, elapsed-print-time records and 3mf metadata, all filed under the printer's serial | Safe to share, since everything is filed by serial. Without a mount, the cache is lost on every image update. |

```bash
docker run -d \
    ... \
    -v /path/to/uploads:/bambu-printer-app/api/uploads \
    -v /path/to/nginx-configs:/nginx:ro \
    -v /path/to/bpm-cache:/root/.bpm \
    -p 80:8080 \
    --name bambu-printer-manager synman/bambu-printer-manager
```

## Custom NGINX Configuration

The container provides a flexible NGINX configuration system that allows you to override the default reverse proxy settings. This is particularly useful for implementing security features like HTTP Basic Authentication.

### Using BAMBU_CUSTOM_NGINX_CONF

Set the `BAMBU_CUSTOM_NGINX_CONF` environment variable to specify a custom NGINX configuration file:

```dockerfile
ENV BAMBU_CUSTOM_NGINX_CONF="/nginx/custom-nginx.conf"
```

Mount your custom configuration directory when starting the container:

```bash
docker run -d \
    -e BAMBU_HOSTNAME="192.168.1.100" \
    -e BAMBU_ACCESS_CODE="12345678" \
    -e BAMBU_SERIAL_NUMBER="01S00A123456789" \
    -e BAMBU_CUSTOM_NGINX_CONF="/nginx/nginx-auth.conf" \
    -v /path/to/your/nginx-configs:/nginx:ro \
    -p 80:8080 \
    --name bambu-printer-manager synman/bambu-printer-manager
```

### Authentication Example

The camera stream is served the same way for every printer model — the embedded camera server always listens on `127.0.0.1:8091` regardless of protocol — so a single custom config with HTTP Basic Authentication covers frontend, API, Socket.IO, and video for any printer. Below is a complete example, adapted from the shipped default (`docker/nginx/nginx.conf`).

#### nginx-auth.conf (all printer models)

```nginx
worker_processes 2;

events {
    worker_connections 256;
}

http {
    set_real_ip_from  172.17.0.0/16;
    set_real_ip_from  10.151.51.1;
    set_real_ip_from  10.151.51.24;
    set_real_ip_from  127.0.0.1;

    real_ip_header    X-Forwarded-For;
    real_ip_recursive on;

    limit_req_zone $binary_remote_addr zone=auth_limit:10m rate=3r/m;

    log_format combined_realip '$remote_addr - $remote_user [$time_local] '
                               '"$request" $status $body_bytes_sent '
                               '"$http_referer" "$http_user_agent"';

    access_log /var/log/nginx/access.log combined_realip;

    server {
        listen 8080;
        port_in_redirect off;

        # Root-level Basic Auth
        auth_basic "Private System";
        auth_basic_user_file /nginx/.htpasswd;

        include /etc/nginx/mime.types;

        # --- Location block for the Vite frontend ---
        location / {
            root /bambu-printer-app/dist;
            index index.html;
            try_files $uri $uri/ /index.html;
            add_header Cache-Control "no-cache";
            add_header X-Powered-By "shellware-vite";
            add_header X-Forward-To-Url "file:///bambu-printer-app/dist$uri";

            error_page 401 = @limit_failed_auth;
        }

        # --- Location block for the API service ---
        location /api/ {
            # Enable NGINX to intercept 503 errors from the backend
            proxy_intercept_errors on;
            error_page 503 @custom_503_python;

            # Need a big max body size to support http uploads
            client_max_body_size 150M;
            proxy_pass http://127.0.0.1:5000;

            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            add_header Cache-Control "no-cache";
            add_header X-Powered-By "shellware-api";
            add_header X-Forward-To-Url "http://$proxy_host$uri$is_args$args";

            error_page 401 = @limit_failed_auth;
        }

        # --- Location block for Socket.IO (WebSocket upgrade) ---
        location /socket.io/ {
            proxy_pass http://127.0.0.1:5000;

            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

            proxy_read_timeout 86400;

            error_page 401 = @limit_failed_auth;
        }

        # --- Location block for the MJPEG stream (embedded camera server on :8091) ---
        location /webcam/ {
            # Enable NGINX to intercept 503 errors from the backend
            proxy_intercept_errors on;
            error_page 503 @custom_503_webcam;

            proxy_pass http://127.0.0.1:8091/;

            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

            add_header Cache-Control "no-cache";
            add_header X-Powered-By "shellware-bpa-camera";
            add_header X-Forward-To-Url "http://$proxy_host$uri$is_args$args";

            # Disable buffering for a near real-time stream.
            proxy_buffering off;

            # Increase the timeout to prevent NGINX from closing the
            # long-lived connection. A high value like 86400 (24 hours) is recommended.
            proxy_read_timeout 86400;

            # Disable caching.
            proxy_cache off;

            # If your stream has a `Content-Type: multipart/x-mixed-replace` header,
            # include the following line for compatibility.
            proxy_set_header Connection "";

            error_page 401 = @limit_failed_auth;
        }

        # --- Specific named location for the API 503 error page ---
        location @custom_503_python {
            root /etc/nginx/errors;
            internal;
            error_page 401 = @limit_failed_auth;
            try_files /503-no-python.http =503;
        }

        # --- Specific named location for the Webcam 503 error page ---
        location @custom_503_webcam {
            root /etc/nginx/errors;
            internal;
            error_page 401 = @limit_failed_auth;
            try_files /503-no-webcam.http =503;
        }

        # The throttling "jail" for failed attempts
        location @limit_failed_auth {
            limit_req zone=auth_limit burst=1 nodelay;
            limit_req_status 429;
            return 401;
        }
    }
}
```

This is the shipped default config (`docker/nginx/nginx.conf`) with Basic Auth, `real_ip`/rate-limiting, and access logging layered on. All printer models proxy `/webcam/` to the same upstream, `http://127.0.0.1:8091/` — the embedded camera server, not a per-model daemon — so there is only one config to maintain.

### Managing Password Files

To use Basic Authentication, create a `.htpasswd` file with bcrypt-hashed passwords:

**Using htpasswd (most Linux distributions, macOS Homebrew):**
```bash
# Create new password file with first user
htpasswd -Bc /path/to/your/nginx-configs/.htpasswd username

# Add additional users
htpasswd -B /path/to/your/nginx-configs/.htpasswd another_user
```

**Using openssl (alternative method):**
```bash
# Generate password hash
echo "username:$(openssl passwd -apr1 your_password)" > /path/to/your/nginx-configs/.htpasswd

# Add additional users
echo "another_user:$(openssl passwd -apr1 another_password)" >> /path/to/your/nginx-configs/.htpasswd
```

**Using Python (cross-platform):**
```python
import bcrypt

username = "admin"
password = "your_password"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

with open('.htpasswd', 'w') as f:
    f.write(f"{username}:{hashed}\n")
```

The mounted directory should contain both your custom NGINX config and the `.htpasswd` file:
```
/path/to/your/nginx-configs/
├── nginx-auth.conf
└── .htpasswd
```

**Security Notes:**
- Mount the directory as read-only (`:ro`) to prevent container modifications
- Use bcrypt (`-B` flag) for password hashing - it's more secure than MD5/SHA
- Never commit `.htpasswd` files to version control
- Consider using strong, randomly generated passwords for production deployments

## Video Stream
No configuration is needed. The embedded camera server derives `BAMBU_SERIAL_NUMBER`'s printer model at startup and picks the matching protocol automatically — TCP+TLS on port 6000 for A1/P1/P1S, RTSPS on port 322 for H2D/X1/P2S — then serves MJPEG frames to the frontend either way over `/webcam/`. The `BAMBU_VIDEO_STREAM_TYPE` variable from earlier versions of this container has been removed; it is no longer read.

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
NGINX (`8080`), it also requires exclusive access to ports `5000` (the Flask/gunicorn backend) and `8091` (the embedded camera server).
Some hosts, such as Synology DSM, use port `5000` themselves and this will cause problems.

Verify your printer's information.  You must know its routable IP Address, access code, and serial #. You can find each of these on
your printer's display.  These must match your Docker container's applicable environment variable values.
```docker
ENV BAMBU_HOSTNAME="PRINTER_HOST_OR_IP"
ENV BAMBU_ACCESS_CODE="PRINTER_ACCESS_CODE"
ENV BAMBU_SERIAL_NUMBER="PRINTER_SERIAL_NUMBER"
```
So long as the backend api (api/api.py) is running, there a number of useful http endpoints you can call to assist with troubleshooting.

* `http://{container_host_ip}:{container_host_port}/api/ping` - Liveness probe (`{"status": "alive"}` whenever the backend process is up, regardless of printer connection). This is what the container's own `HEALTHCHECK` polls.

* `http://{container_host_ip}:{container_host_port}/api/health_check` - This service route dumps the entire [`BambuPrinter`](reference/bpm/bambuprinter.md#bpm.bambuprinter.BambuPrinter) attribute
structure as a `json` document and adds a general success / failure node at the bottom. Unlike `/api/ping`, this one reports failure when the printer has no live data.

* `http://{container_host_ip}:{container_host_port}/api/toggle_verbosity` - This service route toggles the underlying log level between `INFO` and `DEBUG` (the root logger starts at `WARNING`, so the very first call moves it to `DEBUG`; every call after that alternates `DEBUG`/`INFO`).

* `http://{container_host_ip}:{container_host_port}/api/trigger_printer_refresh` - This service route requests the printer send full status and version
reports (when already connected), or starts a background reconnect otherwise.

* `http://{container_host_ip}:{container_host_port}/api/dump_log` - This service route serves the entire contents of the application log.

* `http://{container_host_ip}:{container_host_port}/api/truncate_log` - This service route truncates the current application log to zero bytes (it does not delete the file).  A restart may be
required for logging to resume.

* `http://{container_host_ip}:{container_host_port}/api/toggle_session` - This service route pauses or resumes the [`BambuPrinter`](reference/bpm/bambuprinter.md#bpm.bambuprinter.BambuPrinter) session.  This may be
helpful on machines such as the `A1` where only one client can be connected at a time.

## API Documentation

For complete REST API documentation including all endpoints, parameters, response formats, and usage examples, see the [API Reference](api-reference.md).

The API provides full programmatic control over:

- Printer status and telemetry
- Temperature and fan control
- Print job management
- Filament and AMS operations
- File management (SD card)
- Advanced settings and diagnostics

If you encounter an issue you need help with, feel free to open a ticket at [GitHub](https://github.com/synman/bambu-printer-manager/issues).

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.2 | 2026-09-27 | Verification pass against current source: replaced the retired `webcamd`/`go2rtc`/`BAMBU_VIDEO_STREAM_TYPE` architecture with the embedded per-model camera server (port 8091); corrected the backend server (gunicorn/gthread, not Waitress); consolidated the two MJPEG/RTSPS custom-auth NGINX examples into one, added the `/socket.io/` location and corrected the webcam `proxy_pass` target; fixed `toggle_verbosity` and `truncate_log` behaviour and the Troubleshooting port list; added `/api/ping` and the `BAMBU_SERIAL_NUMBER` validation note |
| 1.1 | 2026-02-25 | Documentation updates for REST API reference and authentication configuration |
| 1.0 | 2026-02-23 | Initial container deployment documentation |
