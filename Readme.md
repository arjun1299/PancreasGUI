**Branch info**
This branch was created with threading and inter-thread communication in mind, since the previous approach of using threadpools may not have been sustainable, due to lack of flexibility and options of QThreadpool. 
___

**Install instructions**
1. pip install PyQt5
1. pip install pyserial
1. sudo apt-get install qt5-default
1. sudo gpasswd --add ${USER} dialout (In order to enable serial communication)
1. Install qtcreator
1. sudo apt-get install bluetooth libbluetooth-dev
1. pip3 install pybluez
(allow hcitool to run without sudo)
1. sudo apt-get install libcap2-bin
1. sudo setcap 'cap_net_raw,cap_net_admin+eip' `which hcitool`
1. sudo useradd -G bluetooth $USER
1. sudo apt-get install bluez
1. pip install  Adafruit-BluefruitLE
___
**Trouble shoot**
If bluetooth stops working
1. sudo hciconfig hci0 down
1. sudo hciconfig hci0 up
