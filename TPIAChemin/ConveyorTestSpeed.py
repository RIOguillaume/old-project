from serial.tools import list_ports
import pydobot
import time
import sys

from dobot_extensions import Dobot

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
device.wait_for_cmd(device.home())
print('[ok]')

print('- position du robot: ', end='')
sys.stdout.flush()
pose = device.get_pose()
print()
print(pose)
position = pose.position

# speed_mm_per_sec, direction=1 ou -1, interface=0)
device.conveyor_belt(20, -1, 0)
print('- mouvement en Z ... ')
device.suck(True)
print('- aspiration ok ... ')
sys.stdout.flush()
device.wait_for_cmd(device.move_to(250, 0, 40, 0, mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
time.sleep(2)
device.wait_for_cmd(device.move_to(250, 50, 100, 0, mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
print(pose)
device.suck(False)
print('- aspiration off ... ')
device.conveyor_belt(0, -1, 0)
print('- deconnexion')
device.close()
