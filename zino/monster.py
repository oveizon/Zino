import pygame
from pygame.sprite import Sprite
from pygame.locals import*

class Monster(Sprite):
 """ a class to rep a single monster in the horde"""
 
 def __init__(self, ai_game):
  """initialize the monster and set its starting point"""
  super().__init__()
  self.screen = ai_game.screen
  self.settings = ai_game.settings
  
  #animation
  self.animation_list = []
  self.frame_index = 0
  self.update_time = pygame.time.get_ticks()
  for i in range(1,3):
   img = pygame.image.load(f'images/monster/ragdin{i}.png')
   self.animation_list.append(img)
  #load the monster image and set its rect attribute.
  self.image = self.animation_list[self.frame_index]
  self.rect = self.image.get_rect()
 
  
  #start each new monster near the top left of the screen.
  self.rect.x = self.rect.width
  self.rect.y = self.rect.height
  
  #store the monster exact horizontal position.
  self.x = float(self.rect.x) 
  
 def update(self):
  animation_cool = 270
  self.image = self.animation_list[self.frame_index]
  if pygame.time.get_ticks()-self.update_time >= animation_cool:
   self.update_time = pygame.time.get_ticks()
   self.frame_index += 1
  if self.frame_index >= len(self.animation_list):
   self.frame_index = 0
  #move the monster to the right.
  self.x -= (self.settings.monster_speed)
  self.rect.x = self.x
  
  
 
 