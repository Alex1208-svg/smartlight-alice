from flask import jsonify

def query():

    return jsonify({

        "request_id": "1",

        "payload": {

            "devices": [

                {

                    "id": "smartlight",

                    "capabilities": [

                        {

                            "type": "devices.capabilities.on_off",

                            "state": {

                                "instance": "on",

                                "value": False

                            }

                        }

                    ]

                }

            ]

        }

    })
