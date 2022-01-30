from tabnanny import check
import pygame
from pygame.locals import *
import sys
from matplotlib import cm
import pygamepopup
from pygamepopup.components import InfoBox, Button
import os
from pygamepopup.menu_manager import MenuManager
import os, sys
import random
import random
import numpy as np
from quantum import exp_val, hamiltonian, pqc
from scipy import interpolate


while True:
    level = input("Choose level: ")

    if level == "1":
        # Load data
        n_qubits = 2
        n_params = n_qubits
        E = np.load("QuantumMarcher/data_" + str(n_qubits) + "_qubits.npy")

        x = np.linspace(0, 1, len(E[0]))
        def f(params):
            return interpolate.interpn(tuple([x for i in range(n_qubits)]), E, params)[0]
        break
    elif level == "2":
        n_params = 3
        def f(params):
            return (1 + np.cos(np.pi * params[0]) * np.cos(np.pi * params[1]) * np.cos(np.pi * params[2]) + np.sin(np.pi * params[2]) ** 2) / 3
        break
    elif level == "3":
        n_params = 4
        def f(params):
            return (np.cos(np.pi * params[0]) * np.sin(np.pi * params[1]) + np.cos(np.pi * params[3]) * np.sin(np.pi * params[2]) + 2) / 4
        break
    else:
        print("Please choose one of the following levels: 1, 2, 3")


TIMER_START = 10
counter = TIMER_START

STATE_PLAY = 0
STATE_WIN = 1
STATE_LOSE = 2
STATE_SEL = STATE_PLAY

pygame.init()
pygamepopup.init()
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 1000)
running = True

DISPLAYSURF = pygame.display.set_mode((900, 600), DOUBLEBUF)    #set the display mode, window title and FPS clock

def leave():
    global running 
    running = False
    pygame.quit()
    sys.exit()


pygame.display.set_caption('Quantum Marcher')
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

params = np.zeros(n_params)
c_x = min_x + (max_x - min_x) * params[curr_alpha]
c_y = min_y + (max_y - min_y) * params[curr_beta] 


def restart():
    global curr_alpha, curr_beta, STATE_SEL, STATE_PLAY, counter, TIMER_START, c_x, c_y
    global min_x, min_y, max_y, max_x, params

    curr_alpha = 0
    curr_beta = 1
    c_x = min_x + (max_x - min_x) * params[curr_alpha]
    c_y = min_y + (max_y - min_y) * params[curr_beta]
    STATE_SEL = STATE_PLAY
    counter = TIMER_START

class MainMenuScene():
    def __init__(self, screen: pygame.surface.Surface, restart_callback, leave):
        self.screen = screen
        self.menu_manager = MenuManager(screen)
        self.exit_request = False

        self.create_main_menu_interface()



    def create_main_menu_interface(self):
        main_menu = InfoBox(
            "You win!!" if STATE_SEL == STATE_WIN else "Game Over",
            [
                [
                    Button(
                        title="Play again",
                        callback=restart
                    )
                ],
                [
                    Button(title="Exit", callback=leave)
                ],
            ],
            has_close_button=False,
        )
        self.menu_manager.open_menu(main_menu)

    def exit(self):
        self.exit_request = True

    def display(self) -> None:
        self.menu_manager.display()

    def motion(self, position: pygame.Vector2) -> None:
        self.menu_manager.motion(position)

    def click(self, button: int, position: pygame.Vector2) -> bool:
        self.menu_manager.click(button, position)
        return self.exit_request

mmscene = MainMenuScene(screen=DISPLAYSURF, restart_callback=restart, leave=leave)

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

def draw_game():
    # draw text for axes
    text = font.render(f'Parameter {curr_alpha}', True, (0, 255, 0), (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (center_x, min_y - 16)
    DISPLAYSURF.blit(text, textRect)

    text = font.render(f'Parameter {curr_beta}', True, (0, 255, 0), (0, 0, 0))
    text = pygame.transform.rotate(text, 90)
    textRect = text.get_rect()
    textRect.center = (min_x - 16, center_y)
    DISPLAYSURF.blit(text, textRect)

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

    if level == "1":
        circ_fig = pygame.image.load("QuantumMarcher/pqc_" + str(n_qubits) + ".png")
        DISPLAYSURF.blit(circ_fig, (max_x + 20, 100)) 

        H_fig = pygame.image.load("QuantumMarcher/hamiltonian_" + str(n_qubits) + ".png")
        DISPLAYSURF.blit(H_fig, (max_x + 20, 200)) 
    else:
        text = font.render("Generated with formula", True, (0, 0, 0), (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (max_x + 150, min_y + 50)
        DISPLAYSURF.blit(text, textRect)

    if f(params) < 0.001:
        text = font.render("Congratulations, you reached the minimum!", True, (0, 0, 255), (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (center_x, max_y)
        DISPLAYSURF.blit(text, textRect)
        STATE_SEL = STATE_WIN

    timer_text = font.render(f"Time: {counter}", True, (255,255,255), (0,0,0))
    timer_text_rect = timer_text.get_rect()
    timer_text_rect.center = (max_x - 16, min_y - 16)
    DISPLAYSURF.blit(timer_text, timer_text_rect)
    

background = create_background()

while running:
    if STATE_SEL == STATE_PLAY:
        DISPLAYSURF.fill((0,0,0))
        draw_game()
        
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
            if event.type == pygame.USEREVENT:
                if counter > 0:
                    counter -= 1
                else: 
                    STATE_SEL = STATE_LOSE
                    
            if event.type == KEYUP:
                if event.key == K_a:
                    counter = TIMER_START
                    curr_alpha = (curr_alpha + 1) % len(params)
                    if curr_alpha == curr_beta:
                        curr_alpha = (curr_alpha + 1) % len(params)
                        background = create_background()
                        c_x = min_x + (max_x - min_x) * params[curr_alpha]
                        c_y = min_y + (max_y - min_y) * params[curr_beta]  

                if event.key == K_s:
                    counter = TIMER_START
                    curr_beta = (curr_beta + 1) % len(params)
                    if curr_beta == curr_alpha:
                        curr_beta = (curr_beta + 1) % len(params)
                        background = create_background()
                        c_x = min_x + (max_x - min_x) * params[curr_alpha]
                        c_y = min_y + (max_y - min_y) * params[curr_beta]

                if event.key == K_SPACE:
                    counter = TIMER_START
                    tmp = random.sample(range(len(params)), 2)
                    curr_alpha = tmp[0]
                    curr_beta = tmp[1]
                    background = create_background()
                    c_x = min_x + (max_x - min_x) * params[curr_alpha]
                    c_y = min_y + (max_y - min_y) * params[curr_beta]
    if STATE_SEL == STATE_WIN:
        win_modal()
    if STATE_SEL == STATE_LOSE:
        mmscene.display()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            running = False
        elif event.type == pygame.MOUSEMOTION:
            mmscene.motion(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 or event.button == 3:
                running = not mmscene.click(event.button, event.pos)
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

    pygame.display.flip()
    FPSCLOCK.tick(30)
    clock.tick(60)
pygame.quit()
exit()