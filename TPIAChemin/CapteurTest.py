from serial.tools import list_ports
from dobot_extensions import Dobot
#from pydobot import Dobot
import pydobot
import time
import sys

PORT_GP1 = 0x00
PORT_GP2 = 0x01
PORT_GP4 = 0x02
PORT_GP5 = 0x03

print('- liste des ports COM:')
ports = list(list_ports.comports())
for p in ports:
    print (p)

print('- connexion au robot ...', end='')
sys.stdout.flush()
port = 'COM5' # replacez ici COM3 par votre port de communication
device = Dobot(port=port)
print('[ok]')
sys.stdout.flush()

print('- home position (le robot recale et définit sa position zéro) ... ', end='')
sys.stdout.flush()
#device.wait_for_cmd(device.home())
print('[ok]')


print('- connexion capteur: ', end='')
sys.stdout.flush()
infraredPort = 'PORT_GP4' # port de communication du capteur
device.SetInfraredSensor(enable=True, infraredPort=PORT_GP4, version=1)
print ('[ok]')
time.sleep(1)
for i in range(5):
    print(device.GetInfraredSensor(infraredPort=PORT_GP4, version=1))
    time.sleep(1)   
print('- deconnexion')
device.close()
