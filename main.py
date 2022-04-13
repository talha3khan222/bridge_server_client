from scripts import BridgeServerClient
from multiprocessing import freeze_support

if __name__ == "__main__":
    freeze_support()
    credentials = {
        "username": None,
        "password": None
    }
    for key in credentials.keys():
        while True:
            data = (input(f"Enter your {key}; ")).strip()
            if data:
                credentials[key] = data
                break
    BridgeServerClient(credentials)
