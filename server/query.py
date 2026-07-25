from flask import request

def query():

    return {
        "request_id": request.headers.get("X-Request-Id", ""),
        "payload": {
            "devices": [
                {
                    "id": "lamp",
                    "capabilities": [
                        {
                            "type": "devices.capabilities.on_off",
                            "state": {
                                "instance": "on",
                                "value": True
                            }
                        }
                    ]
                }
            ]
        }
    }
