# importation de modules
import pygame



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