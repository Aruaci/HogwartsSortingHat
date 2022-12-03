#!/usr/bin/env python3
import time

from mouthServo import MouthServo

mouthServo1 = MouthServo(17)
mouthServo1.start()

time.sleep(10)