from flask import request, jsonify
from mqtt import send

def action():

    data = request.get_json(force=True)

    print("REQUEST:", data)

    try:
        device = data["payload"]["devices"][0]
        state = device["capabilities"][0]["state"]
        value = state["value"]

        if value:
            send("ON")
        else:
            send("OFF")

        return jsonify({
            "request_id": data.get("request_id", ""),
            "payload": {
                "devices": [
                    {
                        "id": device["id"],
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
        })

    except Exception as e:
        print("ERROR:", e)
        raise
