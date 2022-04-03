from typing import Dict, Any
import imagezmq
from imutils.video import VideoStream
from .config import BaseConfig
import socket
import numpy as np


class Streamer(BaseConfig):
    _cap: VideoStream
    _sender: imagezmq.ImageSender
    _device_id: str
    _stream_uri: str
    _camera_identifier: str

    def __init__(self, camera_config: Dict[str, Any], server_config: Dict[str, Any]):
        sending_port = server_config.get("receiving_port")
        local_stream_address = camera_config.get("STREAM_ADDRESS")
        self._camera_identifier = camera_config.get("IDENTIFIER")
        self._stream_uri = server_config.get("stream_uri")
        self._cap = VideoStream(local_stream_address)
        self._sender = imagezmq.ImageSender(connect_to=f'tcp://{self._server_ip}:{sending_port}')
        self._device_id = socket.gethostname()
        self.serve_stream()

    def serve_stream(self):
        stream = self._cap.start()
        print(f"Camera '{self._camera_identifier}':: Transmission Started")
        print("You can access your stream at the link", self._stream_uri)
        while True:
            frame = stream.read()
            if not type(frame) == np.ndarray:
                continue
            self._sender.send_image(self._device_id, frame)
            print(f"Camera '{self._camera_identifier}':: Frame Sent")
