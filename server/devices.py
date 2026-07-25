from flask import jsonify

def get_devices():

    return jsonify({
        "request_id": "1",
        "payload": {
            "user_id": "user1",
            "devices": [
                {
                    "id": "smartlight",
                    "name": "Лента",
                    "type": "devices.types.light",

                    "capabilities": [
                        {
                            "type": "devices.capabilities.on_off",
                            "retrievable": True
                        }
                    ]
                }
            ]
        }
    })
