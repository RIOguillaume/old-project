from serial.tools import list_ports
import csv
import time
import sys
import json
import math
from pydobot import Dobot
import pydobot
from dobot_extensions import Dobot

print('- liste des ports COM:')
ports = list(list_ports.comports())
for p in ports:
    print(p)

print('- connexion au robot ...', end='')
sys.stdout.flush()
port1 = 'COM4'  # replacez ici COM3 par votre port de communication
port2 = 'COM5' 
api1 = Dobot(port=port1)
#api2 = Dobot(port=port2)
print('[ok]')
sys.stdout.flush()

# génère le tableau par ordre croissant de pose, en commencant par le kapla le plus bas et
# parmis les kaplas de même hauteur le plus loin du bras robotique
def algoCreationTableau(tabConstruction):
    #tabTrier =[]
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
with open('construction.json') as json_data:
    tabConstruction = json.load(json_data)
tabTrier =  algoCreationTableau(tabConstruction)
print('Tableau de contruction généré')


#initialise pos initail
#api1.set_home()
#api2.set_home()
print('Home set !')
sys.stdout.flush()

#va en pos ini
api1.wait_for_cmd(api1.home())
#api2.wait_for_cmd(api2.home())
print('robot en position home')
sys.stdout.flush()

#récupère les positions des robots
poseR1 = api1.get_pose()
#poseR2 = api2.get_pose()
positionRobot1 = poseR1.position
#positionRobot2 = poseR2.position

#False ou 0 = on souffle de l'aire
#True ou 1 = on aspire

api1.suck(False)
#api2.suck(False)


#rangé de 5 pièce
"""déterminer les position pour le moment valeur fixe"""
#si possible avec
#positionRobot1.x + ....
#positionRobot1.y + .......
#positionRobot1.z + ....

"""relative au bras robot stockage"""
posInitialStockageX = 200
posInitialStockageY = -150
posInitialStockageZ = -50
espaceEnX = -20
espaceEnY = -20

posConvoyeurDebutX = 200
posConvoyeurDebutY = 0
posConvoyeurDebutZ = 15
posConvoyeurDebutR = 0

"""relative au bras robot contruction vérifier les Z"""
posFinConvoyeurX = 200
posFinConvoyeurY = 0
posFinConvoyeurZ = 15

posBacSansMoteurX = 200
posBacSansMoteurY = 100
posBacSansMoteurZ = -50

posBacAvecMoteurX = 200
posBacAvecMoteurY = 100
posBacAvecMoteurZ = 0


posConstructionX =0
posConstructionY = 230
posConstructionZ = 150
#à tester pour ajouter un espace en Z si pas assez de kapla
def posStockage(cpt):
    return (posInitialStockageX + cpt/5 * espaceEnX,
               posInitialStockageY + cpt % 5 * espaceEnY,
               posInitialStockageZ)
# renvoie
# -1 si erreur
# 0 si pos finale est fin du convoyeur face C
# 1 si dans le bac sans activation du moteur face B
# 2 si dans le bac avec activation du moteur face A
# tab((x,y,z),(x',y',z'),r)
# 1 x,y,z position de base
# 2 x',y',z' position attitude dans 20,25,70
# 3 r rotation vertical en radiant 
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
        return (posFinConvoyeurX, posFinConvoyeurY, posFinConvoyeurZ)
    elif varNbPosFinConvoyeur == 1:
        return (posBacSansMoteurX, posBacSansMoteurY, posBacSansMoteurZ)
    elif varNbPosFinConvoyeur == 2:
        return (posBacAvecMoteurX, posBacAvecMoteurY, posBacAvecMoteurZ)
    else:
        return -1


            


def positionFinal(cpt):
    x = tabTrier[cpt]["base"][0] + tabTrier[cpt]["atitude"][0]/2
    y = tabTrier[cpt]["base"][1] + tabTrier[cpt]["atitude"][1]/2
    z = tabTrier[cpt]["base"][2] + tabTrier[cpt]["atitude"][2]
    r = tabTrier[cpt]["pivot"]
    print((x,y,z,r))
    return (x-40,y+200,z-70,r)
        
        

cpt = 0
pos = posStockage(cpt)
posCubeStockageX= pos[0]
posCubeStockageY= pos[1]
posCubeStockageZ= pos[2]
posCubeStockageR = 0


cpt = 0
while(True):
    pos = posStockage(cpt)
    posCubeStockageX= pos[0]
    posCubeStockageY= pos[1]
    posCubeStockageZ= pos[2]
    posCubeStockageR = 0

    #on envoie le robot chercher la pièce
    #on se place 10 au dessus du Kapla à prendre
    print(pos)
    print(api1.get_pose())
    
    api1.wait_for_cmd(api1.move_to(posCubeStockageX, posCubeStockageY, posCubeStockageZ+30, posCubeStockageR,mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
    print(" posCubeStockageHaut : OK")
    sys.stdout.flush()

    #on va sur notre kapla
    api1.wait_for_cmd(api1.move_to(posCubeStockageX, posCubeStockageY, posCubeStockageZ, posCubeStockageR,mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
    print(" posCubeStockage : OK ")
    sys.stdout.flush()

    #on aspire avec la ventouse
    api1.suck(True)
    time.sleep(2)

    #on remonte de 10 
    api1.wait_for_cmd(api1.move_to(posCubeStockageX, posCubeStockageY, posCubeStockageZ+30, posCubeStockageR,mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
    print(" posCubeStockageHaut : OK ")
    sys.stdout.flush()

    #va à la position initial
    api1.wait_for_cmd(api1.move_to(positionRobot1.x, positionRobot1.y, positionRobot1.z, 0,mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
    print(" posCubeInitial : OK")
    sys.stdout.flush()
    
    #tester jusque ici
    #observer s'il y a besoin d'une rotation
    
    #on envoie le robot 30 au dessus du début du convoyeur
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

    #on remonte de 10 
    api1.wait_for_cmd(api1.move_to(posConvoyeurDebutX, posConvoyeurDebutY, posConvoyeurDebutZ+30, posConvoyeurDebutR,mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
    print(" posConvoyeurDebutHaut : OK")
    sys.stdout.flush()

    #va à la position initial
    api1.wait_for_cmd(api1.move_to(positionRobot1.x, positionRobot1.y, positionRobot1.z, 0,mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
    print(" posCubeInitial : OK")
    sys.stdout.flush()
    #tester jusque ici
    #observer s'il y a besoin d'une rotation

    #gestion du convoyeur
    #a tester : 

    #api1.conveyor_belt_distance(20, 200, -1, 0)
    #

    #gestion camera
    #....
    #
    """
    posConv = posConvoyeur(cpt)
    print(posConvoyeur(cpt))
    posConvoyeurFinX = posConv[0]
    posConvoyeurFinY = posConv[1]
    posConvoyeurFinZ = posConv[2]

    #on va 10 au dessus du kappla sur le convoyeur 
    api2.wait_for_cmd(api2.move_to(posConvoyeurFinX, posConvoyeurFinY, posConvoyeurFinZ+30, 0,mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
    print(" posConvoyeurFinHaut : OK")
    sys.stdout.flush()

    #on va sur le kapla
    api2.wait_for_cmd(api2.move_to(posConvoyeurFinX, posConvoyeurFinY, posConvoyeurFinZ, 0,mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
    print(" posConvoyeurFin : OK")
    sys.stdout.flush()

    #on aspire avec la ventouse
    api2.suck(True)
    time.sleep(2)

    #on remonte de 10
    api2.wait_for_cmd(api2.move_to(posConvoyeurFinX, posConvoyeurFinY, posConvoyeurFinZ+150, 0,mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
    print(" posConvoyeurFinHaut : OK")
    sys.stdout.flush()

    #va à la position construction-inter
    api2.wait_for_cmd(api2.move_to(200, 150, 150, 0,mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
    print(" posConstruction-inter : OK")
    sys.stdout.flush()

    

    
    #tester jusque ici
    #observer s'il y a besoin d'une rotation
    posConstructionFin = positionFinal(cpt)
    posConstructionFinX = posConstructionFin[0]
    posConstructionFinY = posConstructionFin[1]
    posConstructionFinZ = posConstructionFin[2]
    rotContructionFin = posConstructionFin[3]

    #va à la position construction
    api2.wait_for_cmd(api2.move_to(posConstructionX,posConstructionY ,posConstructionZ , 0,mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
    print(" posConstruction-inter : OK")
    sys.stdout.flush()
                
    #on va 10 au dessus de la zone de pos 
    api2.wait_for_cmd(api2.move_to(posConstructionFinX, posConstructionFinY, posConstructionFinZ+80, rotContructionFin,mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
    print(" posConstructionFinHaut : OK")
    sys.stdout.flush()

    #on va 10 au dessus de la zone de pos 
    api2.wait_for_cmd(api2.move_to(posConstructionFinX, posConstructionFinY, posConstructionFinZ, rotContructionFin,mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
    print(" posConstructionFin : OK")
    sys.stdout.flush()
            
    #on lache la piece avec la ventouse
    api2.suck(False)
    time.sleep(2)

    #on remonte de 150
    api2.wait_for_cmd(api2.move_to(posConstructionFinX, posConstructionFinY, posConstructionFinZ+90, rotContructionFin,mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
    print(" posConstructionFinHaut : OK")
    sys.stdout.flush()

    #va à la position construction-inter
    api2.wait_for_cmd(api2.move_to(200, 200, positionRobot2.z, 0,mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
    print(" posConstruction-inter : OK")
    sys.stdout.flush()

    #va à la position initial
    api2.wait_for_cmd(api2.move_to(positionRobot2.x, positionRobot2.y, positionRobot2.z, 0,mode=pydobot.dobot.MODE_PTP.MOVL_XYZ))
    print(" posCubeInitial : OK")
    sys.stdout.flush()
    """
    #tester jusque ici
    #observer s'il y a besoin d'une rotation
    cpt += 1
    if cpt == 3:
        break

api1.close()
#api2.close()

