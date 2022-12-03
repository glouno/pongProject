#importation des modules
import pygame


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
        if self.rect.y > (600 - self.height):
            self.rect.y = (400 - self.height)
