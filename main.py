from machine import Pin, Timer, PWM
import random
import time

class Alarm:
    def start(self):

        self.variant = int(random.random() * 100)

        self.ledtimer = Timer()
        self.noisetimer = Timer()
        Pin(10, Pin.OUT)
        Pin(11, Pin.OUT)
        Pin(13, Pin.OUT)

        self.led1 = PWM(Pin(10))
        self.led1.freq(1000 + self.variant)
        self.led2 = PWM(Pin(11))
        self.led2.freq(1000 + self.variant)

        self.pwm = PWM(Pin(13))
        self.pwm.freq(440)

        self.duty = 0
        self.direction = 1

        self.leddirection = True
        self.ledvalue = 0
        self.ledtimer.init(period=3, mode=Timer.PERIODIC, callback=self.tickled)
        self.noisetimer.init(period=2, mode=Timer.PERIODIC, callback=self.ticknoise)

    def stop(self):
        self.ledtimer.deinit()
        self.noisetimer.deinit()
        time.sleep(0.1)
        self.led1.deinit()
        self.led2.deinit()
        self.pwm.deinit()
        Pin(10, Pin.OUT).off()
        Pin(11, Pin.OUT).off()
        Pin(13, Pin.OUT).off()

    def tickled(self, timer):
        if self.leddirection:
            self.ledvalue += 4
        else:
            self.ledvalue -= 4
        if self.ledvalue > 250:
            self.leddirection = False
            self.ledvalue = 250
        if self.ledvalue < 8:
            self.ledvalue = 8
            self.leddirection = True

        self.led1.duty_u16(self.ledvalue*self.ledvalue)
        self.led2.duty_u16(65535 - (self.ledvalue*self.ledvalue))

    def ticknoise(self, timer):
        self.duty += self.direction
        if self.duty > 200:
            self.duty = 200
            self.direction = -1
        elif self.duty < 0:
            self.duty = 50
            self.direction = 1
        self.pwm.duty_u16(self.duty * self.duty)
        self.pwm.freq(980+self.duty*3)

Pin(10, Pin.OUT).off()
Pin(11, Pin.OUT).off()
Pin(13, Pin.OUT).off()
#time.sleep(1)

alarm = Alarm()
while True:
    alarm.start()
    time.sleep(5)
    alarm.stop()
    time.sleep(5)
