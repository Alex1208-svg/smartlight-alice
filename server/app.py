from flask import Flask

from mqtt import send
from oauth import authorize, token
from devices import get_devices
from actions import action
from query import query

app = Flask(__name__)

@app.route("/")
def home():
    return "SmartLight Server"

@app.route("/success")
def success():
    return "Account linked"

@app.route("/oauth/authorize")
def oauth_authorize():
    return authorize()

@app.route("/oauth/token", methods=["POST"])
def oauth_token():
    return token()

@app.route("/v1.0/user/devices")
def devices():
    return get_devices()

@app.route("/v1.0/user/devices/query", methods=["POST"])
def devices_query():
    return query()

@app.route("/v1.0/user/devices/action", methods=["POST"])
def devices_action():
    return action()

@app.route("/on")
def on():
    send("ON")
    return "OK"

@app.route("/off")
def off():
    send("OFF")
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
