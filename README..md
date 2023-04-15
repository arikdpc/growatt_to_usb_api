# Growatt Inverter Monitoring

This project provides a Python script to monitor Growatt inverters using the Modbus protocol and Flask to expose the data via an HTTP API.

## Prerequisites

- Python 3.x
- A USB to Modbus RTU converter connected to the Growatt inverter
- Docker (optional, for containerizing the application)

## Installation

1. Clone the repository:

git clone https://github.com/yourusername/growatt-inverter-monitoring.git
cd growatt-inverter-monitoring


2. Install the required Python packages:

pip install -r requirements.txt


## Usage

1. Update the `inverterusbport1` variable in the Python script with the correct USB device path:

inverterusbport1 = "/dev/ttyUSB0"

2. Run the script:

python growatt_inverter_monitoring.py


3. Access the inverter data via the HTTP API by navigating to `http://localhost:5000/results` in your web browser or using a tool like `curl`:

curl http://localhost:5000/results


## Docker (Optional)

1. Build the Docker image:

docker build -t my-python-script .


2. Run the Docker container:

docker run -d --name my-python-script-container -p 5000:5000 --device /dev/ttyUSB0:/dev/ttyUSB0 my-python-script


Replace `/dev/ttyUSB0` with the correct device path you found in step 1. This command maps the USB device from the host system to the container and makes it accessible at the same device path.


## Driver issues troubleshoot

1. Check if the USB device is recognized by the system:
   $ lsusb

2. Identify the device path of the USB device:
   $ ls /dev/tty*

3. If the driver is not installed, find the driver for your specific device, download it and install it. In our case, we had to compile and install a kernel module:
   $ cd epsolar-tracer/xr_usb_serial_common-1a
   $ make
   $ sudo make install

4. If the 'modinfo' command is not found, install the 'kmod' package:
   $ sudo apt-get install kmod

5. Check if the kernel module is loaded:
   $ modinfo <module-name>

6. If the kernel module is not loaded, try loading it manually:
   $ sudo modprobe <module-name>

7. Recheck the device path of the USB device:
   $ ls /dev/tty*

8. Update the device path in the 'script.py' file if necessary.

9. Run the script to test the connection:
   $ python3 script.py

10. If you encounter permission issues, check the permissions of the device:
   $ ls -l /dev/tty*

11. If necessary, add your user to the 'dialout' group:
   $ sudo usermod -a -G dialout <username>

12. Reboot the system or log out and log back in for the changes to take effect.

13. Run the script again to test the connection:
   $ python3 script.py


