import paho.mqtt.client as mqtt
from flask import render_template, redirect
from flask import request
from flask import Flask
import os
import urlparse

app = Flask(__name__)
client = mqtt.Client()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pwm', methods=['GET', 'POST'])
def publish_duty():
    if request.method == 'POST':
        client.publish("/nazhimator/pwm", request.form['dutycycle'])
        return redirect("/", code=302)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/nazhimator/pwm")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

if __name__ == "__main__":
    client.on_connect = on_connect
    client.on_message = on_message

    # Parse CLOUDMQTT_URL (or fallback to localhost)
    url_str = os.environ.get('CLOUDMQTT_URL', 'mqtt://localhost:1883')
    url = urlparse.urlparse(url_str)

    # Connect
    client.username_pw_set(url.username, url.password)
    client.connect(url.hostname, url.port)

    client.loop()

    app.run(port=5001)

    print('App is starting')

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
