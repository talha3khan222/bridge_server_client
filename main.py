from imutils.video import VideoStream
import imagezmq
import socket
import numpy as np
import os
import requests

config_file_path = os.path.join(os.getcwd(), '.config')
server_address = "http://3.231.203.30/config"
assert os.path.exists(config_file_path), "Config file not found"
with open(config_file_path, 'r') as file:
    data = list(i.replace('\n', '').split("=") for i in file.readlines())
    data = dict(data)
needed_fields = ["IDENTIFIER", "STREAM_ADDRESS"]
for field in needed_fields:
    assert data.get(field), f"'{field}' is required in config file"
response = requests.get(server_address, params={"id": data["IDENTIFIER"]})
assert response.status_code == 200, "request to server error"
response_data = response.json()
sending_port = response_data.get("receiving_port")
stream_uri = response_data.get("stream_uri")
# change this to your stream address
path = data.get("STREAM_ADDRESS")
cap = VideoStream(path)
sender = imagezmq.ImageSender(connect_to=f'tcp://3.231.203.30:{sending_port}')
cam_id = socket.gethostname()
stream = cap.start()
print("Transmission Started")
print("You can access your stream at the link", stream_uri)
while True:
    frame = stream.read()
    if not type(frame) == np.ndarray:
        continue
    sender.send_image(cam_id, frame)
    # print("Frame Sent")
