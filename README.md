# setup
```
pip3 install -t lib RPi.GPIO
```

# run
## server
```
sudo python3 src/daemon.py
```
in another shell
```
gst-launch-1.0 v4l2src ! "image/jpeg,width=800,height=600,framerate=30/1" ! multifilesink location=/tmp/snapshot.jpg
```
## client
open `http://IP_ADDRESS_OF_SERVER:8000/www` with browser
