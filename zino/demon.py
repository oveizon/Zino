import pygame
from pygame.sprite import Sprite

class Demon(Sprite):
 """ a class to rep a single demon in the assembly"""
 
 def __init__(self, ai_game):
  """initialize the demon and set its starting point"""
  super().__init__()
  self.screen = ai_game.screen
  self.settings = ai_game.settings
  self.time = pygame.time.get_ticks()
  self.animation = []
  self.frame_index = 0
  
  for i in range(1,16):
   #load the demon image and set its rect attribute.
   img = pygame.image.load(f'images/demon/demon{i}.png')
   self.animation.append(img)
  self.image = self.animation[self.frame_index]
  self.rect = self.image.get_rect()
  
  #start each new demon near the top left of the screen.
  self.rect.x = self.rect.width
  self.rect.y = self.rect.height
  
  #store the demon exact horizontal position.
  self.x = float(self.rect.x) 
  
 def update(self):
  animation_cooldown = 40
  self.image = self.animation[self.frame_index]
  if pygame.time.get_ticks()-self.time >= animation_cooldown:
   self.time = pygame.time.get_ticks()
   self.frame_index += 1
  if self.frame_index >=  len(self.animation):
   self.frame_index = 0
  self.x += (self.settings.demon_speed*self.settings.assembly_direction)
  self.rect.x = self.x
  
 def check_edges(self):
  """return true if demon is at edge of screen."""
  screen_rect = self.screen.get_rect()
  if self.rect.right >= screen_rect.right or self.rect.left<= 0:
   return True