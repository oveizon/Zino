import pygame
from pygame.sprite import Sprite
from settings import Settings

class Soldier(Sprite):
 """a class to manage soldier."""
 def __init__(self,ai_game,name):
  """initialize the soldier and set its starting position."""
  super().__init__()
  self.screen = ai_game.screen
  self.screen_rect = ai_game.screen.get_rect()
  self.settings = Settings()
  
  #load the soldier image nd get its rect
  self.image = pygame.image.load(f'images/{name}.png')
  self.rect = self.image.get_rect()
  
  #start each new soldier at d bottom center of d screen.
  if name == 'helpzino2':
   self.rect.midleft = self.screen_rect.midleft
  else:
   self.rect.midbottom = self.screen_rect.midbottom
  
  
  self.x = float(self.rect.x)
  #movement flag
  self.moving_right = False
  self.moving_left = False
 
  self.y = float(self.rect.y)
  self.moving_up = False
  self.moving_down = False
  
   
  
 def update(self):
  """update the soldier's position based on d move flag"""
  if self.moving_right and self.rect.right < self.screen_rect.right:
   self.x += self.settings.soldier_speed
  if self.moving_left and self.rect.left > 0:
   self.x -= self.settings.soldier_speed
  if self.moving_up and self.rect.top > 0:
   self.y -= self.settings.soldier_speed
  if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
   self.y += self.settings.soldier_speed
  #update rect obj from x
  self.rect.y = self.y
  #update rect obj from x
  self.rect.x = self.x
   
 def blitme(self):
  """draw the soldier at its current location."""
  self.screen.blit(self.image,self.rect)
  
 def center_soldier(self):
  """center the soldier on the screen"""
  self.rect.midbottom = self.screen_rect.midbottom
  self.x = float(self.rect.x)
  
 def main_soldier(self):
  """center the soldier on the screen"""
  self.rect.left = self.screen_rect.left
  self.y = float(self.rect.y)
  self.x = float(self.rect.x)
 
  