import os
import requests
from .config import BaseConfig
from .streamer import Streamer
import multiprocessing


class BridgeServerClient(BaseConfig):
    _config = None
    processes = []

    def __init__(self):
        self._process_configuration_file()
        self._serve_stream_process()

    def _process_configuration_file(self):
        assert os.path.exists(self._config_file_path), "Config file not found"
        with open(self._config_file_path, 'r') as file:
            self._config = self._process_configuration_blocks(file.readlines())

    def _fetch_stream_config_from_server(self, config_data):
        identifier = config_data["IDENTIFIER"]
        response = requests.get(self._server_address, params={"id": identifier})
        assert response.status_code == 200, f"Server Validation Error: Camera '{identifier}'"
        return response.json()

    def _serve_stream_to_server(self, camera_config):
        server_config = self._fetch_stream_config_from_server(camera_config)
        Streamer(camera_config, server_config)

    def _serve_stream_process(self):
        for config_block in self._config:
            self.processes.append(
                multiprocessing.Process(target=self._serve_stream_to_server, args=(config_block,), daemon=True))
        for process in self.processes:
            process.start()
        for process in self.processes:
            process.join()
