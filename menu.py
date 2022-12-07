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


def get_font(size): 
    return pygame.font.Font('image jeu/font.ttf', size)

def play():
    
    main.main()


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

