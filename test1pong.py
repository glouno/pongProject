import pygame
import sys
import cv2
import random, time
import numpy as np

pygame.init()
paused = False
fps = 200
#fps_clock = pygame.time.Clock()
cap = cv2.VideoCapture(0)
fps = pygame.time.Clock()

#background = pygame.image.load("starfield.png").convert()
ecran = pygame.display.set_mode([800, 600])
pygame.display.set_caption("Jeu Pong")



ball_1 = [100, 100]
ball_2 = [100, 200]
ball_3 = [100, 300]
C_RADIUS = 30
#1 = droite et -1 = gauche
def updateX(sens):
    if sens == 1: 
       ball_1[0] += 5
       ball_2[0] += 4
       ball_3[0] += 3
    if sens == -1: 
       ball_1[0] -= 5
       ball_2[0] -= 4
       ball_3[0] -= 3
#-1 = monter et 1 = descendre
def updateY(sens):
    if sens == 1: 
       ball_1[1] += 5
       ball_2[1] += 4
       ball_3[1] += 3
    if sens == -1: 
       ball_1[1] -= 5
       ball_2[1] -= 4
       ball_3[1] -= 3


def render():
    ecran.fill(pygame.Color("white"))
    pygame.draw.circle(ecran, (0, 0, 255), ball_1, C_RADIUS)
    pygame.draw.circle(ecran, (255, 0, 0), ball_2, C_RADIUS)
    pygame.draw.circle(ecran, (0, 255, 0), ball_3, C_RADIUS)
    print(f"Circle 1 : \n x = {ball_1[0]} et y = {ball_1[1]}")
    print(f"Circle 2 : \n x = {ball_2[0]} et y = {ball_2[1]}")
    print(f"Circle 3 : \n x = {ball_3[0]} et y = {ball_3[1]}")
    pygame.display.update()
    fps.tick(60)
    
    

game_pong = True
while game_pong:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit 
            #sys.exit
        
        if event.type == pygame.K_SPACE:
            paused = not paused
        if not paused:
           if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    updateX(-1)
                if event.key == pygame.K_RIGHT:
                    updateX(1)
                if event.key == pygame.K_DOWN:
                    updateY(1)
                if event.key == pygame.K_UP:
                    updateY(-1)    
        render()
   
    



    

    


    


    