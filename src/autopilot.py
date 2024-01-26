import os
import math

import pyinotify
import cv2
import numpy as np

import config

src_filename = "plain-snapshot.jpg"
dst_filename = "scanned-snapshot.jpg"
debug = False


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
            if decoded_info[i] != "Zumo Robot":
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
    def __init__(self):
        self.detector = Detector()

    def process_IN_MOVED_TO(self, event):
        if event.pathname == config.tmpdir + "/" + src_filename:
            dist, gap = self.detector.get_qr_info(
                config.tmpdir + "/" + src_filename
            )  # dist: ZumoとQRコード間の距離, gap: QRコードの重心が画像中心からどれだけ離れているか
            if debug:
                print(dist, gap)


def main():
    wm = pyinotify.WatchManager()
    wdd = wm.add_watch(config.tmpdir, pyinotify.IN_MOVED_TO)
    # pyinotify.ThreadedNotifier(wm, Handler()).start()
    pyinotify.Notifier(wm, Handler()).loop()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
