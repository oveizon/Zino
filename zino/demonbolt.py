import pygame
from pygame.sprite import Sprite



class DemonBolt(Sprite):
 """a class to manage bolts fired from the demon"""
 
 def __init__(self,ai_game,x,y):
  """create a bolts object at the demon"s current position"""
  super().__init__()
  self.screen = ai_game.screen
  self.settings = ai_game.settings
  self.color = self.settings.bullet_color
  
  #create a bolts rect at (0,0) and then set correct position.
  self.image = pygame.image.load(f'images/demon_bolt.png')  
  self.rect = self.image.get_rect() 
  
  self.rect.x = x
  self.rect.y = y
  #store the bolt"s position as a decimal value.
  self.y = float(self.rect.y)
  
 
  
  
 def update(self):
  """move the bolts up the screen"""
  #update the decimal position of the bolts
  self.y += self.settings.demon_bolt_speed
  #update the rect position
  self.rect.y = self.y
  
 def blitme(self):
  """draw the bolts at its current location."""
  self.screen.blit(self.image,self.rect)
  
  
  
  