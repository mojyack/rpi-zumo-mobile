import os
import math
import time
import functools

import pyinotify
import cv2
import numpy as np

import config

src_filename = "plain-snapshot.jpg"
dst_filename = "scanned-snapshot.jpg"


class Detector:
    def __init__(self):
        self.detector = cv2.QRCodeDetector()

    def get_qr_info(self, image_path):
        image = cv2.imread(image_path)

        window_height = image.shape[0]
        window_width = image.shape[1]
        window_center = window_width / 2

        (
            retval,
            decoded_info,
            points,
            straight_qrcode,
        ) = self.detector.detectAndDecodeMulti(image)

        if not retval:
            return (None, None)

        for i, point in enumerate(points):
            if len(points) != 1 and decoded_info[i] != "Zumo Robot":
                continue

            point_list = point.tolist()
            left_top = point_list[0]
            left_bottom = point_list[3]

            # height of qrcode in pixels
            height_pixels = math.sqrt(
                (left_bottom[0] - left_top[0]) ** 2
                + (left_bottom[1] - left_top[1]) ** 2
            )
            # height of qrcode in mm
            height_mm = height_pixels * config.camera_sensor_height / window_height

            # distance in mm
            dist = config.qrcode_height * config.camera_focal_length / height_mm

            qrcode_center = np.sum(point, axis=0) / 4
            center_gap_pixel = float(qrcode_center[0]) - window_center
            center_gap = center_gap_pixel / (window_width / 2)

            if config.enable_scanned_channel:
                save_name = config.tmpdir + "/" + dst_filename
                save_tmpname = config.tmpdir + "/_" + dst_filename
                image = cv2.putText(
                    image,
                    f"{round(dist, 2)} mm, {round(center_gap, 2)}",
                    point[0].astype(int),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2,
                )
                cv2.imwrite(save_tmpname, image)
                os.replace(save_tmpname, save_name)

            return (dist, center_gap)

        return (None, None)


class Handler(pyinotify.ProcessEvent):
    def __init__(self, handle_qr_info):
        self.detector = Detector()
        self.handle_qr_info = handle_qr_info

    def process_IN_MOVED_TO(self, event):
        if event.pathname == config.tmpdir + "/" + src_filename:
            dist, gap = self.detector.get_qr_info(config.tmpdir + "/" + src_filename)
            self.handle_qr_info(dist, gap)


class AutoPilot:
    def __init__(self, handle_left_motor, handle_right_motor):
        self.handle_left_motor = handle_left_motor
        self.handle_right_motor = handle_right_motor

        wm = pyinotify.WatchManager()
        wm.add_watch(config.tmpdir, pyinotify.IN_MOVED_TO)
        self.notifier = pyinotify.ThreadedNotifier(
            wm, Handler(functools.partial(AutoPilot.handle_qr_info, self))
        )

    def handle_qr_info(self, dist, gap):
        if config.debug_autopilot:
            print("dist:", dist, "gap:", gap)

        if dist == None or gap == None:
            self.handle_left_motor(0)
            self.handle_right_motor(0)
            return

        remaining_dist = dist - config.algo_desired_distance
        if remaining_dist < 0:
            self.handle_left_motor(0)
            self.handle_right_motor(0)
            return
        
        base_speed = remaining_dist / config.algo_max_speed_distance * config.algo_straight_ratio
        base_speed = min(base_speed, 100)

        if config.debug_autopilot:
            print("rem", remaining_dist, "base", base_speed)
        l = +1 * gap * config.algo_curve_ratio + base_speed
        r = -1 * gap * config.algo_curve_ratio + base_speed

        self.handle_left_motor(max(-100,min(l, 100)))
        self.handle_right_motor(max(-100,min(r, 100)))

    def start(self):
        self.notifier.start()
        if config.debug_autopilot:
            print("autopilot started")

    def stop(self):
        self.notifier.stop()
        if config.debug_autopilot:
            print("autopilot stopped")


def main():
    def handle_left_motor(value):
        print("L:", value)

    def handle_right_motor(value):
        print("R:", value)

    ap = AutoPilot(handle_left_motor, handle_right_motor)
    ap.start()
    try:
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        pass
    ap.stop()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
