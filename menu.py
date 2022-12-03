# Importation des modules importants
import pygame

from joueur import Player
from Ball import Balle

    
# initialise tous les modules pygame importés
pygame.init()

# creation de la fenetre de jeu 
fenetre = pygame.display.set_mode ((840, 600))
pygame.display.set_caption(" JEU PING PONG")

background = pygame.image.load('bg.jpg')
# changer la couleur de fond de ma fenetre     




'''
On constate que la fenetre s'ouvre et se ferme automatiquement
De ce fait, on va créer une variable de type booléenne et l'executer tant que cette variable est vraie
'''
Player_1= Player((50,50,50), 20, 80)
Player_1.rect.x = 0
Player_1.rect.y = 250
Player_2 = Player((50,50,50), 20, 80)
Player_2.rect.x = 820 
Player_2.rect.y = 250

balle = Balle((50,50,50), 40, 40, 20)
balle.rect.centerx = 420
balle.rect.centery =  300

'''
Étant donné que les différentes instances de la classe Player hérite aussi de la classe Sprite
il faut créér une liste qui va regrouper tous les elements de cette et les ajouter à chaque fois sur notre ecran 
'''


# ajouter des elements graphiques à la fenetre 

all_sprites_list = pygame.sprite.Group()

all_sprites_list.add(Player_1)
all_sprites_list.add(Player_2)

all_sprites_list.add(balle)

jeu_en_cours = True

(score1,score2) = (0,0)
'''
on va se lancer dans la collecte de donnée en creant un fichier csv qui va contenir les positions en x et en y de la balle
sa vitesse ainsi que la position en y d'un joueur 
'''
jeu_file = open('pong_csv', 'a+')
print("x, y, vx, vy, Player_n" , file= jeu_file)
# creation de la boucle d'execution du jeu et definition des differentes conditions d'execution
while jeu_en_cours:
    
    #si le joueur ferme la fenetre
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jeu_en_cours = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                jeu_en_cours = False
        elif score1 == 10 or score2 == 10:
            jeu_en_cours == False
    
    
    # on va recuperer les touches saisies par l'utilisateur dans une variable
    Keys = pygame.key.get_pressed()
    if Keys[pygame.K_UP]:
        Player_2.monter(10)
    if Keys[pygame.K_DOWN]:
        Player_2.descendre(10)
    if Keys[pygame.K_w]:
        Player_1.monter(10)
    if Keys[pygame.K_s]:
        Player_1.descendre(10)
    
    balle.update()
    # gestion des collisions et incrementation du score
    if balle.rect.centerx > 820:
        score1 += 1
        (balle.rect.centerx, balle.rect.centery) = (420, 300)
        balle.vitesse[0] *= -1
    if balle.rect.centerx < 20:
        score2 += 1
        (balle.rect.centerx, balle.rect.centery) = (420, 300)
        balle.vitesse[0] *= -1
    if balle.rect.centery > 580:
        balle.vitesse[1] *= -1
    if balle.rect.centery < 20:
        balle.vitesse[1] *= -1   
    
    '''
    Sprite possede une methode collide.mask qui permet de dire si deux objets sont entrés en collisions
    Nous allons l'utiliser ici pour determiner lorsqu'une raquette frappe la balle et ainsi inverser
    la vitesse de celle-ci grave à la fonction rebond 
    '''
    if pygame.sprite.collide_mask(balle, Player_1) or pygame.sprite.collide_mask(balle, Player_2):
        balle.rebond()
    
    fenetre.fill((255,255,255))
    
    # dessine une ligne au milieu de la fenetre
    pygame.draw.line(fenetre,(50,50,50), [840//2, 0 ],[840//2, 600 ], 5)
    
    # dessiner le score
    font = pygame.font.Font('/Users/mballaelisabeth/Desktop/atari-classic-font/AtariClassicExtrasmooth-LxZy.ttf',74)
    message = font.render (str(score1), 1,(50,50,50))
    fenetre.blit(message,[840//4, 10 ])
    message = font.render (str(score2), 1,(50,50,50))
    fenetre.blit(message,[3*840//4, 10 ])

    # dessiner les différents objets à l'ecran
    all_sprites_list.draw(fenetre)
    # mettre à jour la fenetre apres une modification
    pygame.display.flip() 
    print( "{},{},{},{},{}".format(balle.rect.centerx, balle.rect.centery,balle.vitesse[0], balle.vitesse[1],Player_2.rect.y ),file = jeu_file)
pygame.quit()            
