import ssl
import json
import paho.mqtt.client as mqtt
from config import *

def send(data):

    print("===== NEW MQTT.PY =====")
    
    payload = json.dumps(data)

    print("HOST =", MQTT_HOST)
    print("PORT =", MQTT_PORT)
    print("USER =", MQTT_USER)
    print("TOPIC =", MQTT_TOPIC)
    print("PAYLOAD =", payload)

    client = mqtt.Client(
        client_id="render-debug",
        protocol=mqtt.MQTTv311
    )

    client.username_pw_set(MQTT_USER, MQTT_PASSWORD)

    client.tls_set(
        tls_version=ssl.PROTOCOL_TLS_CLIENT
    )

    client.connect(MQTT_HOST, MQTT_PORT, 60)

    print("CONNECTED")

print("==========================")
print("HOST =", MQTT_HOST)
print("PORT =", MQTT_PORT)
print("USER =", MQTT_USER)
print("TOPIC =", MQTT_TOPIC)
print("PAYLOAD =", payload)
print("==========================")
    
    rc = client.publish(
        MQTT_TOPIC,
        payload,
        qos=0,
        retain=False
    )

    client.loop(1)

    print("publish rc =", rc.rc)

    client.disconnect()
