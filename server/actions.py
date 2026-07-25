from flask import request
from mqtt import send

def action():

    data = request.json

    value = data["payload"]["devices"][0]["capabilities"][0]["state"]["value"]

    if value:
        send("ON")
    else:
        send("OFF")

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
                                "action_result": {
                                    "status": "DONE"
                                }
                            }
                        }
                    ]
                }
            ]
        }
    }
