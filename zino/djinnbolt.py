import pygame
from pygame.sprite import Sprite



class DjinnBolt(Sprite):
 """a class to manage bolts fired from the ship"""
 
 def __init__(self,ai_game,x,y):
  """create a bolts object at the djinn"s current position"""
  super().__init__()
  self.screen = ai_game.screen
  self.settings = ai_game.settings
  self.color = self.settings.bullet_color
  

  self.image = pygame.image.load(f'images/djinn_bolt.png')  
  self.rect = self.image.get_rect()
  self.rect.x = x
  self.rect.y = y
  
  #store the bolts"s position as a decimal value.
  self.y = float(self.rect.y)
  
 
  
  
 def update(self):
  """move the bullet up the screen"""
  #update the decimal position of the bolts
  self.y += self.settings.djinn_bolt_speed
  #update the rect position
  self.rect.y = self.y
  
 def blitme(self):
  """draw the bolts at its current location."""
  self.screen.blit(self.image,self.rect)
  
  