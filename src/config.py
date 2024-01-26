gpiochip = "/dev/gpiochip0"
left_motor_pwm = 1
right_motor_pwm = 0
left_motor_direction = 6
right_motor_direction = 5
min_speed = 0.15
max_speed = 0.7

# camera
tmpdir = "/tmp/card"
camera_command = "gst-launch-1.0 v4l2src ! 'image/jpeg,width=800,height=600,framerate=30/1' ! multifilesink location=plain-snapshot.jpg"
# camera_command = "/usr/bin/true"

# autopilot
camera_focal_length = 28 # mm
camera_sensor_height = 3.72 # mm
qrcode_height = 120 # mm
enable_scanned_channel = True
