import pygame
from Graphics import *
from State import State
from Env import Env
from Human_Agent import Human_Agent
from Random_Agent import Random_Agent
from DQN_Agent import DQN_Agent
import shutil
import os
import random
import numpy as np

pygame.init()

PATH = "Data\DQN_PARAM_2M.pth"
clock = pygame.time.Clock()
graphics = Graphics()
env = Env(State())
player1 = DQN_Agent(1, PATH, train=False, env=env)
player2 = Human_Agent(2,env)



run = True
player = player1
env.state.end_of_game = 3
color = "red"

def switch_players(player):
    if player == player1:
        return player2
    else:
        return player1
    

while run:
    clock.tick(FPS)
    events = pygame.event.get()

    pygame.display.update()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
    action = player.get_action(events = events,state= env.state)
    if action is not None:
        graphics.draw_animation(action, env.state.board, color)
        if color == "red":
            color = "yellow"
        else:
            color = "red"
        env.move(action)
        player = switch_players(player)
    graphics.draw(env.state)
    pygame.time.delay(200)
    if env.state.end_of_game != 0:
        while env.state.end_of_game != 0:
            pygame.display.update()
            graphics.draw(env.state)
            clock.tick(FPS)
            events = pygame.event.get()
            if run == False:
                break
            for event in events:
                if event.type == pygame.QUIT:
                    run = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    x,y = pos
                    if y<765 and y>745 and x<500 and x>300:
                        env = Env(State())
                        player1 = DQN_Agent(1, "Data\DQN_PARAM_30K.pth", train=False, env=env)
                        player2 = Human_Agent(2,env)
                        player = player1
                        color="red"
                        env.state.end_of_game = 0

                    
                
            


