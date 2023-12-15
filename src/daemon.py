import sys
import os
import tty
import termios

sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))
import RPi.GPIO as GPIO

import config
import pwm

print(GPIO.RPI_INFO)

class Motor():
    pwm_period = 5000000

    def __init__(self, pwm_pin, dir_pin):
        self.pwm_pin = pwm_pin
        self.dir_pin = dir_pin

        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.output(self.dir_pin, GPIO.HIGH)

        if config.use_soft_pwm:
            GPIO.setup(self.pwm_pin, GPIO.OUT)
            self.pwm = GPIO.PWM(self.pwm_pin, 200)
            self.pwm.start(0)
        else:
            self.pwm = pwm.PWMDevice(pwm_pin)
            self.pwm.set_enabled(0)
            self.pwm.set_inversed(0)
            self.pwm.set_duty(0)
            self.pwm.set_period(Motor.pwm_period)
            self.pwm.set_enabled(1)
    
    def change_speed(self, speed):
        if speed < 0:
            GPIO.output(self.dir_pin, GPIO.HIGH)
            speed = -speed
        else:
            GPIO.output(self.dir_pin, GPIO.LOW)
            pass

        if config.use_soft_pwm:
            self.pwm.ChangeDutyCycle(speed)
        else:
            self.pwm.set_enabled(0)
            self.pwm.set_duty(int(speed * Motor.pwm_period / 100))
            self.pwm.set_enabled(1)

GPIO.setmode(GPIO.BCM)

motor_l = Motor(config.left_motor_pwm, config.left_motor_direction)
motor_r = Motor(config.right_motor_pwm, config.right_motor_direction)

import webui

def handle_left_motor(value):
    global motor_l
    motor_l.change_speed(value)

def handle_right_motor(value):
    global motor_r
    motor_r.change_speed(value)

webui.start_server(handle_left_motor, handle_right_motor)

del motor_l
del motor_r

GPIO.cleanup()
