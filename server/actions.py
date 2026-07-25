from flask import request, jsonify

from mqtt import send

def action():

    data = request.json

    value = data["payload"]["devices"][0]["capabilities"][0]["state"]["value"]

    if value:
        send("ON")
    else:
        send("OFF")

    return jsonify({

        "request_id": data["request_id"],

        "payload": {

            "devices": [

                {

                    "id": "smartlight",

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
