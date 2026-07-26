import os
import json
import ssl
import paho.mqtt.client as mqtt
from flask import Flask, request, jsonify

app = Flask(__name__)

# ====================== НАСТРОЙКИ MQTT ======================
MQTT_HOST = "eff66a679ce34bd480bbf9946f2f2510.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USER = "smartlight"
MQTT_PASS = "Alex1208"
MQTT_TOPIC = "smartlight/lamp"

DEVICE_ID = "smartlight"

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

def on_connect(client, userdata, flags, rc):
    print("========== MQTT CONNECT ==========")
    print("RC =", rc)
    print("Connected =", rc == 0)
    print("==================================")

def on_disconnect(client, userdata, rc):
    print("MQTT DISCONNECT RC =", rc)

mqtt_client.on_connect = on_connect
mqtt_client.on_disconnect = on_disconnect

mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)

mqtt_client.tls_set(
    cert_reqs=ssl.CERT_NONE,
    tls_version=ssl.PROTOCOL_TLS_CLIENT
)

mqtt_client.tls_insecure_set(True)

mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)

mqtt_client.loop_start()


def mqtt_send(payload):

    msg = json.dumps(payload)

    print("\n========== MQTT SEND ==========")
    print("HOST =", MQTT_HOST)
    print("PORT =", MQTT_PORT)
    print("TOPIC =", MQTT_TOPIC)
    print("PAYLOAD =", msg)
    print("CONNECTED =", mqtt_client.is_connected())

    info = mqtt_client.publish(
        MQTT_TOPIC,
        payload=msg,
        qos=1,
        retain=False
    )

    info.wait_for_publish()

    print("MID =", info.mid)
    print("RC =", info.rc)
    print("PUBLISHED =", info.is_published())
    print("===============================\n")


# ====================== ХРАНИЛИЩЕ ТЕКУЩЕГО СОСТОЯНИЯ ======================
state = {
    "on": False,
    "brightness": 100,
    "color_hex": "FFFFFF",
    "scene": None,
}


def rgb_to_hex(r, g, b):
    return f"{r:02X}{g:02X}{b:02X}"


def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16)


# ====================== СЛУЖЕБНОЕ ======================

@app.route('/')
def index():
    return "OK", 200


@app.route('/on')
def manual_on():
    state['on'] = True
    mqtt_send({'power': True})
    return "OK", 200


@app.route('/off')
def manual_off():
    state['on'] = False
    mqtt_send({'power': False})
    return "OK", 200


# ====================== OAUTH (упрощённый, для навыка) ======================

@app.route('/oauth/authorize')
def oauth_authorize():
    redirect_uri = request.args.get('redirect_uri')
    state_param = request.args.get('state')
    return '', 302, {'Location': f'{redirect_uri}?code=123456&state={state_param}'}


@app.route('/oauth/token', methods=['POST'])
def oauth_token():
    return jsonify({
        "access_token": "token123",
        "token_type": "bearer",
        "expires_in": 31536000
    })


# ====================== СПИСОК УСТРОЙСТВ ======================

@app.route('/v1.0/user/devices')
def devices_list():
    request_id = request.headers.get('X-Request-Id', '')
    return jsonify({
        "request_id": request_id,
        "payload": {
            "user_id": "user1",
            "devices": [
                {
                    "id": DEVICE_ID,
                    "name": "Лента",
                    "type": "devices.types.light",
                    "capabilities": [
                        {
                            "type": "devices.capabilities.on_off",
                            "retrievable": True,
                            "reportable": False
                        },
                        {
                            "type": "devices.capabilities.range",
                            "retrievable": True,
                            "reportable": False,
                            "parameters": {
                                "instance": "brightness",
                                "unit": "unit.percent",
                                "range": {"min": 0, "max": 100, "precision": 1}
                            }
                        },
                        {
                            "type": "devices.capabilities.color_setting",
                            "retrievable": True,
                            "reportable": False,
                            "parameters": {
                                "color_model": "rgb",
                                "color_scene": {
                                    "scenes": [
                                        {"id": "party"},
                                        {"id": "movie"}
                                    ]
                                }
                            }
                        }
                    ]
                }
            ]
        }
    })


# ====================== ЗАПРОС СОСТОЯНИЯ ======================

@app.route('/v1.0/user/devices/query', methods=['POST'])
def devices_query():
    request_id = request.headers.get('X-Request-Id', '')
    r, g, b = hex_to_rgb(state['color_hex'])

    capabilities = [
        {
            "type": "devices.capabilities.on_off",
            "state": {"instance": "on", "value": state['on']}
        },
        {
            "type": "devices.capabilities.range",
            "state": {"instance": "brightness", "value": state['brightness']}
        },
        {
            "type": "devices.capabilities.color_setting",
            "state": {
                "instance": "rgb",
                "value": (r << 16) + (g << 8) + b
            }
        }
    ]

    return jsonify({
        "request_id": request_id,
        "payload": {
            "devices": [
                {
                    "id": DEVICE_ID,
                    "capabilities": capabilities
                }
            ]
        }
    })


# ====================== ВЫПОЛНЕНИЕ ДЕЙСТВИЯ ======================

@app.route('/v1.0/user/devices/action', methods=['POST'])
def devices_action():
    print("\n========== ACTION ==========")
    print(json.dumps(data, indent=4, ensure_ascii=False))
    request_id = request.headers.get('X-Request-Id', '')
    data = request.get_json()

    result_capabilities = []
    mqtt_payload = {}

    devices = data.get('payload', {}).get('devices', [])

    for device in devices:
        for cap in device.get('capabilities', []):
            cap_type = cap.get('type')
            cap_state = cap.get('state', {})
            instance = cap_state.get('instance')
            value = cap_state.get('value')

            if cap_type == 'devices.capabilities.on_off':
                state['on'] = bool(value)
                mqtt_payload['power'] = bool(value)

            elif cap_type == 'devices.capabilities.range' and instance == 'brightness':
                state['brightness'] = int(value)
                mqtt_payload['brightness'] = int(round(int(value) * 255 / 100))

            elif cap_type == 'devices.capabilities.color_setting':
                if instance == 'rgb':
                    rgb_int = int(value)
                    r = (rgb_int >> 16) & 0xFF
                    g = (rgb_int >> 8) & 0xFF
                    b = rgb_int & 0xFF
                    state['color_hex'] = rgb_to_hex(r, g, b)
                    mqtt_payload['color'] = f"#{state['color_hex']}"
                    mqtt_payload['effect'] = 'static'
                elif instance == 'scene':
                    scene = value
                    if scene == 'party':
                        mqtt_payload['effect'] = 'rainbow'
                    elif scene == 'movie':
                        mqtt_payload['effect'] = 'fire'

            result_capabilities.append({
                "type": cap_type,
                "state": {
                    "instance": instance,
                    "action_result": {"status": "DONE"}
                }
            })

    if mqtt_payload:
        print("MQTT PAYLOAD =", mqtt_payload)
        mqtt_send(mqtt_payload)

    return jsonify({
        "request_id": request_id,
        "payload": {
            "devices": [
                {
                    "id": DEVICE_ID,
                    "capabilities": result_capabilities
                }
            ]
        }
    })


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
