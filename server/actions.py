from flask import request, jsonify
from mqtt import send

def action():

    data = request.json

    print(data)

    device = data["payload"]["devices"][0]
    capability = device["capabilities"][0]

    state = capability["state"]

    command = {}

    if capability["type"] == "devices.capabilities.on_off":

        command["power"] = state["value"]

    elif capability["type"] == "devices.capabilities.range":

        command["brightness"] = int(state["value"] * 255 / 100)

    elif capability["type"] == "devices.capabilities.color_setting":

        rgb = state["value"]["rgb"]

        command["color"] = "#{:06X}".format(rgb)

    send(command)

    return jsonify({

        "request_id": data["request_id"],

        "payload": {

            "devices": [

                {

                    "id": "smartlight",

                    "capabilities": [

                        {

                            "type": capability["type"],

                            "state": {

                                "instance": state["instance"],

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
