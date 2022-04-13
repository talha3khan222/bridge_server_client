import os
from typing import List, Dict, Any
import requests
import socket


class ClientException(Exception):
    def __init__(self, data):
        self.data = data


# Declarations
class BaseConfig:
    _config_file_path = os.path.join(os.getcwd(), '.config')
    _bridge_server_ip = "3.231.203.30"
    _bridge_server_address = f"http://{_bridge_server_ip}"
    _nettbox_server_ip = "157.245.57.225"
    _nettbox_server_address = f"http://{_nettbox_server_ip}"
    _nettbox_server_api_request_headers = None
    _server_secret = "b8bf95a4-d56f-42a2-b6d3-eb5bcb65df98::78d2c88b8ad43eb26f1344051950b446"
    _cached_external_ip_address = None

    def __init__(self, credentials):
        _, data = self._login_user(credentials)
        if not _:
            raise ClientException(data)
        self._nettbox_server_api_request_headers = {"Authorization": f"Bearer {data['access']}"}

    def _login_user(self, credentials):
        endpoint = f"{self._nettbox_server_address}/api/auth/login"
        response = requests.post(endpoint, data=credentials)
        if response.status_code == 200:
            return True, response.json()
        try:
            return False, response.json()
        except:
            return False, response.text

    def _fetch_all_local_cameras(self):
        endpoint = f"{self._nettbox_server_address}/api/local_streaming/camera/all/"
        response = requests.get(endpoint, headers=self._nettbox_server_api_request_headers)
        if response.status_code == 200:
            return True, response.json()
        try:
            return False, response.json()
        except:
            return False, response.text

    @property
    def _client_address(self):
        if self._cached_external_ip_address:
            ip_address = self._cached_external_ip_address
        else:
            ip_address = requests.get('https://api.ipify.org').content.decode('utf8')
            self._cached_external_ip_address = ip_address
        name = socket.gethostname()
        return {
            "ip_address": ip_address,
            "name": name
        }
