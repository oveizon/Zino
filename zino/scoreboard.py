import pygame.font
from pygame.sprite import Group
from soldier import Soldier

class Scoreboard:
 """a class to report scoring info"""
 def __init__(self,ai_game):
  """initialize score keeeping attributes"""
  self.ai_game = ai_game
  self.screen = ai_game.screen
  self.screen_rect = self.screen.get_rect()
  self.settings = ai_game.settings
  self.stats = ai_game.stats
 
  #font settings for scoring information.
  self.text_color = (30,30,30)
  self.font = pygame.font.SysFont(None, 48)
  self._prep_all_images()
 
 def _prep_all_images(self):
  #prepare the initial score images.
  self.prep_score()
  self.prep_high_score()
  self.prep_level()
  self.prep_soldiers()
  
 def prep_score(self):
  """turn the score into a rendered image"""
  rounded_score = round(self.stats.score, -1)
  score_str = '{:,}'.format(rounded_score)
  self.score_image = self.font.render(score_str, True,
   self.text_color, self.settings.bg_color)
   
  #display the score at the top right of the screen.
  self.score_rect = self.score_image.get_rect()
  self.score_rect.right = self.screen_rect.right -20
  self.score_rect.top = 20
  
 def prep_high_score(self):
  """turn the high score into a rendered image"""
  high_score = round(self.stats.high_score,-1)
  high_score_str = '{:,}'.format(high_score)
  self.high_score_image = self.font.render(high_score_str,
   True, self.text_color,self.settings.bg_color)
   
  #center the high score at the top of the screen.
  self.high_score_rect = self.high_score_image.get_rect()
  self.high_score_rect.centerx = self.screen_rect.centerx
  self.high_score_rect.top = self.score_rect.top
  
 def prep_level(self):
  """turn the level into rendered image"""
  level_str = str(self.stats.level)
  self.level_image = self.font.render(level_str,
   True, self.text_color, self.settings.bg_color)
   
  #position the level below the score.
  self.level_rect = self.level_image.get_rect()
  self.level_rect.right = self.score_rect.right
  self.level_rect.top = self.score_rect.bottom + 10
  
 def prep_soldiers(self):
  """show soldiers left"""
  self.soldiers = Group()
  for soldier_number in range(self.stats.soldiers_left):
   soldier = Soldier(self.ai_game)
   soldier.rect.x = 10 + soldier_number * soldier.rect.width
   soldier.rect.y = 10
   self.soldiers.add(soldier)
  
 
 def check_high_score(self):
  """check to see if there is a new high score"""
  if self.stats.score > self.stats.high_score:
   self.stats.high_score = self.stats.score
   self.prep_high_score()
   
 