import pygame, sys
import main
LARGEUR = 1280
HAUTEUR = 900
LARGEUR_JOUEUR = 20
HAUTEUR_JOUEUR = 80

pygame.init()

fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Menu")
icone = pygame.image.load('image jeu/ICONE.png')
pygame.display.set_icon(icone)

background = pygame.image.load('image jeu/BACK2.jpg')
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

class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)


def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font('image jeu/font.ttf', size)

def play():
    
    main.main()

    '''
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        pygame.display.set_caption("jeu")

        
        fenetre.fill((255,255,255))
        # dessine une ligne au milieu de la fenetre
        pygame.draw.line(fenetre,(50,50,50), [LARGEUR//2, 0 ],[LARGEUR//2, HAUTEUR ], 5)

        Player_1= Player((50,50,50), LARGEUR_JOUEUR, HAUTEUR_JOUEUR)
        Player_1.rect.x = 0
        Player_1.rect.y = (HAUTEUR - HAUTEUR_JOUEUR) // 2
        Player_2 = Player((50,50,50), LARGEUR_JOUEUR, HAUTEUR_JOUEUR)
        Player_2.rect.x = (LARGEUR - LARGEUR_JOUEUR)
        Player_2.rect.y = (HAUTEUR - HAUTEUR_JOUEUR) //2

        balle = Balle((50,50,50), 40, 40, 20)
        balle.rect.centerx = LARGEUR //2
        balle.rect.centery = HAUTEUR // 2  

        score1 = 0
        score2 = 0
        font = pygame.font.Font('image jeu/AtariClassicExtrasmooth-LxZy.ttf',74)
        message1 = font.render ( str(score1), 1,(50,50,50))
        message2 = font.render ( str(score2), 1,(50,50,50)) 
        
        #Étant donné que les différentes instances de la classe Player hérite aussi de la classe Sprite
        #il faut créér une liste qui va regrouper tous les elements de cette et les ajouter à chaque fois sur notre ecran 
        
        # ajouter des elements graphiques à la fenetre 
        all_sprites_list = pygame.sprite.Group()
        all_sprites_list.add(Player_1)
        all_sprites_list.add(Player_2)
        all_sprites_list.add(balle) 

        


        # dessiner les différents objets à l'ecran
        all_sprites_list.draw(fenetre)

        # dessiner le score
        fenetre.blit ( message1 , [LARGEUR//4, 10 ] )
        fenetre.blit ( message2, [3*LARGEUR//4, 10 ] )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
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
        if balle.rect.centerx > (LARGEUR - LARGEUR_JOUEUR):
            score1 += 1
            (balle.rect.centerx, balle.rect.centery) = (LARGEUR //2, HAUTEUR //2)
            balle.vitesse[0] *= -1
        if balle.rect.centerx < LARGEUR_JOUEUR:
            score2 += 1
            (balle.rect.centerx, balle.rect.centery) = (LARGEUR //2,HAUTEUR //2)
            balle.vitesse[0] *= -1
        if balle.rect.centery > (HAUTEUR - LARGEUR_JOUEUR):
            balle.vitesse[1] *= -1
        if balle.rect.centery < LARGEUR_JOUEUR:
            balle.vitesse[1] *= -1   
    
        
        #Sprite possede une methode collide.mask qui permet de dire si deux objets sont entrés en collisions
        #Nous allons l'utiliser ici pour determiner lorsqu'une raquette frappe la balle et ainsi inverser
        #la vitesse de celle-ci grave à la fonction rebond 
        
        if pygame.sprite.collide_mask(balle, Player_1) or pygame.sprite.collide_mask(balle, Player_2):
            balle.rebond()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            #if event.type == pygame.MOUSEBUTTONDOWN:
                #if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    #main_menu()
            
        pygame.display.update()

        '''

def aide():
    while True:
        HELP_MOUSE_POS = pygame.mouse.get_pos()

        fenetre.fill("white")
        titleFont  =  pygame.font.Font( 'image jeu/font.ttf' , 100 )
       
        texteRegles  =  pygame.font.Font( 'image jeu/font.ttf'  , 25 )

        # zones cliquables
        

        #affichage à l'écran
        fenetre.blit ( titleFont . render ( "Règles" , True , ( 0 , 0 , 0 )), ( 370, 30 ))
        bouton_back = Button(image=None, pos=(640, 540), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")
        fenetre.blit ( texteRegles . render ( 'Le ping pong est une sorte de tennis de table ' , True , ( 0 , 0 , 0 )), ( 20 , 150  ))
        fenetre.blit ( texteRegles . render ( "en mouvement constant. L'un gagne si l 'autre ne  ", True , ( 0 , 0 , 0 )), ( 20, 200 ))
        fenetre.blit ( texteRegles . render ( "parvient pas à intercepter la balle de l'autre" , True , ( 0 , 0 , 0 )), ( 20 , 250 ))
        fenetre.blit ( texteRegles . render ( 'ici les déplacements sont controlés par les mou' , True , ( 0 , 0 , 0 )), ( 20 , 300 ))
        fenetre.blit ( texteRegles . render ( 'vements du bras. si le joueur souhaite se déplacer' , True , ( 0 , 0 , 0 )), ( 20 , 350 ))
        fenetre.blit ( texteRegles . render ( "vers le haut, il souleve la main et s'il souhaite se"  , True , ( 0 , 0 , 0 )), ( 20 , 400 ))
        fenetre.blit ( texteRegles . render ( 'deplacer vers le bas, il baisse sa main' , True , ( 0 , 0 , 0 )), ( 20 , 450 ))
    

        

        bouton_back.changeColor(HELP_MOUSE_POS)
        bouton_back.update(fenetre)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_back.checkForInput(HELP_MOUSE_POS):
                  main_menu()

        pygame.display.update()    

def score():
    while True:
        SCORE_MOUSE_POS = pygame.mouse.get_pos()

        fenetre.fill("white")
        titleFont  =  pygame.font.Font( 'image jeu/font.ttf', 100 )
       
        texteRegles  =  pygame.font.Font( 'image jeu/font.ttf' , 25)
        

        #affichage à l'écran
        fenetre.blit ( titleFont . render ( "SCORE" , True , ( 0 , 0 , 0 )), ( 370, 30 ))

        score_back = Button(image=None, pos=(640, 540), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")
        
        score_back.changeColor(SCORE_MOUSE_POS)
        score_back.update(fenetre)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if score_back.checkForInput(SCORE_MOUSE_POS):
                  main_menu()



def main_menu():
    while True:
        fenetre.blit(background, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, (182, 143, 64))
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        Bouton_play = Button(image=pygame.image.load("image jeu/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color=(215,252,212), hovering_color="White")
        Bouton_help = Button(image=pygame.image.load("image jeu/aide Rect.png"), pos=(640, 400), 
                            text_input="HELP", font=get_font(75), base_color=(215,252,212), hovering_color="White")
        Bouton_score = Button(image=pygame.image.load("image jeu/aide Rect.png"), pos=(640, 550), 
                            text_input="SCORE", font=get_font(75), base_color=(215,252,212), hovering_color="White")                   
        Bouton_quitter = Button(image=pygame.image.load("image jeu/Quit Rect.png"), pos=(640, 700), 
                            text_input="QUIT", font=get_font(75), base_color=(215,252,212), hovering_color="White")

        fenetre.blit(MENU_TEXT, MENU_RECT)

        for button in [Bouton_play,Bouton_help ,Bouton_score,Bouton_quitter ]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(fenetre)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if Bouton_play.checkForInput(MENU_MOUSE_POS):
                    play()
                if Bouton_help.checkForInput(MENU_MOUSE_POS):
                    aide()
                if Bouton_score.checkForInput(MENU_MOUSE_POS):
                    score()
                if Bouton_quitter.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()

