import json
import time
import requests
import argparse
import sys
import pymodbus.client as ModbusClient
from pymodbus import (
    FramerType,
    ModbusException,
)
from tabulate import tabulate

def argument_parsing() -> argparse.ArgumentParser:

	parser = argparse.ArgumentParser()
	parser.add_argument("-u", "--url",
                        type = str,
                        help = "url of the web server displaying variables")

	parser.add_argument("--modbus",
                        type = str,
                        help = "modbus server address"
                        )
	
	parser.add_argument("--modbus-port",
                        type = int,
                        default = 502,
                        help = "modbus server port"
                        )
	
	parser.add_argument("--protocol",
                        type = str,
                        default = "tcp",
                        help = "protocol to communicate with modbus server (tcp/udp)"
                        )
	return parser

	
def init_client(comm, host, port, framer=FramerType.SOCKET) -> ModbusClient.tcp.ModbusTcpClient:
	"""Run sync client."""

	client: ModbusClient.ModbusBaseSyncClient
	if comm == "tcp":
		client = ModbusClient.ModbusTcpClient(
			host,
			port=port,
			framer=framer,
 		)

	elif comm == "udp":
		client = ModbusClient.AsyncModbusUdpClient(
			host,
			port=port,
			framer=framer,
		)

	client.connect()
	return client

def read_register(client, register: int) -> int:

	try:
		register = client.read_holding_registers(address=register, count=1, slave=1)
	except ModbusException as exc:
		print(f"Received ModbusException({exc}) from library")

	return register.registers[0]
		
def write_register(client, register: int):

	try:
		client.write_register(address=register, value=1337)
	except ModbusException as exc:
		print(f"Received ModbusException({exc}) from library")
		return


def get_values(url: str) -> dict :
	
	r = requests.get(url)
	vals = json.loads(r.text)
	return vals

def main():
	
	parser = argument_parsing()	
	args = parser.parse_args()

	if len(sys.argv) == 1:
		parser.print_help()		
		sys.exit(1)


	url = args.url
	modbus = args.modbus
	modbus_port = args.modbus_port
	protocol = args.protocol
		
	client = init_client(protocol,modbus, modbus_port)

	registers = {}
	vars_list = get_values(url)

	print("initial vars : ", vars_list)

	i = 0

	while len(vars_list) != len(registers):
		
		i += 1
		
		if i > 65535:
			raise ValueError("The register id can not be above 65535")
			# section 6.3 : https://modbus.org/docs/Modbus_Application_Protocol_V1_1b.pdf


		register_before_write = read_register(client, i)
		
		write_register(client, i)	
		register_after_write = read_register(client,i)
			
		vars_after_write = get_values(url)
		

		try :
			updated_index = list(vars_after_write.values()).index(1337)
			updated_var = list(vars_after_write.keys())[updated_index]
			print(f"Found register {i} -> {updated_var}")
			registers[str(i)] = updated_var
			time.sleep(1)
		except Exception as e:
			pass
		
			
		client.write_register(i, register_before_write)
	
	print("\n\n")
	print(tabulate(zip(registers.keys(), registers.values()), ["modbus register", "variable name"], tablefmt="github"))	

	client.close()


if __name__ == "__main__":
	main()
		
