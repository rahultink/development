from gpiozero import MotionSensor
from picamera import PiCamera
#from datetime import datetimea

camera = PiCamera()
pir = MotionSensor(4)

while True:
    #filename = "{0:%Y}-{0:%m}-{0:%d}".format(now)
    pir.wait_for_motion()
    print("Motion Detected!")
    camera.start_preview()
    #camera.start_recording(filename)
    pir.wait_for_no_motion()
    camera.stop_preview()
    #camera.stop_recording(filename)
