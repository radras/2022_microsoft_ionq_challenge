from curses import KEY_UP
from re import X
from numpy import fmax, true_divide
import pygame
from pygame.locals import *
import sys
from matplotlib import cm
from matplotlib.colors import to_rgb
import random
 
pygame.init()
 
DISPLAYSURF = pygame.display.set_mode((600, 600), DOUBLEBUF)    #set the display mode, window title and FPS clock
pygame.display.set_caption('Hill Climbing')
FPSCLOCK = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 16)

n = 100
sq_size = 5
max_x = DISPLAYSURF.get_rect().centerx + (n - n//2) * sq_size
max_y = DISPLAYSURF.get_rect().centery + (n - n//2) * sq_size
min_x = DISPLAYSURF.get_rect().centerx - (n//2) * sq_size
min_y = DISPLAYSURF.get_rect().centery - (n//2) * sq_size

c_size = 10
step_size = 5

curr_alpha = 0
curr_beta = 1
viridis = cm.get_cmap('viridis', 100)

def g(p):
    # return (p[0] + p[1] + p[2]) / 3
    return 1 - ((p[0] - 0.5) ** 2 + (p[1] - 0.5) ** 2 + (p[2] - 0.5) ** 2) * 4 / 3

params = [0.0, 0.0, 0.0]
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
            cr, cg, cb, _ = viridis(g(tmp))
            color = (255 * cr, 255 * cg, 255 * cb)
            row.append(color)
        background.append(row)
    return background

def draw():
    for i in range(n):
        for j in range(n):
            tmp = [params[it] for it in range(len(params))]
            tmp[curr_alpha] = i/n
            tmp[curr_beta] = j/n
            color = background[i][j]
            pygame.draw.rect(DISPLAYSURF, color, 
                    (DISPLAYSURF.get_rect().centerx + (i - n//2) * sq_size, 
                    DISPLAYSURF.get_rect().centery + (j - n//2) * sq_size, 
                    sq_size, sq_size))

            
    pygame.draw.circle(DISPLAYSURF, (255, 255, 255), (c_x, c_y), c_size)

    # draw text for axis
    text = font.render(f'Parameter {curr_alpha}', True, (0, 255, 0), (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (DISPLAYSURF.get_rect().centerx, min_y - 16)
    DISPLAYSURF.blit(text, textRect)

    text = font.render(f'Parameter {curr_beta}', True, (0, 255, 0), (0, 0, 0))
    text = pygame.transform.rotate(text, 90)
    textRect = text.get_rect()
    textRect.center = (min_x - 16, DISPLAYSURF.get_rect().centery)
    DISPLAYSURF.blit(text, textRect)

background = create_background()

def check_finish():
    finish = True
    for p in params:
        if abs(1 - p) > 0.01:
            finish = False
            break
    if finish:
        print("CONGRATS!!!")

while True:
    DISPLAYSURF.fill((0,0,0))
    draw()
    
    keys = pygame.key.get_pressed()

    if keys[K_RIGHT]:
        c_x = min(c_x + step_size, max_x)
    if keys[K_LEFT]:
        c_x = max(c_x - step_size, min_x)
    if keys[K_UP]:
        c_y = max(c_y - step_size, min_y)
    if keys[K_DOWN]:
        c_y = min(c_y + step_size, max_y)

    params[curr_alpha] = (c_x - min_x) / (max_x - min_x)
    params[curr_beta] = (c_y - min_y) / (max_y - min_y)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

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
