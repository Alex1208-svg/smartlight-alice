import ssl
import paho.mqtt.publish as publish

from config import *

def send(command):

    print("MQTT SEND:", command)

    publish.single(
        MQTT_TOPIC,
        command,
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
