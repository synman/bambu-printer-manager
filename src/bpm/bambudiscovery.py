"""
Hosts the discovery service which provides a wrapper for reading and parsing the Bambu Lab Discovery (SSDP) protocol.
"""
import json
import os
import sys
import threading
import time
from dataclasses import asdict, dataclass
from socket import AF_INET, SOCK_DGRAM, socket, timeout


@dataclass
class DiscoveredPrinter:
    """Represents a parsed SSDP response from a Bambu Lab printer."""
    usn: str
    """The unique service name, typically the printer serial number."""
    host: str = ""
    """The SSDP multicast address and port (e.g., 239.255.255.250:1990)."""
    server: str = ""
    """The UPnP server identifier (e.g., UPnP/1.0)."""
    location: str = ""
    """The IP address of the printer."""
    nt: str = ""
    """The notification type (e.g., urn:bambulab-com:device:3dprinter:1)."""
    nts: str = ""
    """The notification subtype (e.g., ssdp:alive)."""
    cache_control: str = ""
    """The cache control header with max-age (e.g., max-age=1800)."""
    dev_model: str = ""
    """The printer model (e.g., O1D)."""
    dev_name: str = ""
    """The printer name (e.g., 3DP-094-913)."""
    dev_connect: str = ""
    """The connection type (e.g., lan)."""
    dev_bind: str = ""
    """The binding status (e.g., free)."""
    dev_seclink: str = ""
    """The security link status (e.g., secure)."""
    dev_inf: str = ""
    """The network interface (e.g., wlan0)."""
    dev_version: str = ""
    """The device firmware version (e.g., 01.02.00.00)."""
    dev_cap: str = ""
    """The device capabilities flag (e.g., 1)."""

    @classmethod
    def fromData(cls, data: str) -> 'DiscoveredPrinter':
        """Parse SSDP data string into a  DiscoveredPrinter instance."""
        lines = data.strip().split('\n')
        parsed = {}
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower()
                value = value.strip()
                if key == 'host':
                    parsed['host'] = value
                elif key == 'server':
                    parsed['server'] = value
                elif key == 'location':
                    parsed['location'] = value
                elif key == 'nt':
                    parsed['nt'] = value
                elif key == 'nts':
                    parsed['nts'] = value
                elif key == 'usn':
                    parsed['usn'] = value
                elif key == 'cache-control':
                    parsed['cache_control'] = value
                elif key == 'devmodel.bambu.com':
                    parsed['dev_model'] = value
                elif key == 'devname.bambu.com':
                    parsed['dev_name'] = value
                elif key == 'devconnect.bambu.com':
                    parsed['dev_connect'] = value
                elif key == 'devbind.bambu.com':
                    parsed['dev_bind'] = value
                elif key == 'devseclink.bambu.com':
                    parsed['dev_seclink'] = value
                elif key == 'devinf.bambu.com':
                    parsed['dev_inf'] = value
                elif key == 'devversion.bambu.com':
                    parsed['dev_version'] = value
                elif key == 'devcap.bambu.com':
                    parsed['dev_cap'] = value
        return cls(**parsed)


class BambuDiscovery:
    """Manages the SSDP discovery thread for Bambu Lab printers."""

    def __init__(self, on_printer_discovered = None, on_discovery_ended = None, discovery_timeout: int = 15):
        self.discovery_timeout = discovery_timeout
        self._thread = None
        self._timer = None
        self._running = False
        self._discovered_printers = {}
        self._on_printer_discovered = on_printer_discovered
        self._on_discovery_ended = on_discovery_ended

    def start(self):
        """Start the discovery thread."""
        if self._thread is None or not self._thread.is_alive():
            self._running = True
            self._thread = threading.Thread(target=self._discovery_thread, name="bpm-discovery-thread")
            self._thread.start()
            self._timer = threading.Timer(self.discovery_timeout, self._stop_on_timeout)
            self._timer.start()

    def stop(self):
        """Stop the discovery thread."""
        self._running = False
        if self._timer:
            self._timer.cancel()
        if self._thread:
            self._thread.join()
        if self._on_discovery_ended:
            self._on_discovery_ended(self._discovered_printers)

    def _stop_on_timeout(self):
        """Stop discovery when timeout is reached."""
        self._running = False
        if self._thread:
            self._thread.join()
        if self._on_discovery_ended:
            self._on_discovery_ended(self._discovered_printers)

    @property
    def discovered_printers(self):
        """Get the dict of discovered printers keyed by USN."""
        return self._discovered_printers

    @property
    def running(self):
        """Check if discovery is currently running."""
        return self._running

    def _discovery_thread(self):
        with socket(AF_INET, SOCK_DGRAM) as sock:
            sock.bind(('', 2021))
            sock.settimeout(1.0)
            while self._running:
                try:
                    data, addr = sock.recvfrom(1024)
                    data_str = data.decode("utf-8")
                    try:
                        item = DiscoveredPrinter.fromData(data_str)
                        if item.usn and item.usn not in self._discovered_printers:
                            self._discovered_printers[item.usn] = item
                            if self._on_printer_discovered:
                                self._on_printer_discovered(item)
                    except TypeError:
                        # Skip malformed SSDP messages missing required fields
                        pass
                except timeout:
                    continue

if __name__ == "__main__":
    def _on_printer_discovered(printer):
        print(f"Discovered printer: {printer.dev_name} at {printer.location} with USN {printer.usn}")
    def _on_discovery_ended(printers):
        print("\r\nDiscovered printers:\r\n")
        for printer in printers:
            print(json.dumps(asdict(printer), indent=2), "\r\n")

    discovery = BambuDiscovery(on_printer_discovered=_on_printer_discovered, on_discovery_ended=_on_discovery_ended)
    discovery.start()
    try:
        while discovery._running:
            time.sleep(1)
    except KeyboardInterrupt:
        if discovery.running:
            print("Interrupting discovery...")
            discovery.stop()
            print("Discovery interrupted.")
