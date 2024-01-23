gpiochip = "/dev/gpiochip0"
left_motor_pwm = 1
right_motor_pwm = 0
left_motor_direction = 6
right_motor_direction = 5
min_speed = 0.1
max_speed = 0.7

# camera
tmpdir = "/tmp/card"
camera_command = "gst-launch-1.0 v4l2src ! 'image/jpeg,width=800,height=600,framerate=30/1' ! multifilesink location=snapshot.jpg"
# camera_command = "/usr/bin/true"
