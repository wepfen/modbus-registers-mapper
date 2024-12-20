# modbus-registers-mapper
Map register with known exposed variables 


## Context

Supposing idk in the context of a ctf or challenge you got access to a kind of API or web server exposing values related to a PLC and you also got access to a modbus, this tool can quickly map the exposed variables with modbus registers.

The exposed variables could look like that :

```json
{
	"var_1":0,
	"var_2":2,
	"var_3":41,
	"var_4":0
}
```

## Installation

```python
python -m venv .venv
source.venv/bin/activate
pip install -r requirements.txt
wget https://raw.githubusercontent.com/wepfen/modbus-registers-mapper/refs/heads/main/map_modbus_registers.py
```

## Usage

```
usage: map_modbus_registers.py [-h] [-u URL] [--modbus MODBUS]
                               [--modbus-port MODBUS_PORT] [--protocol PROTOCOL]

options:
  -h, --help            show this help message and exit
  -u URL, --url URL     url of the web server displaying variables
  --modbus MODBUS       modbus server address
  --modbus-port MODBUS_PORT
                        modbus server port (default: 502)
  --protocol PROTOCOL   protocol to communicate with modbus server (tcp/udp) (default: tcp)
```

## Example 

```bash
python map_modbus_registers.py --url http://172.16.10.10 --modbus controller.lab --protocol tcp

|   modbus register | variable name   |
|-------------------|-----------------|
|                 1 | var_1           |
|                 7 | var_2           |
|                14 | var_3           |
|                32 | var_4           |
```
