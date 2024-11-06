import math
import numpy as np

def direct(joints):
    """
    Reçoit en paramètre la position des articulations du robot, retourne
    la position du bout de l'effecteur
    """
    return [1, 0, 0.5]

def inverse(x, y, z):
    """
    Reçoit en paramètre une position cible, retourne la position des moteurs
    pour atteindre cette position cible
    """
    return [0., 0., 0.]

def inverseIterative(x, y, z):
    """
    Reçoit en paramètre une position cible, retourne la position des moteurs
    pour atteindre cette position cible

    Ici, on utilisera une fonction de score et scipy.minimize au lieu du modèle
    analytique
    """
    return [0., 0., 0.]

def trianglePoints(x, z, h, w):
    """
    Reçoit les paramètres géométriques du triangle, retourne la position des
    trois points du triangle
    """
    return [
        [0.4, 0, 0.3], [0.4, -0.1, 0.2], [0.4, 0.1, 0.2]
    ]

def triangle(x, z, h, w, t):
    """
    Reçoit les paramètres géométriques du triangle, déplace le bout du robot le long
    du triangle
    """

    return [0., 0., 0.]

def circlePoints(x, z, r, N=32):
    """
    Retourne N points qui approximent un cercle de rayon r en position (x,z)
    """
    return trianglePoints(x, z, r, r)

def circle(x, z, r, t):
    """
    Retourne les angles afin que le bout de l'effecteur suive un cercle donné par
    les points ci-dessus
    """
    return [0., 0., 0.]