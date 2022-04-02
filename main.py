from machine import Pin, Timer, PWM
import random

variant=int(random.random()*100)

ledtimer = Timer()
noisetimer = Timer()

led1 = PWM(Pin(10))
led1.freq(1000+variant)
led2 = PWM(Pin(11))
led2.freq(1000+variant)

pwm = PWM(Pin(13))
pwm.freq(440)

duty = 0
direction = 1

leddirection = True
ledvalue = 0

def tickled(timer):
    global led1
    global led2
    global leddirection
    global ledvalue
    if leddirection:
        ledvalue += 4
    else:
        ledvalue -= 4
    if ledvalue > 250:
        leddirection = False
        ledvalue = 250
    if ledvalue < 8:
        ledvalue = 8
        leddirection = True

    led1.duty_u16(ledvalue*ledvalue)
    led2.duty_u16(65535 - (ledvalue*ledvalue))

def ticknoise(timer):
    global duty
    global direction
    duty += direction
    if duty > 200:
        duty = 200
        direction = -1
    elif duty < 0:
        duty = 50
        direction = 1
    pwm.duty_u16(duty * duty)
    pwm.freq(980+duty*3)

ledtimer.init(period=3, mode=Timer.PERIODIC, callback=tickled)
noisetimer.init(period=2, mode=Timer.PERIODIC, callback=ticknoise)
