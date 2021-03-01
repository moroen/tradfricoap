# tradfricoap
A module and command line utility for working with the Ikea Tradfri Gateway.

## Installation
### Requirements
tradfricoap uses py3coap for communicating with the gateway. Py3coap is available on PyPi and should be installed automaticly when installing tradfricoap. If no prebuild wheel of py3coap is available on PyPy, py3coap can be installed from [source](https://github.com/moroen/pycoap).

### From PyPi
```
$ pip3 install tradfricoap
```

### From source
```
$ git clone https://github.com/moroen/tradfricoap.git
$ cd tradfricoap
$ python3 setup.py install
```

## Configuration
$ tradfri config gw IP KEY

## Basic usage
```shell
./tradfri.py --help
```

### List all devices
```shell
./tradfri list
```

### Controll a light
```shell
./tradfri on <ID>
./tradfri off <ID>
./tradfri level <ID> <LEVEL> (Level: 0-254)
```
