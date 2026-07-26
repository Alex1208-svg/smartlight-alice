import ssl
import json
import paho.mqtt.publish as publish

from config import *


def send(data):

    payload = json.dumps(data)

    print("\n=========== MQTT DEBUG ===========")
    print("HOST     :", MQTT_HOST)
    print("PORT     :", MQTT_PORT)
    print("USER     :", MQTT_USER)
    print("PASSWORD :", MQTT_PASSWORD)
    print("TOPIC    :", MQTT_TOPIC)
    print("PAYLOAD  :", payload)

    try:

        publish.single(
            topic=MQTT_TOPIC,
            payload=payload,
            hostname=MQTT_HOST,
            port=MQTT_PORT,
            auth={
                "username": MQTT_USER,
                "password": MQTT_PASSWORD
            },
            tls={
                "tls_version": ssl.PROTOCOL_TLS
            }
        )

        print("PUBLISH OK")

    except Exception as e:

        print("MQTT ERROR")
        print(e)

    print("==================================\n")
