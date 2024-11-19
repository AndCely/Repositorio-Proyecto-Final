import pygame
from pygame.sprite import Sprite
 
class Alien(Sprite):
    """Una clase para representar a un solo alien en la flota."""
 
    def __init__(self, ai_game):
        """Inicializa al alien y configura su posición inicial."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
 
        # Carga la imagen del alien y establece su rectángulo
        self.image = pygame.image.load("images/alien.bmp")  # Asegúrate de tener esta imagen en tu proyecto
        self.rect = self.image.get_rect()
 
        # Comienza cada nuevo alien cerca de la esquina superior izquierda
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
 
        # Almacena la posición exacta del alien
        self.x = float(self.rect.x)

    def check_edges(self):
        """Devuelve True si el alien está en el borde de la pantalla."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Mueve al alien a la derecha o a la izquierda."""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x
 
    