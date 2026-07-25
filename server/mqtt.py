import ssl
import json
import paho.mqtt.publish as publish
from config import *

def send(data):

    print("MQTT SEND:", data)

    publish.single(
        MQTT_TOPIC,
        json.dumps(data),
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

    print("MQTT OK")
