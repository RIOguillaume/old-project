import json
import math

# Exemple de kapla:
K1 = { 'base' : (1.2, -3.5, 0.0), # le kapla a un sommet en (1.2, -3.5, 0.0) (dans le repère monde)                                            \
       'atitude' : (70,20,25), # le kapla posé horizontalement (70 le long des x, 20 le long des y, 25 le long de z)                           \
       'pivot' : 60 # il est tourné autour de l'axe vertical au dessus de son point de base (ci-dessus) de 60° de l'axe des x vers l'axe des y \
     }
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
    print(tabConstruction)
    return tabConstruction


# Exemple de construction:
C =[                                                             \
    { 'base' : (0,0,0), 'atitude' : (25,20,70), 'pivot' : 90},    \
    { 'base' : (50,0,0), 'atitude' : (25,20,70), 'pivot' : 90}, \
    { 'base' : (70,0,0), 'atitude' : (25,20,70), 'pivot' : 90},\
    { 'base' : (120,0,0), 'atitude' : (25,20,70), 'pivot' : 90},\
    { 'base' : (0,0,70), 'atitude' : (70,25,20), 'pivot' : 0},    \
    { 'base' : (75,0,70), 'atitude' : (70,25,20), 'pivot' : 0},    \
    { 'base' : (30,0,90), 'atitude' : (25,20,70), 'pivot' : 90}, \
    { 'base' : (80,0,90), 'atitude' : (25,20,70), 'pivot' : 90}, \
    { 'base' : (30,0,180), 'atitude' : (70,25,20), 'pivot' : 0},    \
    
]
print("---------------------------------------")
algoCreationTableau(C)
print("---------------------------------------")
filename = 'construction.json'

# Ecriture du fichier json
print('Ecriture du fichier d\'encodage d\'une construction:')
with open(filename, 'w') as f:
    json.dump(C,f)

# Lecture d'un fichier de construction:
print('Lecture d\'un fichier d\'encodage d\'une construction:')
with open(filename, 'r') as f:
    D = json.load(f)
print(D) # la construction est disponible pour traitement 
