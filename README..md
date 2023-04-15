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

## License

This project is released under the MIT License.


