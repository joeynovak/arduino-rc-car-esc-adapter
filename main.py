# Example using PWM to fade an LED.

import time
from machine import Pin, PWM

A1 = PWM(Pin(0))
A2 = PWM(Pin(1))
B1 = PWM(Pin(2))
B2 = PWM(Pin(3))

steeringPin = Pin(7)
throttlePin = Pin(6)
# -255 to +255
def leftControl(speed):
    speed = int(speed)
    if(speed > 255):
        speed = 255
    if speed < -255:
        speed = -255
        
    print ("Left " + str(speed))
    
    if speed < 0:
        A1.duty_u16(0)
        A2.duty_u16(abs(speed) * 256)
    else:
        A1.duty_u16(abs(speed) * 256)
        A2.duty_u16(0)
    
def rightControl(speed):
    speed = int(speed)
    if(speed > 255):
        speed = 255
    if speed < -255:
        speed = -255
        
    print ("Right " + str(speed))
    
    if speed < 0:
        B1.duty_u16(0)
        B2.duty_u16(abs(speed) * 256)
    else:
        B1.duty_u16(abs(speed) * 256)
        B2.duty_u16(0)
    
def getPulseWidth(pin):
    while pin.value() == 0:
      pass
    start = time.ticks_us()
    while pin.value() == 1:
        pass
    end = time.ticks_us()
    duration = end - start
    if duration > 1490 and duration < 1510:
        duration = 1500
    
    return duration
        
leftControl(0)
rightControl(0)

while True:    
    steering = 0
        
    throttlePulseWidth = getPulseWidth(throttlePin)
    throttle = (float(throttlePulseWidth)-1500) / 2
    
    steeringPulseWidth = getPulseWidth(steeringPin)
    steering = (float(steeringPulseWidth) - 1500) / 2
    
    print ("Throttle " + str(throttle))
    print ("Steering " + str(steering))
    
    total = throttle + steering
    
    left = throttle
    right = throttle
    
    left = left - steering
    right = right + steering
    
    leftControl(left)
    rightControl(right)