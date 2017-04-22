import paho.mqtt.client as mqtt
from flask import render_template, redirect
from flask import request
from flask import Flask
import os
import urlparse
import logging
import logging.handlers

app = Flask(__name__)
client = mqtt.Client()

logger = logging.getLogger('app')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
logger.addHandler(ch)


@app.route('/')
def index():
    logger.info('INDEX')
    return render_template('index.html')

@app.route('/pwm', methods=['GET', 'POST'])
def publish_duty():
    if request.method == 'POST':
        client.publish('/nazhimator/pwm', request.form['dutycycle'])
        return redirect('/', code=302)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    logger.info('Connected with result code %s', str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe('/nazhimator/pwm')

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    logger.info(msg.topic + ' ' + str(msg.payload))

def on_publish(mosq, obj, mid):
    logger.info('Publish: %s', str(mid))

def on_subscribe(mosq, obj, mid, granted_qos):
    logger.info('Subscribed: %s, %s' + str(mid), + str(granted_qos))

def on_log(mosq, obj, level, string):
    logger.info('LOG %s', string)


client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.on_subscribe = on_subscribe
client.on_log = on_log

# Parse CLOUDMQTT_URL (or fallback to localhost)
url_str = os.environ.get('CLOUDMQTT_URL', 'mqtt://localhost:1883')
url = urlparse.urlparse(url_str)

# Connect
client.username_pw_set(url.username, url.password)
client.connect(url.hostname, url.port)

client.loop()
client.subscribe('/nazhimator/pwm')

logger.info('App is starting ' + url_str)
