from flask import request

def get_devices():
    return {
        "request_id": request.headers.get("X-Request-Id", ""),
        "payload": {
            "user_id": "alex",
            "devices": [
                {
                    "id": "lamp",
                    "name": "Умная лента",
                    "type": "devices.types.light",
                    "capabilities": [
                        {
                            "type": "devices.capabilities.on_off"
                        }
                    ]
                }
            ]
        }
    }
