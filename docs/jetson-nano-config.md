# Jetson Nano SetUp

[Download](https://developer.nvidia.com/embedded/downloads#?search=RPi%20IMX477%20Support%20Nano%202GB) Jetson Image with Support for Pi Camera


## Installation

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

#### CircuitPython Installation of GPS Library
`sudo pip3 install adafruit-circuitpython-gps`

#### Raspberry Pi Camera Module V2

https://github.com/JetsonHacksNano/CSI-Camera

`gst-launch-1.0 nvarguscamerasrc ! nvoverlaysink`

#### OLED Screen
https://github.com/JetsonHacksNano/installPiOLED
