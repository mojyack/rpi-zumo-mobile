import sys

import config
import gpio
import pwm


class Motor:
    pwm_period = int(1000000000 / 200000)

    def __init__(self, pwm_pin, dir_pin):
        self.phase = gpio.GPIOPin(config.gpiochip, "car-daemon", dir_pin)

        self.enable = pwm.PWMDevice(pwm_pin)
        self.enable.set_enabled(0)
        self.enable.set_inversed(0)
        self.enable.set_duty(0)
        self.enable.set_period(Motor.pwm_period)
        self.enable.set_enabled(1)

    # -100 <= speed <= 100
    def change_speed(self, speed):
        if speed < 0:
            self.phase.set_active(True)
            speed = -speed
        else:
            self.phase.set_active(False)
        # 0 <= speed <= 100

        speed /= 100
        # 0.0 <= speed <= 1.0

        speed = speed * (config.max_speed - config.min_speed) + config.min_speed
        # min_speed <= speed <= max_speed

        self.enable.set_enabled(0)
        self.enable.set_duty(int(speed * Motor.pwm_period))
        self.enable.set_enabled(1)


motor_l = Motor(config.left_motor_pwm, config.left_motor_direction)
motor_r = Motor(config.right_motor_pwm, config.right_motor_direction)

import camera

cam = camera.Camera(config.tmpdir, config.camera_command)

import webui


def handle_left_motor(value):
    global motor_l
    motor_l.change_speed(value)

    if config.debug_daemon:
        print("L:", value)


def handle_right_motor(value):
    global motor_r
    motor_r.change_speed(value)

    if config.debug_daemon:
        print("R:", value)


import autopilot

ap = autopilot.AutoPilot(handle_left_motor, handle_right_motor)

ap.start()

cam.start()
webui.start_server(handle_left_motor, handle_right_motor)
cam.stop()

ap.stop()

del motor_l
del motor_r
