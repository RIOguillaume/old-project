import numpy as np
import matplotlib.pyplot as plt

# Collecte des données de déplacement du robot à l'aide de capteurs
robot_data = np.array([[1, 0], [1, 1.5], [2, 2.5], [4, 3.5], [6, 4]])

#collecte des données des murs
wall_data = np.array(
    [[0, 1], [0, 2], [0, 4], [4,8],[8,9],
    [9,9], [12,9]]
    )
#fichage de l'axe du robot X et Y
robot_axis= np.array([
    [robot_data[-1][0]+1,robot_data[-1][1]],
    [robot_data[-1][0],robot_data[-1][1]],
    [robot_data[-1][0],robot_data[-1][1]+1],
        ])


# Position actuel du robot 
posActuelX= robot_data[-1][0]
posActuelY = robot_data[-1][1]
# Angle dû au virage 
thetaAvant = np.pi/4+1.5
thetaDroite = thetaAvant - np.pi/2
# segment observé devant
axeAvantX = posActuelX + 1*np.cos(thetaAvant)
axeAvantY = posActuelY + 1*np.sin(thetaAvant)
# segment observé
axeDroiteX = posActuelX + 1*np.cos(thetaDroite)
axeDroiteY = posActuelY + 1*np.sin(thetaDroite)





## Tracé les données de déplacement du robot
#Tracé les points sauvegardé du robot
plt.plot(robot_data[:, 0], robot_data[:, 1], 'bo')
#Tracé des lignes de déplacements du robot
plt.plot(robot_data[:, 0], robot_data[:, 1], 'y-.')

##Tracé de la postion actuel du robot
# Tracé du segment correspondant à la position que regarde le robot
plt.plot([posActuelX, axeAvantX], [posActuelY, axeAvantY ], 'r')
plt.plot([posActuelX, axeDroiteX], [posActuelY, axeDroiteY ], 'r')

plt.plot(wall_data[:, 0], wall_data[:, 1], 'ro')


plt.plot(robot_axis[:, 0], robot_axis[:, 1], 'g:')



plt.title('Carte des déplacements du robot')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()
