from ipaddress import ip_address
from datetime import datetime
import pyvisa
import socket
import json

SCPI_server_IP = 'localhost'
SCPI_Port = '9001'
SCPI_timeout = 20000
VISA_resource_name = 'TCPIP::' + SCPI_server_IP + '::' + SCPI_Port + '::SOCKET'

def Init():
    try:
        # print('Trying to connect to VISA resource: ' + VISA_resource_name)
        visaSession = pyvisa.ResourceManager().open_resource(VISA_resource_name)
        visaSession.timeout = SCPI_timeout
        visaSession.read_termination = '\n'
        json_obj = {}
        json_obj['instrument'] = []

        # print('SCPI client connected to SCPI server: ' + visaSession.query('*idn?'))
        # print()

        instrument_idn = visaSession.query('*idn?').split(',')
        descriptions = instrument_idn[0] + " " + instrument_idn[1] + " - " + instrument_idn[2]
        hostname = visaSession.query(':SYSTem:COMMunicate:LAN:HOSTname?')
        mac_address = visaSession.query(':SYSTem:MACaddress?')
        tcp_ip_address = visaSession.query(':SYSTem:COMMunicate:LAN:CONFig?')
        visa_resource_string = VISA_resource_name
        date = visaSession.query(':SYSTem:DATE?')
        date = date.replace(',', '-')
        time = datetime.today().strftime("%I:%M %p")
        current_time = date + " " + time
        
        json_obj['instrument'].append({
            'LXI_Device_Model' : instrument_idn[1],
            'Manufacturer' : instrument_idn[0],
            'Serial_Number' : instrument_idn[2],
            'Description' : descriptions,
            'LXI_Extended_Functions' : 'TBD',
            'LXI_Version' : 'TBD',
            'Hostname' : hostname,
            'MAC_Address' : mac_address,
            'TCP_IP_Address' : tcp_ip_address,
            'Firmware_Revision' : instrument_idn[3],
            'LXI_Device_Address_String' : visa_resource_string,
        })
 
        # Write the object to file.
        with open('public/api/instrument_info.json','w', encoding='utf-8') as jsonFile:
            json.dump(json_obj, jsonFile, ensure_ascii=False, indent=4)
            visaSession.close()
    except pyvisa.VisaIOError:
        # Handles the exception and sends a false connection back to the server.py
        return False
if __name__ == "__main__":
    Init()