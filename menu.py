
import sys
import pygame
import math

LARGEUR = 1280
HAUTEUR = 800
HAUTEUR_JOUEUR = 80
LARGEUR_JOUEUR = 20
#initialise tous les modules pygame importés
def get_font(size): 
    return pygame.font.Font('Images/font.ttf', size)


'''
La classe Sprite est la classe de base  de tous les elements graphiques visibles de la fenetre
De ce fait, notre classe Player va heriter de tous les attributs et methode de la classe 
Sprite notamment le methode super
def _init_ quant à lui est un un constructeur qui est initialisé lors de la création d'une classe
Et ce constructeur va se charrger de contenir tous les attributs de notte classe Player
Enfin le mot clé self directement generé par la fonction est un mot clé qui va nous permettre de faire
reference à notre objet tout au long de la fonction
'''
class Player (pygame.sprite.Sprite):
    def __init__(self, color, width, height ) :
        super().__init__() 
        self.color = color
        self.width = width
        self.height = height
        # Maintenant on va dessiner et configurer l'espace sur lequel on va créer nos différents joueurs
        self.image = pygame.Surface([width, height ])
        self.image.fill((255,255,255))
        self.image.set_colorkey((255,255,255))

        # On dessine ensuite le rectangle sur la surface generé plus haut
        pygame.draw.rect(self.image, self.color, [0,0, self.width, self.height ])

        # Enfin on récupere l'image conçu dans l'objet rect afin de le deplacer facilement sur le fenetre
        self.rect = self.image.get_rect()



    # fonction des déplacements des joueurs
    def monter(self, pixels):
        self.rect.y -= pixels
        # on veut s'assurer que le joueur reste dans les liùmites de la fenetre
        if (self.rect.y < 0):
            self.rect.y = 0

    def descendre(self, pixels):
        self.rect.y += pixels
        if self.rect.y > (HAUTEUR - self.height):
            self.rect.y = (HAUTEUR - self.height)
# Creation de la classe Balle

class Balle (pygame.sprite.Sprite):
    def __init__(self, color, width, height, rayon) :
        super().__init__()
        self.color = color
        self.width = width
        self.height = height
        self.rayon = rayon
        '''
        Tout comme pour les joueurs on va dessiner la surface qui va contenir le cercle et ensuite
        le recuperer dans l'objet rect pour pouvoir le déplacer sur la fenetre
        '''
        self.image = pygame.Surface([width, height])
        self.image.fill((255,255,255))
        self.image.set_colorkey((255,255,255))
        #vitesse aleatoire de la balle
        self.vitesse = [2 , 4]

        # On dessine le cercle
        pygame.draw.circle(self.image, self.color,(self.width//2, self.height//2), self.rayon)
        self.rect = self.image.get_rect()
    
    # C'est cette methode qui va faire bouger la balle
    def update (self):
        self.rect.centerx += self.vitesse[0]
        self.rect.centery += self.vitesse[1]
    
    '''
    cette derniere methode va permettre de definir une methode qui inverse la vitesse de la balle lorsque celle-ci rencontre la 
    raquette d'un joueur
    '''
    
    def rebond(self):
        self.vitesse[0] *= -1
        self.vitesse[1] *= -1

class score:
    pass

class Game:
    def __init__(self):
         # on va créer des variables booléenes qui determinent si le joueur a cliqué sur play ou sur help
        self.is_playing = False
        self.is_reading = False

        self.titleFont  =  pygame.font.Font( 'Images/font.ttf', 100 )
        self.texteRegles  =  pygame.font.Font( 'Images/font.ttf'  , 25 )

        self.Player_1= Player((50,50,50), LARGEUR_JOUEUR, HAUTEUR_JOUEUR)
        self.Player_1.rect.x = 0
        self.Player_1.rect.y = (HAUTEUR - HAUTEUR_JOUEUR) // 2
        self.Player_2 = Player((50,50,50), LARGEUR_JOUEUR, HAUTEUR_JOUEUR)
        self.Player_2.rect.x = (LARGEUR - LARGEUR_JOUEUR)
        self.Player_2.rect.y = (HAUTEUR - HAUTEUR_JOUEUR) //2

        self.balle = Balle((50,50,50), 40, 40, 20)
        self.balle.rect.centerx = LARGEUR //2
        self.balle.rect.centery = HAUTEUR // 2  

        self.score1 = 0
        self.score2 = 0
        self.font = pygame.font.Font('Images/AtariClassicExtrasmooth-LxZy.ttf',74) 
        self.message1= self.font.render (str(self.score1), 1,(50,50,50)) 
        self.message2 = self.font.render (str(self.score2), 1,(50,50,50))
        '''
        Étant donné que les différentes instances de la classe Player hérite aussi de la classe Sprite
        il faut créér une liste qui va regrouper tous les elements de cette et les ajouter à chaque fois sur notre ecran 
        '''
        # ajouter des elements graphiques à la fenetre 
        self.all_sprites_list = pygame.sprite.Group()
        self.all_sprites_list.add(self.Player_1)
        self.all_sprites_list.add(self.Player_2)
        self.all_sprites_list.add(self.balle) 
       
    def game_over(self):
        pass
    def jouer(self, fenetre):
        pygame.display.set_caption("jeu")

        
        fenetre.fill((255,255,255))
        # dessine une ligne au milieu de la fenetre
        pygame.draw.line(fenetre,(50,50,50), [LARGEUR//2, 0 ],[LARGEUR//2, HAUTEUR ], 5)

        # dessiner les différents objets à l'ecran
        self.all_sprites_list.draw(fenetre)

        # dessiner le score
        
        fenetre.blit(self.message1 ,[LARGEUR//4, 10 ])
      
        fenetre.blit(self.message2 ,[3*LARGEUR//4, 10 ])
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # on va recuperer les touches saisies par l'utilisateur dans une variable
        Keys = pygame.key.get_pressed()
        if Keys[pygame.K_UP]:
            self.Player_2.monter(10)
        if Keys[pygame.K_DOWN]:
            self.Player_2.descendre(10)
        if Keys[pygame.K_w]:
            self.Player_1.monter(10)
        if Keys[pygame.K_s]:
            self.Player_1.descendre(10)
    
            self.balle.update()
        # gestion des collisions et incrementation du score
        if self.balle.rect.centerx > (LARGEUR - LARGEUR_JOUEUR):
            self.score1 += 1
            (self.balle.rect.centerx, self.balle.rect.centery) = (LARGEUR //2, HAUTEUR //2)
            self.balle.vitesse[0] *= -1
        if self.balle.rect.centerx < LARGEUR_JOUEUR:
            self.score2 += 1
            (self.balle.rect.centerx, self.balle.rect.centery) = (LARGEUR //2,HAUTEUR //2)
            self.balle.vitesse[0] *= -1
        if self.balle.rect.centery > (HAUTEUR - LARGEUR_JOUEUR):
            self.balle.vitesse[1] *= -1
        if self.balle.rect.centery < LARGEUR_JOUEUR:
            self.balle.vitesse[1] *= -1   
    
        '''
        Sprite possede une methode collide.mask qui permet de dire si deux objets sont entrés en collisions
        Nous allons l'utiliser ici pour determiner lorsqu'une raquette frappe la balle et ainsi inverser
        la vitesse de celle-ci grave à la fonction rebond 
        '''
        if pygame.sprite.collide_mask(self.balle, self.Player_1) or pygame.sprite.collide_mask(self.balle, self.Player_2):
            self.balle.rebond()

             
        # mettre à jour la fenetre apres une modification
        pygame.display.flip() 

    def aide(self,fenetre):
        pygame.display.set_caption("aide")
       

        fenetre.fill((255,255,255))
        

        # zones cliquables
        

        #affichage à l'écran
        fenetre. blit ( self.titleFont . render ( "Règles" , True , ( 0 , 0 , 0 )), ( 370, 30 ))
        '''
        aide_retour = Button(image=None, pos=(640, 540), 
                text_input="RETOUR", font=get_font(75), base_color="Black", hovering_color="Green")
        '''
        fenetre . blit ( self.texteRegles . render ( 'Le ping pong est une sorte de tennis de table ' , True , ( 0 , 0 , 0 )), ( 20 , 150  ))
        fenetre. blit ( self.texteRegles . render ( "en mouvement constant. L'un gagne si l 'autre ne  ", True , ( 0 , 0 , 0 )), ( 20, 200 ))
        fenetre. blit ( self.texteRegles . render ( "parvient pas à intercepter la balle de l'autre" , True , ( 0 , 0 , 0 )), ( 20 , 250 ))
        fenetre. blit ( self.texteRegles . render ( 'ici les déplacements sont controlés par les mou' , True , ( 0 , 0 , 0 )), ( 20 , 300 ))
        fenetre. blit ( self.texteRegles . render ( 'vements du bras. si le joueur souhaite se déplacer' , True , ( 0 , 0 , 0 )), ( 20 , 350 ))
        fenetre. blit ( self.texteRegles . render ( "vers le haut, il souleve la main et s'il souhaite se"  , True , ( 0 , 0 , 0 )), ( 20 , 400 ))
        fenetre. blit ( self.texteRegles . render ( 'deplacer vers le bas, il baisse sa main' , True , ( 0 , 0 , 0 )), ( 20 , 450 ))
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
       
    def score(self):
    
        fenetre.fill((255,255,255))
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

pygame.init ()
# creation de la fenetre de menu 
pygame.display.set_caption(" MENU ")

fenetre = pygame.display.set_mode ((LARGEUR, HAUTEUR))

# charger l'image de fond de la fenetre de menu
background = pygame.image.load('Images/BACK2.jpg')

icone = pygame.image.load('Images/ICONE.png')
pygame.display.set_icon(icone)
# chargement des différents boutons de la page d'accueil
Bouton_play = pygame.image.load('Images/bouton_play.png')
# redimensioner les différentes images
Bouton_play = pygame.transform.scale(Bouton_play, (400,150))
Bouton_play_rect = Bouton_play.get_rect()
Bouton_play_rect.x = math.ceil(fenetre.get_width()/3.33)
Bouton_play_rect.y = 100
Bouton_score = pygame.image.load('Images/bouton_score.png')
Bouton_score = pygame.transform.scale(Bouton_score, (400,150))
Bouton_score_rect = Bouton_score.get_rect()
Bouton_score_rect.x = math.ceil(fenetre.get_width()/3.33)
Bouton_score_rect.y = 300
Bouton_help = pygame.image.load('Images/bouton_aide.png')
Bouton_help = pygame.transform.scale(Bouton_help, (400,150))
Bouton_help_rect = Bouton_help.get_rect()
Bouton_help_rect.x = math.ceil(fenetre.get_width()/3.33)
Bouton_help_rect.y = 500
Bouton_quitter = pygame.image.load('Images/bouton_sortie.png')
Bouton_quitter = pygame.transform.scale(Bouton_quitter, (400,150))
Bouton_quitter_rect = Bouton_quitter.get_rect()
Bouton_quitter_rect.x = math.ceil(fenetre.get_width()/3.33)
Bouton_quitter_rect.y = 700 

# chargement du jeu
g = Game()

jeu_en_cours = True

while jeu_en_cours:
    
    fenetre.blit(background, (0,-200))
    fenetre.blit(Bouton_play,Bouton_play_rect)
    fenetre.blit(Bouton_help, Bouton_score_rect)
    fenetre.blit(Bouton_score, Bouton_help_rect)
    fenetre.blit(Bouton_quitter, Bouton_quitter_rect)
    if g.is_playing:
        g.jouer(fenetre)
    elif g.is_reading:
        g.aide(fenetre)
    pygame.display.flip()

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() 
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if Bouton_play_rect.collidepoint(event.pos):
                    g.is_playing = True
                elif Bouton_help_rect.collidepoint(event.pos):
                    g.is_reading = True
                elif Bouton_score_rect.collidepoint(event.pos):
                    g.score     
pygame.quit()       
