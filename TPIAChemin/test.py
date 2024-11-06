from serial.tools import list_ports
import csv
import time
import sys
import json
import math
import CodeV3
from pydobot import Dobot
import pydobot
from dobot_extensions import Dobot
from serial import Serial

serial_port = Serial(port="COM6", baudrate=115200, timeout=1, bytesize=8, stopbits=1)

print('- liste des ports COM:')
ports = list(list_ports.comports())
for p in ports:
    print(p)

print('- connexion au robot ...', end='')
sys.stdout.flush()
port1 = 'COM3'
port2 = 'COM5'
api2 = Dobot(port=port2)
print("co "+str(port2))
api1 = Dobot(port=port1)
print("co "+str(port1))

print('[ok]')
sys.stdout.flush()

# génère le tableau par ordre croissant de pose, en commencant par le kapla le plus bas et
# parmis les kaplas de même hauteur le plus loin du bras robotique
def algoCreationTableau(tabConstruction):
    tabTrier =[]
    tailleTab = len(tabConstruction)
    i = 1
    while i > 0:
        i=0
        for cpt in range(tailleTab-1):
            if tabConstruction[cpt]['base'][2] > tabConstruction[cpt+1]['base'][2]:
                i+=1
                tmp = tabConstruction[cpt]
                tabConstruction[cpt] = tabConstruction[cpt+1]
                tabConstruction[cpt+1] = tmp
    i = 1
    while i > 0:
        i=0
        for cpt in range(tailleTab-1):
            pos1 = math.sqrt(tabConstruction[cpt]['base'][0]*tabConstruction[cpt]['base'][0]+tabConstruction[cpt]['base'][1]*tabConstruction[cpt]['base'][1])
            pos2 = math.sqrt(tabConstruction[cpt+1]['base'][0]*tabConstruction[cpt+1]['base'][0]+tabConstruction[cpt+1]['base'][1]*tabConstruction[cpt+1]['base'][1])
            if tabConstruction[cpt]['base'][2] == tabConstruction[cpt+1]['base'][2] and pos1 < pos2:
                i+=1
                tmp = tabConstruction[cpt]
                tabConstruction[cpt] = tabConstruction[cpt+1]
                tabConstruction[cpt+1] = tmp
    return tabConstruction

#ouvrir le tableau et génération du tableau trier dans l'ordre des poses 
with open('F:/Worspace/Code 2/construction.json') as json_data:
    tabConstruction = json.load(json_data)
tabTrier =  algoCreationTableau(tabConstruction)
print('Tableau de contruction généré')

#récupère les positions des robots
poseR1 = api1.get_pose()
poseR2 = api2.get_pose()
#sauvegarde la position dans laquel le robot est au moment du lancement du programe 
positionRobot1 = poseR1.position
positionRobot2 = poseR2.position

#False ou 0 = on souffle de l'aire
#True ou 1 = on aspire

api1.suck(False)
api2.suck(False)

ZOffset = 20

#position initial d'un kapla dans le bac 
posBacSansMoteurX = 250
posBacSansMoteurY = -175
posBacSansMoteurZ = -50

#position initial d'un kapla dans le bac avec levé
posBacAvecMoteurX = 250
posBacAvecMoteurY = -175
posBacAvecMoteurZ = 0

#paramètre initial du stockage
posInitialStockageX = 200
posInitialStockageY = 150
posInitialStockageZ = -46
espaceEnY = 21
espaceEnZ = 25
nbEtages = 2

#position initial de convoyeur 
posConvoyeurDebutX = 265
posConvoyeurDebutY = -50
posConvoyeurDebutZ = 50 + ZOffset
posConvoyeurDebutR = 0

#position initial d'un kapla en fin de convoyeur 
posFinConvoyeurX = 276
posFinConvoyeurY = -80
posFinConvoyeurZ = 36 + ZOffset

#position construction, c'est la position à lequel le robot se rendra avant chaque dépose 
posConstructionX =0
posConstructionY = 230
posConstructionZ = 150
        

#Renvoie la position du kapla numéro "cpt" dans le stockage
def posStockage(cpt):
    return (posInitialStockageX,
               posInitialStockageY + (cpt% 5) * espaceEnY,
               posInitialStockageZ + (nbEtages - math.floor(cpt/5) -1) * espaceEnZ)
# renvoie
# -1 si erreur
# 0 si pos finale est fin du convoyeur face C
# 1 si dans le bac sans activation du moteur face B
# 2 si dans le bac avec activation du moteur face A
def numeroPosFinConvoyeur(cpt):
    if tabTrier[cpt]["atitude"][2] == 25:
        return 0
    elif tabTrier[cpt]["atitude"][2] == 20:
        return 1
    elif tabTrier[cpt]["atitude"][2] == 70:
        return 2
    else:
        return -1

#renvoie la position (x,y,z) à laquelle il faut aller chercher le kapla courrent 
def posConvoyeur(cpt):
    varNbPosFinConvoyeur = numeroPosFinConvoyeur(cpt) 
    if varNbPosFinConvoyeur == 0:
        offset = cam.distancePreciseLvK()
        offset = [0,0]
        return (posFinConvoyeurX - int(offset[1]), posFinConvoyeurY - int(offset[0]), posFinConvoyeurZ)
    elif varNbPosFinConvoyeur == 1:
        return (posBacSansMoteurX, posBacSansMoteurY, posBacSansMoteurZ)
    elif varNbPosFinConvoyeur == 2:
        return (posBacAvecMoteurX, posBacAvecMoteurY, posBacAvecMoteurZ)
    else:
        return -1

#renvoie la position de construction du kapla numéro "cpt" avec l'ajout des offsets
def positionFinalConstruction(cpt, rot_offset: float):
    xOffset = -40
    yOffset = 230
    zOffset = -75
    x = tabTrier[cpt]["base"][0] + tabTrier[cpt]["atitude"][0]/2
    y = tabTrier[cpt]["base"][1] + tabTrier[cpt]["atitude"][1]/2
    z = tabTrier[cpt]["base"][2] + tabTrier[cpt]["atitude"][2]
    r = tabTrier[cpt]["pivot"] + rot_offset
    return (x+xOffset,y+yOffset,z+zOffset,r)

def boiteAction(action):
    """
    2: plat \n
    3: droit \n
    4: vibre \n
    5: ejection \n
    """
    data = str(action).encode("ascii") + "\n".encode("ascii")
    serial_port.write(data)

#on le place au dessus du stockage pour calibration du stockage
api1.wait_for_cmd(api1.move_to(posInitialStockageX, posInitialStockageY, posInitialStockageZ+50, 0,mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
time.sleep(10)

#on initialise la boite en position 45 degré 
boiteAction(2)
#initialisation du compteur de kapla
cpt = 0
#lancement de la camera
cam = CodeV3.Camera()
#api1.wait_for_cmd(api1.home())
#api2.wait_for_cmd(api2.home())
while(True):
    """
    pos = posStockage(cpt)
    posCubeStockageX= pos[0]
    posCubeStockageY= pos[1]
    posCubeStockageZ= pos[2]
    posCubeStockageR = 0
    """
    (posCubeStockageX,posCubeStockageY,posCubeStockageZ) = posStockage(cpt)
    
    boiteAction(2)#45 degré
    
    #on envoie le robot chercher le premier kapla
    #on se place 30mm au dessus du Kapla à prendre
    api1.wait_for_cmd(api1.move_to(posCubeStockageX, posCubeStockageY, posCubeStockageZ+30, posCubeStockageR,mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
    print(" posCubeStockageHaut : OK")
    sys.stdout.flush()

    #on va sur notre kapla dans le stockage 
    api1.wait_for_cmd(api1.move_to(posCubeStockageX, posCubeStockageY, posCubeStockageZ, posCubeStockageR,mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
    print(" posCubeStockage : OK ")
    sys.stdout.flush()

    #on aspire avec la ventouse
    api1.suck(True)
    time.sleep(2)

    #on remonte de 30mm
    api1.wait_for_cmd(api1.move_to(posCubeStockageX, posCubeStockageY, posCubeStockageZ+30, posCubeStockageR,mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
    print(" posCubeStockageHaut : OK ")
    sys.stdout.flush()

    #va à la pos saugardé au debut 
    api1.wait_for_cmd(api1.move_to(positionRobot1.x, positionRobot1.y, positionRobot1.z, 0,mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
    print(" posCubeInitial : OK")
    sys.stdout.flush()

    #on envoie le robot 30mm au dessus du début du convoyeur
    api1.wait_for_cmd(api1.move_to(posConvoyeurDebutX, posConvoyeurDebutY, posConvoyeurDebutZ+30, posConvoyeurDebutR,mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
    print(" posConvoyeurDebutHaut : OK")
    sys.stdout.flush()
    
    #on va sur le convoyeur
    api1.wait_for_cmd(api1.move_to(posConvoyeurDebutX, posConvoyeurDebutY, posConvoyeurDebutZ, posConvoyeurDebutR,mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
    print(" posConvoyeurDebut : OK")
    sys.stdout.flush()
    
    #on lache la piece avec la ventouse
    api1.suck(False)
    time.sleep(1)

    #on remonte de 30mm
    api1.wait_for_cmd(api1.move_to(posConvoyeurDebutX, posConvoyeurDebutY, posConvoyeurDebutZ+30, posConvoyeurDebutR,mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
    print(" posConvoyeurDebutHaut : OK")
    sys.stdout.flush()

    #va à la pos saugardé au debut 
    api1.wait_for_cmd(api1.move_to(positionRobot1.x, positionRobot1.y, positionRobot1.z, 0,mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
    print(" posCubeInitial : OK")
    sys.stdout.flush()
    
    #gestion du convoyeur
    #on démarre le convoyeur
    #si le robot doit aller chercher le kapla sur le convoyeur on stop le convoyeur dès que le kapla franchi la ligne virtuel de la camera
    #sinon on attend que la kapla tombe dans le bac puis on stop le convoyeur
    api1.conveyor_belt(100,-1, 0)
    offset_rot_angle = 0
    if numeroPosFinConvoyeur(cpt) == 0:
        while not cam.ligneVirtuelleTrigerred():
            time.sleep(0.05)
        time.sleep(0.05)
        
        offset_rot_angle = cam.normAngleLine2(cam.getAnglePiece())
    else:
        while not cam.checkEtatConvoyeur():
            time.sleep(0.05)
        while not cam.ligneVirtuelleTrigerred():
            time.sleep(0.05)
        api1.conveyor_belt(30,-1, 0)
        while cam.checkEtatConvoyeur():
            time.sleep(0.05)
    api1.conveyor_belt(0, -1, 0)
    time.sleep(2)
    
    #gestion du bac
    #si un kapla est dans le bac on fait vibrer le moteur puis soit on le place à l'horizontal ou à la vertical 
    if numeroPosFinConvoyeur(cpt) != 0:
        boiteAction(4)
        time.sleep(5)
        if numeroPosFinConvoyeur(cpt) == 2:
            boiteAction(3)
        else:
            boiteAction(1)
        time.sleep(5)


    (posConvoyeurFinX,posConvoyeurFinY,posConvoyeurFinZ) = posConvoyeur(cpt)
    """
    posConv = posConvoyeur(cpt)
    posConvoyeurFinX = posConv[0]
    posConvoyeurFinY = posConv[1] 
    posConvoyeurFinZ = posConv[2]
    """
    #on va 85mm au dessus du kapla
    api2.wait_for_cmd(api2.move_to(posConvoyeurFinX, posConvoyeurFinY, posConvoyeurFinZ+85, 0,mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
    print(" posConvoyeurFinHaut : OK")
    sys.stdout.flush()

    #on va sur le kapla
    api2.wait_for_cmd(api2.move_to(posConvoyeurFinX, posConvoyeurFinY, posConvoyeurFinZ, 0,mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
    print(" posConvoyeurFin : OK")
    sys.stdout.flush()

    #on aspire avec la ventouse
    api2.suck(True)
    time.sleep(2)

    #on remonte de 105mm
    api2.wait_for_cmd(api2.move_to(posConvoyeurFinX, posConvoyeurFinY, posConvoyeurFinZ+105, 0,mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
    print(" posConvoyeurFinHaut : OK")
    sys.stdout.flush()

    #va à la position construction-inter
    api2.wait_for_cmd(api2.move_to(200, 150, 150, 0,mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
    print(" posConstruction-inter : OK")
    sys.stdout.flush()


    (posConstructionFinX,posConstructionFinY,posConstructionFinZ,rotContructionFin)=positionFinalConstruction(cpt, offset_rot_angle)
    """
    posConstructionFin = positionFinalConstruction(cpt, offset_rot_angle)
    posConstructionFinX = posConstructionFin[0] 
    posConstructionFinY = posConstructionFin[1] 
    posConstructionFinZ = posConstructionFin[2]
    rotContructionFin = posConstructionFin[3]
    """
    #va à la position construction-inter
    api2.wait_for_cmd(api2.move_to(posConstructionX, posConstructionY, posConstructionZ, rotContructionFin,mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
    print(" posConstruction-inter : OK")
    sys.stdout.flush()

    #on va 30mm au dessus de la zone de pose 
    api2.wait_for_cmd(api2.move_to(posConstructionFinX, posConstructionFinY, posConstructionFinZ+30, rotContructionFin,mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
    print(" posConstructionFinHaut : OK")
    sys.stdout.flush()
    
    #on va sur la zone de pose
    api2.wait_for_cmd(api2.move_to(posConstructionFinX, posConstructionFinY, posConstructionFinZ, rotContructionFin,mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
    print(" posConstructionFin : OK")
    sys.stdout.flush()
    
    #on lache la piece avec la ventouse
    api2.suck(False)
    time.sleep(2)

    #on remonte de 90mm
    api2.wait_for_cmd(api2.move_to(posConstructionFinX, posConstructionFinY, posConstructionFinZ+90, rotContructionFin,mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
    print(" posConstructionFinHaut : OK")
    sys.stdout.flush()

    #va à la position construction-inter
    api2.wait_for_cmd(api2.move_to(200, 150, 150, 0,mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
    print(" posConstruction-inter : OK")
    sys.stdout.flush()

    #va à la pos saugardé au debut 
    api2.wait_for_cmd(api2.move_to(positionRobot2.x, positionRobot2.y, positionRobot2.z, 0,mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
    print(" posCubeInitial : OK")
    sys.stdout.flush()

    cpt += 1
    #on continue tant qu'on a des pièces à construire.
    if cpt == len(tabTrier):
        break

cam.stop()
api1.close()
api2.close()
sys.exit()
