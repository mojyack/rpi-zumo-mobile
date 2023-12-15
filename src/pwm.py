import sys

sysfs = "/sys/class/pwm/pwmchip0"

class PWMDevice():
    def sysfs_write(file, value):
        open(f"{sysfs}/{file}", "w").write(str(value))

    def __init__(self, num):
        self.number = num
        PWMDevice.sysfs_write("export", self.number)

    def __del__(self):
        PWMDevice.sysfs_write("unexport", self.number)

    def set_enabled(self, flag):
        PWMDevice.sysfs_write(f"pwm{self.number}/enable", flag)

    def set_inversed(self, flag):
        PWMDevice.sysfs_write(f"pwm{self.number}/polarity", "inversed" if flag else "normal")

    def set_period(self, period):
        PWMDevice.sysfs_write(f"pwm{self.number}/period", period)

    def set_duty(self, duty):
        PWMDevice.sysfs_write(f"pwm{self.number}/duty_cycle", duty)
