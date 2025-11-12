import ssl

import paho.mqtt.client as mqtt


def create_local_ssl_context(cafile: str) -> ssl.SSLContext:
    """
    This context validates the certificate for TLS connections to local printers.
    It additionally requires calling `context.wrap_socket(sock, servername=printer_serial_number)`
    for the Server Name Indication (SNI).
    """
    context = ssl.create_default_context(cafile=cafile)
    context.verify_flags &= ~ssl.VERIFY_X509_STRICT
    return context


class MQTTSClient(mqtt.Client):
    """
    MQTT Client that supports custom certificate Server Name Indication (SNI) for TLS.
    see https://github.com/eclipse-paho/paho.mqtt.python/issues/734#issuecomment-2256633060
    """

    def __init__(self, *args, server_name=None, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._server_name = server_name

    def _ssl_wrap_socket(self, tcp_sock) -> ssl.SSLSocket:
        orig_host = self._host
        if self._server_name:
            self._host = self._server_name
        res = super()._ssl_wrap_socket(tcp_sock)
        self._host = orig_host
        return res
