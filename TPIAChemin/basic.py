from serial.tools import list_ports
from pydobot import Dobot
import pydobot
import time
import sys

def pretty_print_pose(pose):
    print('(x=%0.2f, y=%0.2f, z=%0.2f r=%0.2f)' % \
          (pose.position.x, pose.position.y, pose.position.z, pose.position.r))

print('- liste des ports COM:')
ports = list(list_ports.comports())
for p in ports:
    print (p)

print('- connexion au robot ...', end='')
sys.stdout.flush()
port = 'COM4' # replacez ici COM3 par votre port de communication
device = Dobot(port=port)
print('[ok]')
sys.stdout.flush()

print('- position du robot: ', end='')
sys.stdout.flush()
pose = device.get_pose()
pretty_print_pose(pose)
position = pose.position

print('- mouvement en Z ... ', end='')
sys.stdout.flush()
device.wait_for_cmd(device.move_to(position.x, position.y, position.z+40, position.r))
print('[ok]')
# l'usage de wait_for_cmd (ligne suivante) permet d'attendre que la
# commande soit exécutée.  Ca n'est pas obligatoire, sans cela le
# robot lance le déplacement et rend la main au programme
# immédiatement sans attendre que le déplacement effectif soit fini.
print('- mouvement en Y ... ', end='')
sys.stdout.flush()
device.move_to(position.x, position.y+20, position.z+40, position.r)
# ici la commande rend la main immédiatement sans attendre la fin du déplacement
device.wait_for_cmd(device.move_to(position.x, position.y, position.z+40, position.r))
# ici on attend la fin
print('[ok]')
print('- mouvement en X ... ', end='')
sys.stdout.flush()
device.move_to(position.x+20, position.y, position.z+40, position.r)
device.wait_for_cmd(device.move_to(position.x, position.y, position.z+40, position.r))
print('[ok]')
print('- rotation de l\'outil ... ', end='')
sys.stdout.flush()
device.move_to(position.x, position.y, position.z+40, position.r+45)
device.wait_for_cmd(device.move_to(position.x, position.y, position.z+40, position.r))
print('[ok]')

print('- home position (le robot recale et définit sa position zéro) ... ', end='')
sys.stdout.flush()
device.set_home()
device.wait_for_cmd(device.home())
print('[ok]')

print('- mouvement vertical rectiligne ... ', end='')
device.wait_for_cmd(device.move_to(150, 0, 40, 0, mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
device.wait_for_cmd(device.move_to(150, 0, 100, 0, mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
print('[ok]')

pretty_print_pose(device.get_pose())
print()

print('- test ventouse ... ', end='')
device.suck(True)
time.sleep(1)
device.suck(False)
print('[ok]')

print('- deconnexion')
device.close()
