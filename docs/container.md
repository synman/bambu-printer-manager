# bambu-printer-manager Client Container
This container is a Material UI / React application for monitoring and administering Bambu Lab printers.  It runs on an `Alpine Linux` image with `NGINX` working as a reverse proxy for the frontend, backend, and webcam services.

The frontend is written in `nodejs` and uses the `React Material UI` library for producing a content rich user experience.  The backend is written in `Python` and uses a `Flask Waitress` server for responding to frontend api calls and a [custom python library](https://github.com/synman/bambu-printer-manager) developed specifically for interacting with `Bambu Lab` printers.

The webcam service for A1 and P1 series printers is a [custom python daemon](https://github.com/synman/webcamd/tree/bambu) that decodes the printer's built-in webcam data and produces a `MJPEG` stream that is served by the frontend.

The video stream for P2/H2/X1 series printers is produced using `go2rtc` and `ffmpeg`.

## Become a Sponsor
While caffiene and sleepness nights drive the delivery of this project, they unfortunately do not cover the financial expense necessary to further its development.  Please consider becoming a `bambu-printer-manager` sponsor today!

[![Sponsor](https://img.shields.io/badge/Sponsor-%E2%9D%A4-red?style=for-the-badge&logo=github)](https://github.com/sponsors/synman)

## Installation
```
# Configure the host, access code, serial #, stream type environment variables and
# map the NGINX listener to a host port to launch the container

docker run \
       -e BAMBU_HOSTNAME='PRINTER_HOSTNAME_OR_IP' \
       -e BAMBU_ACCESS_CODE='PRINTER_ACCESS_CODE' \
       -e BAMBU_SERIAL_NUMBER='PRINTER_SERIAL_NUMBER' \
       -e BAMBU_VIDEO_STREAM_TYPE='MJPEG or RTSPS' \
       -p 80:8080 \
       --name bambu-printer-manager synman/bambu-printer-manager
```
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
    -e BAMBU_VIDEO_STREAM_TYPE="MJPEG" \
    -e BAMBU_CUSTOM_NGINX_CONF="/nginx/nginx-webcamd-auth.conf" \
    -v /path/to/your/nginx-configs:/nginx:ro \
    -p 80:8080 \
    --name bambu-printer-manager synman/bambu-printer-manager
```

### Authentication Examples

Below are two complete authentication-enabled NGINX configurations implementing HTTP Basic Authentication across all endpoints (frontend, API, and video streams).

#### nginx-webcamd-auth.conf (MJPEG - A1/P1 series)

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

        # --- Location block for the MJPEG stream ---
        location /webcam/ {
            # Enable NGINX to intercept 503 errors from the backend
            proxy_intercept_errors on;
            error_page 503 @custom_503_webcam;

            # This rewrite rule removes the "/webcam/" prefix before forwarding
            # the request to the backend server.
            rewrite ^/webcam/(.*)$ /$1 break;
            proxy_pass http://localhost:8090;

            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

            add_header Cache-Control "no-cache";
            add_header X-Powered-By "shellware-webcamd";
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

#### nginx-rtsps-auth.conf (RTSPS - P2/H2/X1 series)

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

        # --- Location block for the MJPEG stream ---
        location /webcam/ {
            # Enable NGINX to intercept 503 errors from the backend
            proxy_intercept_errors on;
            error_page 503 @custom_503_webcam;

            proxy_pass http://localhost:1984/api/stream.mjpeg?src=bambu_mjpeg&;

            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

            add_header Cache-Control "no-cache";
            add_header X-Powered-By "shellware-webcamd";
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

**Key Differences:**
- **MJPEG config**: Proxies to `http://localhost:8090` (webcamd daemon)
- **RTSPS config**: Proxies to `http://localhost:1984/api/stream.mjpeg?src=bambu_mjpeg&` (go2rtc)

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
├── nginx-webcamd-auth.conf
└── .htpasswd
```

**Security Notes:**
- Mount the directory as read-only (`:ro`) to prevent container modifications
- Use bcrypt (`-B` flag) for password hashing - it's more secure than MD5/SHA
- Never commit `.htpasswd` files to version control
- Consider using strong, randomly generated passwords for production deployments

## Video Stream
```dockerfile
ENV BAMBU_VIDEO_STREAM_TYPE="MJPEG-or-RTSPS"
```
You need to set which stream format to use.  The A1 and P1 series require `MJPEG` and all other machines use `RTSPS`. If you do not define this variable, the container will default to MJPEG.

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
NGINX (`8080`), it also requires exclusive access to ports `3000` (nodejs react frontend), `5000` (flask waitress backend), and
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
