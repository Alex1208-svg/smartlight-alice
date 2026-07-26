import ssl
import json
import paho.mqtt.client as mqtt
from config import *

def send(data):

    print("\n========== MQTT DEBUG ==========")

    payload = json.dumps(data)

    print("HOST    :", MQTT_HOST)
    print("PORT    :", MQTT_PORT)
    print("USER    :", MQTT_USER)
    print("TOPIC   :", MQTT_TOPIC)
    print("PAYLOAD :", payload)

    client = mqtt.Client(
        client_id="render-debug",
        protocol=mqtt.MQTTv311
    )

    client.username_pw_set(
        MQTT_USER,
        MQTT_PASSWORD
    )

    client.tls_set(
        tls_version=ssl.PROTOCOL_TLS_CLIENT
    )

    def on_connect(client, userdata, flags, rc):
        print("CONNECT RC =", rc)

    client.on_connect = on_connect

    print("Connecting...")

    client.connect(
        MQTT_HOST,
        MQTT_PORT,
        60
    )

    client.loop_start()

    import time
    time.sleep(1)

    print("Publishing...")

    info = client.publish(
        MQTT_TOPIC,
        payload,
        qos=0,
        retain=False
    )

    info.wait_for_publish()

    print("Publish rc =", info.rc)
    print("Published  =", info.is_published())

    time.sleep(1)

    client.loop_stop()
    client.disconnect()

    print("Disconnected")
    print("========== END MQTT ==========\n")
