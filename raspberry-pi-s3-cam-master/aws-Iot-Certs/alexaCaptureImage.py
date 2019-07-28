from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
from picamera import PiCamera
import time

# initializing logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

#setting up MQTT details
host = "ac13cwuti4i3x-ats.iot.us-east-1.amazonaws.com"
certPath = "/home/pi/rahul/awsIot/"
clientId = "rahul-pi-demo-subscriber"
subscribeTopicName = "rahul/cam"
camera = PiCamera()

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, 8883)
myAWSIoTMQTTClient.configureCredentials("{}root-ca.pem".format(certPath), "{}72026dff66-private.pem".format(certPath), "{}72026dff66-certificate.pem.crt".format(certPath))

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
myAWSIoTMQTTClient.connect()

def customCallback(clientid, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    camera.capture('foo.jpg')


print("Subscribing to topic: ", subscribeTopicName)
myAWSIoTMQTTClient.subscribe(subscribeTopicName, 1, customCallback)
print("Subscribed to topic: ", subscribeTopicName)


# Publish message to the above topic when PIR sensor detects motion
while True:
    time.sleep(10)

myAWSIoTMQTTClient.disconnect()