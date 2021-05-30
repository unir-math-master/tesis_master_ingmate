# Jetson Nano SetUp

[Download](https://developer.nvidia.com/embedded/downloads#?search=RPi%20IMX477%20Support%20Nano%202GB) Jetson Image with Support for Pi Camera


## Software Installation

#### Upgrade software
```
sudo apt-get update
sudo apt-get upgrade
```

Reboot the system:
```
sudo reboot
```

#### Install pip
```
sudo apt install python3-pip
```

### Install ROS
For the Jetson nano follow these [steps](https://elinux.org/Jetson_Zoo).
 
### CircuitPython Installation of GPS Library

CircuitPython initial setup gide can be found [here](https://learn.adafruit.com/circuitpython-libraries-on-linux-and-the-nvidia-jetson-nano/initial-setup).


GPS Library installation:
```
sudo pip3 install adafruit-circuitpython-gps
```

After install, if the GPS is connected by the USB-Serial converter we need to grant permisions for `ttyUSB0`
```
sudo usermod -aG　dialout <user>
```

### Raspberry Pi Camera Module V2

https://github.com/JetsonHacksNano/CSI-Camera

`gst-launch-1.0 nvarguscamerasrc ! nvoverlaysink`

#### OLED Screen
https://github.com/JetsonHacksNano/installPiOLED
