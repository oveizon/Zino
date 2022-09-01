import pygame
from pygame.sprite import Sprite


class Djinn(Sprite):
 """ a class to rep a single djinn in the flock"""
 
 def __init__(self, ai_game,):
  """initialize the djinn and set its starting point"""
  super().__init__()
  self.screen = ai_game.screen
  self.settings = ai_game.settings
  
  #load the djinn image and set its rect attribute.
  self.image = pygame.image.load('images/arcanes.png')
  self.rect = self.image.get_rect()
  
  #start each new djinn near the top left of the screen.
  self.rect.x = self.rect.width
  self.rect.y = self.rect.height
  mark = self.rect
  #store the djinn exact horizontal position.
  self.x = float(self.rect.x) 
  
 def update(self):
  #move the djinn to the right.
  self.x += (self.settings.djinn_speed*self.settings.flock_direction)
  #walk = mixer.Sound('sounds/rock-golem-walking.wav')
  #walk.play()
  self.rect.x = self.x
  
 def check_edges(self):
  """return true if djinn is at edge of screen."""
  screen_rect = self.screen.get_rect()
  if self.rect.right >= screen_rect.right or self.rect.left<= 0:
   return True