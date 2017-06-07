#!/usr/bin/python

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys
import time
import Adafruit_DHT

# Custom MQTT message callback
def customCallback(client, userdata, message):
        print("Received a new message: ")
        print(message.payload)
        print("from topic: ")
        print(message.topic)
        print("--------------\n\n")


# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
myAWSIoTMQTTClient = AWSIoTMQTTClient("basicPubSub")
myAWSIoTMQTTClient.configureEndpoint("a2exf2ut0yar8e.iot.us-east-1.amazonaws.com", 8883)
#myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
myAWSIoTMQTTClient.configureCredentials("root-CA.crt", "Atul-pi3.private.key", "Atul-pi3.cert.pem")

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
#myAWSIoTMQTTClient.subscribe("Atul-pi3/dht11", 1, customCallback)
time.sleep(2)

print('connected to AWS IOT...')

while True:
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)

    print 'Temp: {0:0.1f} C  Humidity: {1:0.1f} %'.format(temperature, humidity)
    
    msg = '"Temp": "{0:0.1f} C" , "Humidity": "{1:0.1f} %"'.format(temperature, humidity)
    myAWSIoTMQTTClient.publish("Atul-pi3/dht11", msg, 1)

    print('Sleeping...')
    time.sleep(1)