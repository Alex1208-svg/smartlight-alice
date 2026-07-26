import ssl
import json
import paho.mqtt.client as mqtt
from config import *

def send(data):

    payload = json.dumps(data)

    print("HOST =", MQTT_HOST)
    print("PORT =", MQTT_PORT)
    print("TOPIC =", MQTT_TOPIC)
    print("USER =", MQTT_USER)
    print("PAYLOAD =", payload)

    client = mqtt.Client()

    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

    client.tls_set(tls_version=ssl.PROTOCOL_TLS)

    client.connect(MQTT_HOST, MQTT_PORT)

    r = client.publish(MQTT_TOPIC, payload)

    print("publish rc =", r.rc)

    client.disconnect()
