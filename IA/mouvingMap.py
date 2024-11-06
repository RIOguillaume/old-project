import pygame
import numpy as np
import matplotlib.pyplot as plt


# Initialisation de Pygame
pygame.init()

# Définition des dimensions de la fenêtre
screen_width = 600
screen_height = 600

# Définition des couleurs
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Création de la fenêtre
screen = pygame.display.set_mode((screen_width, screen_height))

# Fond blanc
screen.fill(white)

#offset pygame
offset_width = screen_width/2
offset_height =screen_height/2

# Collecte des données de déplacement du robot à l'aide de capteurs
robot_position = np.array([
    [0, 0], [10, 10], [15,25 ], [20, 40], [30, 60]
    ])

# Collecte des données des murs
wall_data = np.array([
    [50, 0], [50, 20], [50, 40], [40,80],[30,90]
    ])


def afficher_Point (point_list, color = red):
    for point_position in point_list:
        pygame.draw.circle(screen, color, (point_position[0] + offset_width, point_position[1]  + offset_height), 1)

# Afficher les points des déplacements sauvegardés du robot 
afficher_Point(robot_position,blue)

#afficher les points des obstacles sauvegardés par le robot
afficher_Point(wall_data, red)

# Afficher le robot
#afficher_Point(robot_position[-1], red)
pygame.draw.circle(screen, green, (robot_position[-1][0] + offset_width, robot_position[-1][1]  + offset_height), 3)

#Afficher le repère monde par rapport au robot

# Affichage de la fenêtre
pygame.display.flip()

# Boucle principale
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
