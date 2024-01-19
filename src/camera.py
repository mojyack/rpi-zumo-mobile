import os
import subprocess
import signal


class Camera:
    def __init__(self, tmpdir, camera_command):
        self.tmpdir = tmpdir
        self.camera_command = camera_command
        os.makedirs(tmpdir, exist_ok=True)

    def start(self):
        self.process = subprocess.Popen(
            f"cd '{self.tmpdir}' && {self.camera_command}", shell=True
        )

    def stop(self):
        self.process.send_signal(signal.SIGINT)
        self.process.wait()

    # we do not delete tmpdir, to prevent an accident
