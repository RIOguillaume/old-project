from serial.tools import list_ports
from dobot_extensions import Dobot
import pydobot
import time
import sys

print('- liste des ports COM:')
ports = list(list_ports.comports())
for p in ports:
    print (p)

print('- connexion au robot ...', end='')
sys.stdout.flush()
port = 'COM3' # replacez ici COM3 par votre port de communication
device = Dobot(port=port)
print('[ok]')
sys.stdout.flush()

# speed_mm_per_sec, distance_mm, direction=1 ou -1, interface=0)
device.conveyor_belt_distance(20, 200, -1, 0)

print('- deconnexion')
device.close()
