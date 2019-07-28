from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
from gpiozero import MotionSensor
from picamera import PiCamera
import datetime
import logging

# initializing logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

#initialize camera and PIR sensor
camera = PiCamera()
pir = MotionSensor(4)

#setting up MQTT details
host = "ac13cwuti4i3x-ats.iot.us-east-1.amazonaws.com"
certPath = "/home/pi/rahul/awsIot/"
clientId = "rahul-pi-demo-publisher"
topic = "demo/topic"

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

# Publish message to the above topic when PIR sensor detects motion
while True:
    now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    logger.info("try to publish:{}".format(now))
    pir.wait_for_motion()
    logger.info("Motion Detected!")
    #print("Motion Detected!")
    message = {}
    message['message'] = "Motion-Detected-in-living-room"
    message['header'] = "living-room-sensor"
    messageJson = json.dumps(message)
    myAWSIoTMQTTClient.publish(topic, messageJson, 1)
    logger.info('Published topic %s: %s\n' % (topic, messageJson))
    # print('Published topic %s: %s\n' % (topic, messageJson))
myAWSIoTMQTTClient.disconnect()