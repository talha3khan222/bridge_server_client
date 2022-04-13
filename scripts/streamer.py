from typing import Dict, Any
import imagezmq
from imutils.video import VideoStream
from .config import BaseConfig
import socket
import numpy as np
import cv2


class Streamer(BaseConfig):
    _cap: VideoStream
    _sender: imagezmq.ImageSender
    _device_id: str
    _local_stream_address: str
    _camera_identifier: str
    _target_width = 400

    def __init__(self, camera_config: Dict[str, Any]):
        sending_port = camera_config["local_streaming_receiving_port"]
        self._local_stream_address = camera_config["address"]
        self._camera_identifier = camera_config["label_name"]
        self._cap = VideoStream(self._local_stream_address)
        address = f'tcp://{self._bridge_server_ip}:{sending_port}'
        self._sender = imagezmq.ImageSender(connect_to=address)
        self._device_id = socket.gethostname()
        self.serve_stream()

    def serve_stream(self):
        stream = self._cap.start()
        print(f"Camera '{self._camera_identifier}':: Transmission Started")
        print("Sending Streams From", self._local_stream_address)
        while True:
            frame = stream.read()
            if not type(frame) == np.ndarray:
                continue
            # print(frame.shape)
            height, width, *_ = frame.shape
            # print(width, "by", height, "-----Initial Size")
            if width <= self._target_width:
                scaled_frame = frame
            else:
                reduction_ratio = width / self._target_width
                new_width = int(width / reduction_ratio)
                new_height = int(height / reduction_ratio)
                # print(new_width, "by", new_height, "-----Reduced Size")
                scaled_frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)
            self._sender.send_image(self._device_id, scaled_frame)
            print(f"Camera '{self._camera_identifier}':: Frame Sent")
