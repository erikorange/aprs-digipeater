# aprs-digipeater

## Hardware
This is an APRS digipeater consisting of:
- Yaesu FT-2600M 2m 60W mobile transceiver
- direwolf running on a Raspberry Pi 3B+
- Syba USB Stereo Soundcard adapter
- VFAN USB GPS receiver
- a custom interface board

The FT-2600M has a DB9 port which provides access to:
- Tx audio in
- Rx audio out
- PTT triggering when shorted to GND
- GND

## Design
direwolf is configured to use a GPIO output to trigger PTT. The interface board uses an optioisolator to electrically isolate the GPIO output from the DB9 PTT pin on the FT-2600M.  The Rx audio out from the DB9 is not used because the audio level is too low.  The FT-26600M speaker out is instead connected to the Pi's external soundcard input.  The external soundcard output is connected to the DB9 Tx audio in.

The interface board also has:
- Red LED - illuminates when direworlf is transmitting
- Green LED - stays illuminated as long as direwolf is running
- Yellow LED - indicates an OS shutdown is in progress
- Pushbutton - hold for up to 3 seconds to initiate an OS shutdown

## Custom Software
digipeater-mon.py starts via .bashrc which executes automatically because the Pi is configured to login upon boot.  The software will flash the green and yellow LEDs alternately to indicate the Pi has successfully booted and .bashrc is executing.  When the pushbutton is pressed, the green and yellow LEDS will flash in unison to indicate the OS is shutting down.  During normal operation, the software will periodically check if the direwolf process is running and keep the green LED illuminated. If the direwolf process is not detected then the green LED will be extinguished.

## Raspberry Pi OS Build
```
sudo apt-get update
sudo apt-get -y upgrade
sudo raspi-config
    System Options -> Audio -> USB PnP Sound device
    System Options -> Boot / Auto Login -> Console Autologin
    Advanced Options -> Expand Filesystem
<reboot>
```

## direwolf prerequisite install
```
sudo apt-get install git
sudo apt-get install cmake
sudo apt-get install libasound2-dev
sudo apt-get install libudev-dev
sudo apt-get install gpiod
sudo apt-get install libgpod-dev

dpkg -l | grep gps
```
if no gpsd or libgps-dev packages:
```
sudo apt-get install gpsd
sudo apt-get install libgps-dev
```

## direwolf build
The dev branch of direwolf is used in support of the GPIO fix required for later versions of the Raspberry Pi OS.
```
cd ~
git clone https://www.github.com/wb2osz/direwolf
cd direwolf
git checkout dev
mkdir build && cd build
cmake -DUNITTEST=1 ..
make -j4
make test
sudo make install

cd ~
mkdir aprslogs
```


## python support for process monitoring
```
sudo apt install python3-psutil
```
Copy these files to /home/pi
- direwolf.conf
- digipeater-mon.py
<br>

Append this script to .bashrc
```
if [ -n "$SSH_CLIENT" ]; then
  echo "Remote login detected"
else
  echo "starting digipeater-mon"
  python digipeater-mon.py > digipeater-mon.log 2>&1 &
  echo "starting direwolf"
  direwolf -t 0 -l /home/pi/aprslogs > direwolf_console.log 2>&1 &
fi
```

## tools for testing soundcard and GPS
```
speaker-test -c2 -twav 2
aplay -l
arecord -l
alsamixer -c l

gpioinfo
cgps -s
```



