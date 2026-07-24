from flask import Flask
from mqtt import send

app = Flask(__name__)


@app.route("/")
def home():
    return "SmartLight Server"


@app.route("/on")
def on():
    send("ON")
    return "OK"


@app.route("/off")
def off():
    send("OFF")
    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)