import os
import json
import ssl
import time
import paho.mqtt.publish as publish
from flask import Flask, request, jsonify

app = Flask(__name__)

# ====================== НАСТРОЙКИ MQTT ======================
MQTT_HOST = "eff66a679ce34bd480bbf9946f2f2510.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_USER = "smartlight"
MQTT_PASS = "Alex1208"
MQTT_TOPIC = "smartlight/lamp"

DEVICE_ID = "smartlight"

# Названия цветов, которые присылает Алиса вместо числового RGB
NAMED_COLORS = {
    "red": "FF0000", "orange": "FF8000", "yellow": "FFFF00",
    "green": "00FF00", "emerald": "00FF80", "turquoise": "00FFFF",
    "cyan": "00FFFF", "blue": "0000FF", "violet": "8000FF",
    "purple": "FF00FF", "pink": "FF0080", "raspberry": "FF0040",
    "white": "FFFFFF", "warm_white": "FFF4E0", "cold_white": "E0F0FF",
}

# ====================== ХРАНИЛИЩЕ ТЕКУЩЕГО СОСТОЯНИЯ ======================
# effect: "static" | "rainbow" | "fire"
state = {
    "on": False,
    "brightness": 100,
    "color_hex": "FFFFFF",
    "effect": "static",
}


def rgb_to_hex(r, g, b):
    return f"{r:02X}{g:02X}{b:02X}"


def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return int(hex_str[0:2], 16), int(hex_str[2:4], 16), int(hex_str[4:6], 16)


def publish_full_state():
    """Публикует ПОЛНОЕ состояние лампы одним retained-сообщением.
    Благодаря retain=True, при любом переподключении ESP8266 брокер
    сразу отдаёт этот снимок состояния — без опроса и дополнительной логики."""
    payload = {
        "power": state['on'],
        "brightness": int(round(state['brightness'] * 255 / 100)),
        "color": f"#{state['color_hex']}",
        "effect": state['effect'],
    }
    msg = json.dumps(payload)
    print("MQTT SEND (full state):", msg)
    try:
        publish.single(
            MQTT_TOPIC,
            payload=msg,
            qos=1,
            retain=True,
            hostname=MQTT_HOST,
            port=MQTT_PORT,
            auth={'username': MQTT_USER, 'password': MQTT_PASS},
            tls={'cert_reqs': ssl.CERT_NONE, 'tls_version': ssl.PROTOCOL_TLS_CLIENT},
            client_id="render-" + str(int(time.time() * 1000)),
        )
        print("MQTT publish OK")
    except Exception as e:
        print("MQTT publish FAILED:", e)


# ====================== СЛУЖЕБНОЕ ======================

@app.route('/')
def index():
    return "OK", 200


@app.route('/on')
def manual_on():
    state['on'] = True
    publish_full_state()
    return "OK", 200


@app.route('/off')
def manual_off():
    state['on'] = False
    publish_full_state()
    return "OK", 200


# ====================== OAUTH ======================

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
    data = request.get_json()
    request_id = request.headers.get('X-Request-Id', '')

    print("\n========== ACTION ==========")
    print(json.dumps(data, indent=2, ensure_ascii=False))

    result_capabilities = []
    devices = data.get('payload', {}).get('devices', [])

    for device in devices:
        for cap in device.get('capabilities', []):
            cap_type = cap.get('type')
            cap_state = cap.get('state', {})
            instance = cap_state.get('instance')
            value = cap_state.get('value')

            if cap_type == 'devices.capabilities.on_off':
                state['on'] = bool(value)

            elif cap_type == 'devices.capabilities.range' and instance == 'brightness':
                state['brightness'] = int(value)

            elif cap_type == 'devices.capabilities.color_setting':
                if instance == 'rgb':
                    rgb_int = int(value)
                    r = (rgb_int >> 16) & 0xFF
                    g = (rgb_int >> 8) & 0xFF
                    b = rgb_int & 0xFF
                    state['color_hex'] = rgb_to_hex(r, g, b)
                    state['effect'] = 'static'

                elif instance == 'color':
                    # Алиса иногда шлёт название цвета строкой, а не число RGB
                    hex_color = NAMED_COLORS.get(str(value).lower())
                    if hex_color:
                        state['color_hex'] = hex_color
                        state['effect'] = 'static'

                elif instance == 'scene':
                    if value == 'party':
                        state['effect'] = 'rainbow'
                    elif value == 'movie':
                        state['effect'] = 'fire'

            result_capabilities.append({
                "type": cap_type,
                "state": {
                    "instance": instance,
                    "action_result": {"status": "DONE"}
                }
            })

    # Всегда публикуем ПОЛНОЕ состояние одним retained-сообщением
    publish_full_state()

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
