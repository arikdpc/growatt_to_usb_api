#!/usr/bin/env python3

import time
import datetime
import os
import sys
from pymodbus.exceptions import ModbusIOException
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from flask import Flask, jsonify
# import threading

# Full path of the file
file_path = 'fields.json'


interval = 0

numinverters = 1
inverterusbport1 = "/dev/ttyUSB0"
#not sure yet if the inverters will allow me to poll them over a single usb connection or not
inverterusbport2 = "COM4"
inverterusbport3 = "/dev/ttyUSB2"

verbose = 0
gwverbose = 0
gwinfodump = 1

# Codes
StatusCodes = {
    0: "Standby",
    1: "noUSE",
    2: "Discharge",
    3: "Fault",
    4: "Flash",
    5: "PV Charge",
    6: "AC Charge",
    7: "Combine Charge",
    8: "Combine charge and Bypass",
    9: "PV charge and Bypass",
    10: "AC Charge and Bypass",
    11: "Bypass",
    12: "PV charge and discharge"
}

def merge(*dict_args):
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

import json

class Growatt:
    def __init__(self, client, name, unit, fields_file):
        self.client = client
        self.name = name
        self.unit = unit
        self.fields_file = fields_file

        row = self.client.read_holding_registers(73, unit=self.unit)
        if type(row) is ModbusIOException:
            if gwverbose: print("GWVERBOSE1",row)
            raise row
        self.modbusVersion = row.registers[0]

        with open(self.fields_file, 'r') as f:
            self.fields = json.load(f)

    def read(self):
        row = self.client.read_input_registers(0, 83, unit=self.unit)
        if gwverbose: print("GWVERBOSE2")
        if gwverbose: print("GWVERBOSE3")
        info = {                                    # ==================================================================
             "Module": self.unit,  # use self.unit instead of unit
             "StatusCode": row.registers[0],
             "Status": StatusCodes[row.registers[0]],
        }
        for field_num, field_data in self.fields.items():
            name = field_data["name"]
            unit = field_data["unit"]
            explanation = field_data["explanation"]
            divider = field_data["divider"]
            value = float(row.registers[int(field_num)]) / divider
            info[name] = value
        if gwinfodump: print(info)
        return info


print("Connecting to Inverter..", end="")
try:
  client = ModbusClient(method='rtu', port=inverterusbport1, baudrate=9600, stopbits=1, parity='N', bytesize=8, timeout=1)
  client.connect()
except:
  print("Failed")
else:
 print("Done!")



print("Loading inverters.. ", end="")
inverters = []
for i in range(numinverters):
  #unit is this concept in modbus of an address of the thing you are talking to on the bus
  #it should be 1 for gw1, 2 for gw2, etc..etc  be sure to set any addressable things on the bus
  #to a different unit number
  #it looks like growatt it 
  unit=i+1
  name = "Growatt"+str(unit)
  measurement=str(unit)
  print("Name ",name," unit is ",unit," measurement is ",measurement)
  growatt = Growatt(client, name, unit, file_path)
  inverters.append({
    'growatt': growatt,
    'measurement': measurement
  })
print("Done!")
app = Flask(name)
results = []


@app.route("/results", methods=["GET"])
def get_results():
    # Call the poll_inverters function to update the results
    for inverter in inverters:
        growatt = inverter['growatt']
        try:
            now = time.time()
            info = growatt.read()
            results = [info]  # Replace the info to the results list
                
            if verbose: print("CHECK4")
            points = [{
                'time': int(now),
                'measurement': inverter['measurement'],
                "fields": info
            }]
            if verbose: print("CHECK5")
        except Exception as err:
            if verbose: print("ERRORHERE1")
            print(err)
        time.sleep(interval)
    
    return jsonify(results)



# Create a thread for the poll_inverters function
# poll_thread = threading.Thread(target=poll_inverters)
# poll_thread.start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)