from tabnanny import check
import pygame
from pygame.locals import *
import sys
from matplotlib import cm
import random
import numpy as np

from quantum import exp_val, hamiltonian, pqc
from scipy import interpolate
 

# Load data
n_qubits = 2
E = np.load("data_" + str(n_qubits) + "_qubits.npy")

x = np.linspace(0, 1, len(E[0]))
g = interpolate.interp2d(x, x, E, kind='cubic')
def f(params):
    return g(*params)[0]

# GUI
pygame.init()

width = 900
height = 600

DISPLAYSURF = pygame.display.set_mode((width, height), DOUBLEBUF)    #set the display mode, window title and FPS clock
pygame.display.set_caption('Quantum Marcher')
FPSCLOCK = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 24)
font1 = pygame.font.Font('freesansbold.ttf', 16)

n = 100
sq_size = 5

sb_size = 300
center_x = DISPLAYSURF.get_rect().centerx - sb_size // 2
center_y = DISPLAYSURF.get_rect().centery

max_x = center_x + (n - n//2) * sq_size
max_y = center_y + (n - n//2) * sq_size
min_x = center_x - (n//2) * sq_size
min_y = center_y - (n//2) * sq_size

c_size = 10  #circle size 
step_size = 5 #5 pixels per every move 

curr_alpha = 0
curr_beta = 1
viridis = cm.get_cmap('viridis', 100) #color map

params = [0.0, 0.0]
c_x = min_x + (max_x - min_x) * params[curr_alpha]
c_y = min_y + (max_y - min_y) * params[curr_beta] 

def create_background():
    background = []
    for i in range(n):
        row = []
        for j in range(n):
            tmp = [params[it] for it in range(len(params))]
            tmp[curr_alpha] = i/n
            tmp[curr_beta] = j/n
            cr, cg, cb, _ = viridis(f(tmp))
            color = (255 * cr, 255 * cg, 255 * cb)
            row.append(color)
        background.append(row)
    return background #store in array don't want to recalculate every timne 

def draw():
    for i in range(n):
        for j in range(n):
            tmp = [params[it] for it in range(len(params))]
            tmp[curr_alpha] = i/n
            tmp[curr_beta] = j/n
            color = background[i][j]
            pygame.draw.rect(DISPLAYSURF, color, 
                    (center_x + (i - n//2) * sq_size, 
                    center_y + (j - n//2) * sq_size, 
                    sq_size, sq_size))

            
    pygame.draw.circle(DISPLAYSURF, (255, 0, 0), (c_x, c_y), c_size)
    
    text = font1.render(f'{round(f(params), 2)}', True, (0, 0, 0), (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (c_x, c_y + c_size + 16)
    DISPLAYSURF.blit(text, textRect)

    # draw text for axis
    text = font.render(f'Parameter {curr_alpha}', True, (0, 255, 0), (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (center_x, min_y - 16)
    DISPLAYSURF.blit(text, textRect)

    text = font.render(f'Parameter {curr_beta}', True, (0, 255, 0), (0, 0, 0))
    text = pygame.transform.rotate(text, 90)
    textRect = text.get_rect()
    textRect.center = (min_x - 16, center_y)
    DISPLAYSURF.blit(text, textRect)

    if f(params) < 0.001:
        text = font.render("Congratulations, you reached the minimum!", True, (0, 0, 255), (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (center_x, max_y)
        DISPLAYSURF.blit(text, textRect)

    circ_fig = pygame.image.load("pqc_2.png")
    DISPLAYSURF.blit(circ_fig, (max_x + 20, 100)) 

    H_fig = pygame.image.load("hamiltonian_2.png")
    DISPLAYSURF.blit(H_fig, (max_x + 20, 200)) 


background = create_background()

while True:
    DISPLAYSURF.fill((0,0,0)) #fill black
    draw() #draw surface 
    
    keys = pygame.key.get_pressed()
    if keys[K_RIGHT]:
        c_x = min(c_x + step_size, max_x)
    if keys[K_LEFT]:
        c_x = max(c_x - step_size, min_x)
    if keys[K_UP]:
        c_y = max(c_y - step_size, min_y)
    if keys[K_DOWN]:
        c_y = min(c_y + step_size, max_y)

    params[curr_alpha] = (c_x - min_x) / (max_x - min_x) #update parameters 
    params[curr_beta] = (c_y - min_y) / (max_y - min_y)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            #A, s, space wsitch between parameters
            if event.key == K_a:
                print("Switch slice")
                curr_alpha = (curr_alpha + 1) % len(params)
                if curr_alpha == curr_beta:
                    curr_alpha = (curr_alpha + 1) % len(params)
                    background = create_background()
                    c_x = min_x + (max_x - min_x) * params[curr_alpha]
                    c_y = min_y + (max_y - min_y) * params[curr_beta]  

            if event.key == K_s:
                print("Switch slice")
                curr_beta = (curr_beta + 1) % len(params)
                if curr_beta == curr_alpha:
                    curr_beta = (curr_beta + 1) % len(params)
                    background = create_background()
                    c_x = min_x + (max_x - min_x) * params[curr_alpha]
                    c_y = min_y + (max_y - min_y) * params[curr_beta]

            if event.key == K_SPACE:
                print("Switch slice")
                tmp = random.sample(range(len(params)), 2)
                curr_alpha = tmp[0]
                curr_beta = tmp[1]
                background = create_background()
                c_x = min_x + (max_x - min_x) * params[curr_alpha]
                c_y = min_y + (max_y - min_y) * params[curr_beta]
    
    pygame.display.flip()
    FPSCLOCK.tick(30)
