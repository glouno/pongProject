
import pygame
import math
import sys
from pygame.locals import*
import numpy as np
import random, time
from pygame.locals import *

import cv2 as cv
from cvzone.HandTrackingModule import HandDetector

# Loading all sounds
pygame.mixer.init()  ## For sound
shooting = pygame.mixer.Sound("/Users/mballaelisabeth/Desktop/sound/bounce.ogg")


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
window_height = 300
window_width = 500
display_surf = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("menu")
# Loading all images

# background = pygame.image.load("starfield.png").convert()
background = pygame.image.load('/Users/mballaelisabeth/Desktop/starfield.png')

icone = pygame.image.load('/Users/mballaelisabeth/Desktop/image jeu/ICONE.png')
pygame.display.set_icon(icone)

Bouton_play = pygame.image.load('/Users/mballaelisabeth/Desktop/button.png')
Bouton_play = pygame.transform.scale(Bouton_play, (200,100))
Bouton_play_rect = Bouton_play.get_rect()
Bouton_play_rect.x = math.ceil(display_surf.get_width()/3.33)
Bouton_play_rect.y = math.ceil(display_surf.get_height()/2)

fps = 200
fps_clock = pygame.time.Clock()
#cap = cv2.VideoCapture(0)

# Threshold for binary
lower = np.array([60,25,30], dtype = 'uint8')
upper = np.array([255,220,255], dtype = 'uint8')
flag = 0

#definir les axes 
class Paddle:
    def __init__(self, x, w, h):
        self.w = w
        self.h = h
        self.x = x
        self.y = window_height / 2
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)


    def draw(self):
        pygame.draw.rect(display_surf, WHITE, self.rect)


#le mouvement du rectangle
    def detectMove(self, cy):
        self.rect.y = int(cy)
        self.draw()

#barre de jeu de la machine
class AutoPaddle(Paddle):
    def __init__(self, x, w, h, speed, ball):
        super().__init__(x, w, h)
        self.speed = speed
        self.ball = ball

#mouvement automatique
    def move(self):
        if self.ball.dir_x == 1:
            if self.rect.y + self.rect.h/2 < self.ball.rect.bottom:
                self.rect.y += self.speed
            if self.rect.y + self.rect.h/2 > self.ball.rect.bottom:
                self.rect.y -= self.speed


class ScoreBoard:
    def __init__(self, score=0):
        self.x = window_width - 150
        self.y = 20
        self.score = score
        self.font = pygame.font.Font('/Users/mballaelisabeth/Desktop/font.ttf', 20)

#affichage du score
    def display(self, score):
        result_srf = self.font.render('Score : %s' % score, True, WHITE)
        result_rect = result_srf.get_rect()
        result_rect.topleft = (window_width - 150, 20)
        display_surf.blit(result_srf, result_rect)


class Ball:
    def __init__(self, x, y, w, h, speed):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.speed = speed
        self.dir_x = -1  # left = -1 and right = 1
        self.dir_y = -1   # up = -1 and down = 1
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self):
        pygame.draw.rect(display_surf, WHITE, self.rect)

#le rebon de la ball
    def bounce(self, axis):
        if axis == 'x':
            self.dir_y *= -1
        if axis == 'y':
            self.dir_x *= -1
        shooting.play()

#controle la direction de la ball (haut, bas, gauche, droite)
    def hit_ceiling(self):
        if self.dir_y == -1 and self.rect.top <= self.h:
            return True
        else:
            return False

    def hit_floor(self):
        if self.dir_y == 1 and self.rect.bottom >= window_height - self.h:
            return True
        else:
            return False

    def hit_wall(self):
        if (self.dir_x == -1 and self.rect.left <= self.w) or (self.dir_x == 1 and self.rect.right >= window_width - self.w):
            return True
        else:
            return False

#la barre de jeu de l'utilisateur
    def hit_paddle_user(self, paddle):
        if self.rect.left == paddle.rect.right and self.rect.bottom >= paddle.rect.top and self.rect.top <= paddle.rect.bottom:
            return True
        else:
            return False

#la barre de jeu de l'ordinateur
    def hit_paddle_computer(self, paddle):
        if self.rect.right == paddle.rect.left and self.rect.bottom >= paddle.rect.top and self.rect.top <= paddle.rect.bottom:
            return True
        else:
            return False


    def move(self):
        self.rect.x += (self.dir_x * self.speed)
        self.rect.y += (self.dir_y * self.speed)
        if self.hit_ceiling() or self.hit_floor():
            self.bounce('x')


class Game:
    def __init__(self, line_thickness=10, speed=5):
        self.line_thickness = line_thickness
        self.speed = speed
        ball_x = window_width / 2
        ball_y = window_height / 2
        ball_w = self.line_thickness
        ball_h = self.line_thickness
        self.ball = Ball(ball_x, ball_y, ball_w, ball_h, self.speed)
        self.paddles = {}
        paddle_x = 20
        paddle_w = self.line_thickness
        paddle_h = 50
        self.paddles['user'] = Paddle(paddle_x, paddle_w, paddle_h)
        self.paddles['computer'] = AutoPaddle(window_width - paddle_x - 10, paddle_w, paddle_h, self.speed, self.ball)
        self.score = ScoreBoard()

#la fenêtre de jeu
    def draw_arena(self):
        display_surf.blit(background, [0,0])


    def update(self):
        self.draw_arena()
        self.ball.draw()
        self.paddles['user'].draw()
        self.paddles['computer'].draw()
        self.ball.move()
        self.paddles['computer'].move()
        if self.ball.hit_paddle_user(self.paddles['user']):
            self.ball.bounce('y')
            self.score.score += 1
        self.score.display(self.score.score)
        if self.ball.hit_paddle_computer(self.paddles['computer']):
            self.ball.bounce('y')


def main():

    pygame.init()
    game = Game()
    paused = False

    liveVideo = cv.VideoCapture(0)
    handDetector = HandDetector(detectionCon = 0.8, maxHands=2)    

    while liveVideo.isOpened():
        #_, frame = cap.read()

        ret, frame = liveVideo.read()
        frame = cv.flip(frame, 1)
        hands, frame = handDetector.findHands(frame, flipType=False)
        
        '''
        frame_resize = cv.resize(frame, (500, 400))
        grayimage = cv2.cvtColor(frame_resize, cv2.COLOR_RGB2GRAY)
        cascade_file = cv2.CascadeClassifier("fist.xml")
        fist = cascade_file.detectMultiScale(grayimage,scaleFactor=1.1,
                                            minNeighbors=5,
                                            minSize=(30, 30),
                                            flags=cv2.CASCADE_SCALE_IMAGE)

                                          
        for x, y, w, h in fist:
            k = cv2.rectangle(frame_resize, (x, y), (x + w, y + h), (255, 255, 255), 5)

            cx = int(x + (w / 2))
            cy = y -50
            cv2.circle(frame_resize, (cx, cy), 10, (255, 255, 0))
            game.paddles['user'].detectMove(cy)
        '''

        #HAND DETECTION
        #Use element number 8: INDEX_FINGER_TIP

        #for each hand we'Ll have info Like Hand--›dict{lmList,boundinqboundary, img)
        if hands:
            hand1=hands[0]                          #gives us first hand
            lmList1=hand1["lmList"]                 #List of 21 Landmarks
            bbox1=hand1["bbox"]                     #x,y,w,h of bounding box
            centerPoint1=hand1[ "center" ]          #center of the hand cx, cy
            handType1=hand1["type"]                #Left or right
            finger1=handDetector.fingersUp(hand1)
            
            #needs something to find the distance / x,y positions 
            #length, info, frame=handDetector.findDistance(lmList1[8], lmList1[12])
            yCoordinate = lmList1[8][1:2]       
            #yCoordinate = tuple(yCoordinate) #careful change data type to tuple with tuple() if doing a circle bounding box
            #cv2.circle() ...
            print(yCoordinate[0])
            print(type(yCoordinate[0]))
            game.paddles['user'].detectMove(yCoordinate[0]) #On doit écrire yCoordinate[0] parce que c'est une liste et on doit sortir l'élement)

        if len(hands)==2:
            hand2=hands[1]                          #gives us second hand
            lmList2=hand2["lmList"]                 #List of 21 Landmarks
            bbox2=hand2["bbox" ]                    #x,y, w,h of bounding box
            centerPoint2=hand2["center"]            #center of the hand cx, cy
            handType2=hand2["type" ]                #Left or right
            finger2=handDetector.fingersUp(hand2)
            #length, info, frame=handDetector.findDistance(lmList1[8],lmList2[8],frame)
            #length, info, frame=handDetector.findDistance(centerPoint1, centerPoint2, frame)



        #cv.imshow('frame', frame)

        if cv.waitKey(1) & 0xFF == ord('q'):    #waitKey(1) & 0xFF is a bitwise operation to only keep the last 8 bits and compare it to ord('q')
            break

        '''
        k = cv.waitKey(40)

        if k == ord(' '):
            paused = not paused
        '''

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
              
            #if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    paused = not paused
        

        '''
        if cv.waitKey(1) & 0x70 == ord('p'):    #waitKey(1) & 0xFF is a bitwise operation to only keep the last 8 bits and compare it to ord('q')
            paused = not paused
        '''

        if not paused:
            #cv2.imshow("contour", frame_resize) previous resize, not sure why
            cv.imshow('frame', frame)
            game.update()
            if game.ball.hit_wall():
                break
                game.update()
                
            pygame.display.update()
            fps_clock.tick(fps)
            
    print('Your score:', game.score.score)

    # After the loop release the cap object
    liveVideo.release()
    # Destroy all the windows
    cv.destroyAllWindows()
    


jeu_en_cours = True

while jeu_en_cours:
    
    display_surf.blit(background, (0,-200))
    display_surf.blit(Bouton_play,Bouton_play_rect)
    '''
    fenetre.blit(Bouton_help, Bouton_score_rect)
    fenetre.blit(Bouton_score, Bouton_help_rect)
    fenetre.blit(Bouton_quitter, Bouton_quitter_rect)
    '''
    
    pygame.display.flip()

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if Bouton_play_rect.collidepoint(event.pos):
                    main()
#if __name__ == '__main__':
#   main()
