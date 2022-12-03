import RPi.GPIO as GPIO

class MouthServo:
    def __init__(self, pinNumber):
        self.pinNumber = pinNumber
        self.servoReady = False
        self.outputPin = None

    def start(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pinNumber, GPIO.OUT)
        self.outputPin = GPIO.PWM(self.pinNumber, 50)
        self.outputPin.start(5)

    def __del__(self):
        self.outputPin.stop()