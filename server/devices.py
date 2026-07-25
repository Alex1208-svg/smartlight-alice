from flask import jsonify

def devices():

    return jsonify({

        "request_id":"1",

        "payload":{

            "user_id":"1",

            "devices":[

                {

                    "id":"smartlight",

                    "name":"Лента",

                    "type":"devices.types.light",

                    "capabilities":[

                        {

                            "type":"devices.capabilities.on_off"

                        },

                        {

                            "type":"devices.capabilities.range",

                            "retrievable":True,

                            "parameters":{

                                "instance":"brightness",

                                "unit":"unit.percent",

                                "range":{

                                    "min":1,

                                    "max":100,

                                    "precision":1

                                }

                            }

                        },

                        {

                            "type":"devices.capabilities.color_setting",

                            "retrievable":True,

                            "parameters":{

                                "color_model":"rgb"

                            }

                        }

                    ]

                }

            ]

        }

    })
