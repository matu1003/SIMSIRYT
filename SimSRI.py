import pygame
from matplotlib import pyplot as plt
from random import randint, random, randrange


WIN_W = 1300
WIN_H = 800

fig = plt.figure()

win = pygame.display.set_mode((WIN_W, WIN_H))
pygame.display.set_caption("Simulation SRI")
win.fill((255, 255, 255))

# Parametre de la simulation
vitesse = 3
pop_depart = 300
cont_depart = 2
cont_rad = 20
fps = 30
duree_maladie = 3
###############

individus = []
contamines = []
nb_cont = []
susceptibles = []
nb_susc = []
retablies = []
nb_ret = []


for ID in range(pop_depart):
    indiv = {}
    
    x = randint(30, WIN_W-30)
    indiv['x'] = x
    
    y = randint(30, WIN_H-30)
    indiv['y'] = y
    
    vx = random() * vitesse *2
    vx -= vitesse
    indiv['vx'] = vx
    
    vy = ((vitesse)**2 - vx**2)**0.5
    signe = randrange(-1, 2, 2)
    indiv['vy'] = signe * vy
    
    if len(contamines) < cont_depart:
        indiv['cont'] = True
        indiv['couleur'] = (150, 200, 0)
        indiv['duree_infection'] = 0
        contamines.append(ID)
    else:
        indiv['cont'] = False
        indiv['couleur'] = (0, 150, 200)
        susceptibles.append(ID)    
    
    individus.append(indiv)
    
    
    
def afficher(indiv, win):
    couleur = indiv['couleur']
    x = indiv['x']
    y = indiv['y']
    pygame.draw.circle(win, couleur, (round(x), round(y)), 7)
    if indiv['cont']:
        pygame.draw.circle(win, couleur, (round(x), round(y)), cont_rad, 1)
    

def deplacer(indiv):
    
    if indiv['x'] < 20 or indiv['x'] > WIN_W - 20:
        indiv['vx'] *= -1
        
    if indiv['y'] < 20 or indiv['y'] > WIN_H - 20:
        indiv['vy'] *= -1
        
    indiv['x'] += indiv['vx']
    indiv['y'] += indiv['vy']
    
    
def analyser(IDindiv):
    indiv = individus[IDindiv]
    if IDindiv in susceptibles:
        for IDinfecte in contamines:
            indivinf = individus[IDinfecte]
            dist = ((indiv['x']-indivinf['x'])**2+ (indiv['y']-indivinf['y'])**2)**0.5
            if dist < cont_rad:
                indiv['cont'] = True
                indiv['couleur'] = (150, 200, 0)
                indiv['duree_infection'] = 0
                break
            
        if indiv['cont']:
            contamines.append(IDindiv)
            susceptibles.remove(IDindiv)
    
    elif indiv['cont']:
        indiv['duree_infection'] += 1
        if indiv['duree_infection'] > fps * duree_maladie:
            indiv['cont'] = False
            indiv['couleur'] = (150, 150, 150)
            contamines.remove(IDindiv)
            retablies.append(IDindiv)
        
    


clock = pygame.time.Clock()
sim_active = True
while sim_active:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sim_active = False
            pygame.quit()
    
    if not(sim_active):
        break
    
    win.fill((255, 255, 255))
    
    for indiv in individus:
        deplacer(indiv)
        
    for IDindiv in range(pop_depart):
        analyser(IDindiv)
    
    for indiv in individus:
        afficher(indiv, win)
    
    nb_cont.append(len(contamines))
    nb_ret.append(len(retablies))
    nb_susc.append(len(susceptibles))
    
    pygame.display.update()
    clock.tick(fps)
    
    
plt.plot(nb_cont, c=(0.58, 0.78, 0), label = 'Infectee')
plt.plot(nb_susc, c = (0, 0.58, 0.78), label = 'Susceptibles')
plt.plot(nb_ret, c=(0.58, 0.58, 0.58), label = 'Retablies')
plt.legend()
plt.show()
    





