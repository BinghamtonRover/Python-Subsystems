# Subsystems
A bridge between the UDP network and the CAN bus

## Raspberry Pi setup

Here is a comprehensive list of how to set up this Pi from a clean image

1. Connect to WiFi: 
  - SSID: `mydevicesbing`, no password
  - Disable MAC randomization: 
    ```bash
    printf "[connection]\nwifi.mac-address-randomization=1\n\n[device]\nwifi.scan-rand-mac-address=no\n" | sudo tee /etc/NetworkManager/conf.d/100-disable-wifi-mac-randomization.conf
	```
  - Register this device's MAC address at [mydevices.binghamton.edu](mydevices.binghamton.edu)
  - Reboot and verify that WiFi has internet
2. Setup the [Subsystems repository](https://github.com/BinghamtonRover/Subsystems):
  - Clone the repository:
	```bash
	git clone https://github.com/BinghamtonRover/Subsystems rover/subsystems
	git switch -c pi
	```
  - On your PC, set up this Pi as a Git remote:
	```bash
	cd path/to/your/subsystems
	git remote add pi pi@192.168.1.20:~/rover/subsystems
	git fetch
	cd network
	git remote add pi pi@192.168.1.20:~/rover/subsystems/network
	git fetch
	```
3. Configure CAN
  - Add the following to the end of /boot/config.txt
	```toml
	[all]
	enable_uart=1
	
	# STORE-BOUGHT CAN HAT
	# dtparam=spi=on
	# dtoverlay=mcp2515-can0,oscillator=12000000,interrupt=25,spimaxfrequency=2000000

	# 10/22/2022 PI HAT
	dtparam=spi=on
	dtoverlay=mcp2510-can0,oscillator=16000000,interrupt=12
	```
4. Install dependencies: 
  - Install Python libraries: 
	```bash
	cd rover/subsystems
	pip3 install -r requirements.txt
	sudo pip3 install -r requirements.txt
	```
	These commands will take a while. The `sudo` variant is needed to run the subsystems program as root
  - Install OpenCV, needed for the video program
	```bash
	sudo apt-get update
	sudo apt-get install build-essential cmake pkg-config libjpeg-dev libtiff5-dev libjasper-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libfontconfig1-dev libcairo2-dev libgdk-pixbuf2.0-dev libpango1.0-dev libgtk2.0-dev libgtk-3-dev libatlas-base-dev gfortran libhdf5-dev libhdf5-serial-dev libhdf5-103 python3-pyqt5 python3-dev -y
	```
  - Install [can-utils](https://github.com/linux-can/can-utils/releases/latest): 
	```bash
	sudo apt-get install can-utils
	```
	Now you can use `candump` and `cansend`
5. Convenience scripts
  - Setup a script to start the subsystems program in `~/subsystems.sh`:
	```bash
	#!/bin/bash
	echo Starting subsystems...
	sleep 1
	sudo pigpiod
	sleep 1
	cd /home/pi/rover/subsystems
	python3 -m bin.main
	```
  - Setup a program to stop the subsystems program in `~/kill-subsystems.sh`:
	```bash
	#!/bin/bash
	sudo kill `pgrep -f "python3 -m bin.main"`
	```
  - Add the following service to a new file `/etc/systemd/system/subsystems.service`:
	```toml
	[Unit]
	Description=Rover Subsystems
	After=network-online.target

	[Service]
	ExecStart=/home/pi/subsystems.sh
	ExecStop=/home/pi/kill-subsystems.sh
	TimeoutStopSec=5
	User=pi

	[Install]
	WantedBy=multi-user.target
	```
  - Test the service:
	Then run `sudo systemctl enable subsystems.service`
6. Setup the Pi's static IP address over Ethernet
  - Right click on the network icon, configure the `eth0` interface
  - Set IP=`192.168.1.20`, router=`192.168.1.2`
  - In `Preferences > Raspberry Pi Configuration > Interfaces`, enable `SSH`
  - Verify that you can `ssh` into `pi@192.168.1.20` over Ethernet
