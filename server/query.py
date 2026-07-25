from flask import jsonify

def query():

    return jsonify({

        "request_id":"1",

        "payload":{

            "devices":[

                {

                    "id":"smartlight",

                    "capabilities":[

                        {

                            "type":"devices.capabilities.on_off",

                            "state":{

                                "instance":"on",

                                "value":True

                            }

                        },

                        {

                            "type":"devices.capabilities.range",

                            "state":{

                                "instance":"brightness",

                                "value":100

                            }

                        },

                        {

                            "type":"devices.capabilities.color_setting",

                            "state":{

                                "instance":"rgb",

                                "value":{

                                    "rgb":16777215

                                }

                            }

                        }

                    ]

                }

            ]

        }

    })
