import os
import requests
from .config import BaseConfig, ClientException
from .streamer import Streamer
import multiprocessing


class BridgeServerClient(BaseConfig):
    processes = []

    def __init__(self, credentials):
        super(BridgeServerClient, self).__init__(credentials)
        self._serve_stream_process()

    def _update_instance_address_on_server(self, identifier):
        endpoint = f'{self._bridge_server_address}/client/{identifier}/address/'
        headers = {'secret-key': self._server_secret}
        response = requests.post(endpoint, data=self._client_address, headers=headers)
        print("Address Update:", identifier, response.status_code)

    def _serve_stream_to_server(self, camera_config):
        self._update_instance_address_on_server(camera_config["bridge_server_instance_id"])
        Streamer(camera_config)

    def _serve_stream_process(self):
        _, data = self._fetch_all_local_cameras()
        if not _:
            raise ClientException(data)
        print("__________________Local Cameras_____________________", *(i["label_name"] for i in data), sep="\n")
        for config in data:
            self.processes.append(
                multiprocessing.Process(target=self._serve_stream_to_server, args=(config,), daemon=True))
        for process in self.processes:
            process.start()
        for process in self.processes:
            process.join()
