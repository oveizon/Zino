import sys
import time
import pygame

from pygame import mixer
from random import randint
from settings import Settings
from game_stats import Gamestats
from scoreboard import Scoreboard
from button import Button
from soldier import Soldier
from djinn import Djinn
from bullet import Bullet
from djinnbolt import DjinnBolt
from big import DemonInvasion
from random import choice



class MonsterInvasion:
 """overall class to manage game assets and behaviour"""
 
 def __init__(self):
  """initialize the game & create game resources."""
  pygame.init()
  #self.tain = gain
  self.settings = Settings()
  
  self.screen = pygame.display.set_mode((1366,768))
  self.background = pygame.image.load('images/deserts.png')
  
  
  
  pygame.display.set_caption("Zino")
  
  #create an instance to store game statistics.
  #and create a scoreboard.
  
  self.stats = Gamestats(self)
  #self.mut = Moon(self)
  self.sb = Scoreboard(self)
  #self.jack = False
  self.soldier = Soldier(self,'helpzino')
  self.crush = DemonInvasion()
  self.bullets = pygame.sprite.Group()
  self.djinnbolts = pygame.sprite.Group()
  self.djinns = pygame.sprite.Group()
  self.clock = pygame.time.Clock()
  self.fps = 60
  self.bullet_cooldown = 3000
  self.begin_time = pygame.time.get_ticks()
  self.start_time = time.time()
  
  #self.old = djinnInvasion()
    
  
  self._create_flock()
  
  #make the play button.
  self.play_button = Button(self,'you died')
  self.inter = Button(self,'Continue>>')
  self.void = 0

  
 def make_game(self):
  """start the main loop for the game"""
  mixer.music.load('sounds/spirit-in-the-woods.wav')
  mixer.music.play(-1)
   
  while True:
    #self.clock.tick(self.fps)
    self._check_events()
   
    if self.stats.game_active or self.stats.game_interlude:
     self.soldier.update()
     self._update_bullet()
     self._update_djinns()  
     self.djinns_fire()
     self._update_screen()
      
   
 def _check_events(self):
   """watch for keyboard and mouse events."""
   
   for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
     self._check_keydown_events(event)
    if event.type == pygame.KEYUP:
     self._check_keyup_events(event)
    elif event.type == pygame.QUIT:
     sys.exit()
    elif event.type ==pygame.MOUSEBUTTONDOWN:
     mouse_pos = pygame.mouse.get_pos()
     self._check_play_button(mouse_pos)
     self._check_interlude_button(mouse_pos)
     
 def _check_play_button(self,mouse_pos):
  """start a new game when the player clicks anywhere around play"""
  button_clicked = self.play_button.rect.collidepoint(mouse_pos)
  if button_clicked and not self.stats.game_active: 
   
   import main
   main.Moon()
   
   
 def _check_interlude_button(self,mouse_pos):
   
   button_clicked = self.inter.rect.collidepoint(mouse_pos)
   mixer.music.stop()
   if button_clicked and not self.stats.game_interlude:
    self.crush.drill_game()
    
    
 def _check_keydown_events(self,event):
     #move the soldier right
     if event.key == pygame.K_RIGHT:
      self.soldier.moving_right = True
     #move the soldier left
     elif event.key == pygame.K_LEFT:
      self.soldier.moving_left = True
     #move the soldier up
     elif event.key == pygame.K_UP:
      self.soldier.moving_up = True
     #move the soldier down
     elif event.key == pygame.K_DOWN:
      self.soldier.moving_down = True      
     elif event.key == pygame.K_q:
      sys.exit()
     elif event.key == pygame.K_SPACE:
      bolt = mixer.Sound('sounds/mgun_burst3.wav')
      bolt.play()
      self._fire_bullet()
     
     
 def _check_keyup_events(self,event):   
     if event.key == pygame.K_RIGHT:
      self.soldier.moving_right = False
     elif event.key == pygame.K_LEFT:
      self.soldier.moving_left = False
     elif event.key == pygame.K_UP:
      self.soldier.moving_up = False
     elif event.key == pygame.K_DOWN:
      self.soldier.moving_down = False
      
 def _fire_bullet(self):
  """create a new and add it to the bullets group."""
  if len(self.bullets) < self.settings.bullet_allowed:
   new_bullet = Bullet(self)
   self.bullets.add(new_bullet)
   
   
 def djinns_fire(self):
  """djinns fire"""
  time_now = pygame.time.get_ticks()
  #elapsed_time = time_now - self.start_time
  if time_now - self.begin_time > self.bullet_cooldown:
   violent = choice(self.djinns.sprites())
   big_bullet = DjinnBolt(self, violent.rect.x, violent.rect.bottom)
   self.djinnbolts.add(big_bullet)   
   self.begin_time = time_now
   self.void = mixer.Sound('sounds/thunder2 (1).wav')
   self.void.play()
     

 def _update_bullet(self):
  #updates bullet positions
  self.bullets.update()
  #get rid of disappeared bullets.
  for bullet in self.bullets.copy():
    if bullet.rect.bottom <= 0:
     self.bullets.remove(bullet)
  self._check_bullet_djinn_collisions()
  """djinn bullets"""
  self.djinnbolts.update()
  #get rid of disappeared bullets.
  for bullet in self.djinnbolts.copy():
    if bullet.rect.bottom <= 0:
     self.djinnbolts.remove(bullet)
  self._check_bullet_soldier_collisions()
  
 
 def _check_bullet_soldier_collisions(self):
   if pygame.sprite.spritecollideany(self.soldier, self.djinnbolts):
    self._soldier_hit()
   
  
 def _check_bullet_djinn_collisions(self):  
  #check any bullets that have hit djinns
  #if so, get rid of the bullets and djinn
  elapsed_time = int(time.time() - self.start_time)
  if elapsed_time % 2 == 0:
    collisions = pygame.sprite.groupcollide(
      self.bullets,self.djinns,True,True)   
    if collisions:
     
     for djinns in collisions.values():
      death = mixer.Sound('sounds/monster-scream.wav')
      death.play()
      self.stats.score += self.settings.djinn_points*len(djinns)
    self.sb.prep_score()
    self.sb.check_high_score()
    self._all_djinns_killed()
   
 def _all_djinns_killed(self):  
  if not self.djinns:
    #destroy existing bullets and create new djinns.
    self.bullets.empty()
    self.djinnbolts.empty()
    
    self.settings.increase_speed()   
    #increase level.
    self.stats.level += 1
    self.sb.prep_level()
    if self.stats.level == 2:#and self.stats.soldiers_left > 0:
     self.void.stop
     self.stats.game_interlude = False
     mixer.music.load('sounds/The_Lord_Of_The_Rings_2_The_Hornburg.mp3')
     mixer.music.play()
     pygame.mouse.set_visible(True)
    else:
     self._create_flock()
     

    
 def _create_flock(self):
  #create the flock of djinns 
  djinn = Djinn(self)
  number_djinns_x = 10
  number_row = 1 
  #create the full flock of djinns.
  for row_number in range(number_djinns_x):
   for djinn_number in range(number_row):
    self._create_djinn(djinn_number,row_number)
    
  
 def _create_djinn(self,djinn_number,row_number):
   #setting the coordinates (x,y) of each djinn.  
   djinn = Djinn(self)
   x = [200,800,300,420,1000,550,200,1000,670,800]
   y = [1,1,200,350,320,300,400,450,100,400]
   ran = randint(0,9)
   for i in range(1):
    djinn.x = x[ran]
   djinn.rect.x = djinn.x
   for m in range(1):
    djinn.y = y[ran] #CHEECK THIS GUY!!
    djinn.rect.y = djinn.y
   #create an djinn and place it in a row.
   self.djinns.add(djinn)
   
   
      
 def _update_djinns(self):
   """check if the flock is at an edge, then update the positions of all djinns in the flock."""
   self._check_flock_edges()
   self.djinns.update()
   #look for djinn-soldier collisions.
   if pygame.sprite.spritecollideany(self.soldier, self.djinns):
    self._soldier_hit()
   self._check_djinns_bottom()
   
    
 def _soldier_hit(self):
  """responds to the soldier being hit by an djinn or monster."""
  if self.stats.soldiers_left > 0:
   #reduce soldiers_left, and update scoreboard.
   self.stats.soldiers_left -= 1
   self.sb.prep_soldiers()
   #self.mut.switch()
   #remove remaining djinns, monsters and bullets.
   if self.djinns:
    self.djinns.empty()
    self.bullets.empty()
    self.djinnbolts.empty()   
    #create new flock or horde and center soldier
    
    self._create_flock()
    self.soldier.center_soldier()
  
   #pause
   time.sleep(0.5)
  
  else:
   self.stats.game_active = False
   pygame.mouse.set_visible(True)
   
   
  
 def _check_djinns_bottom(self):
  """check if djinns have reched bottom"""
  screen_rect = self.screen.get_rect()
  for djinn in self.djinns.sprites():
   if djinn.rect.bottom >= screen_rect.bottom:
    self._soldier_hit()
    break
  
 
 def _check_flock_edges(self):
   """ respond appropriately if edges"""
   for djinn in self.djinns.sprites():
    if djinn.check_edges():
     self._change_flock_direction()
     break
     
  
 def _change_flock_direction(self):
   """drop the flock and change direction,"""
   for djinn in self.djinns.sprites():
    djinn.rect.y +=self.settings.flock_drop_speed
   self.settings.flock_direction *= -1
    
         
 def _update_screen(self):
   """redraw the screen during each pass tru the loop/
   updates images on the screen"""
   self.screen.fill(self.settings.bg_color)
   self.screen.blit(self.background,(0,0))
   self.soldier.blitme()
   for bullet in self.bullets.sprites():
    bullet.draw_bullet()
   for djinnbolt in self.djinnbolts.sprites():
    djinnbolt.blitme()
  
   self.djinns.draw(self.screen) 
   
   #draw the score info
   #self.sb.show_score()
   
   #draw the play button if the game is inactive.
   if not self.stats.game_active:
    self.play_button.draw_button()
   if not self.stats.game_interlude:
    self.inter.draw_button_for_more()
 
   #make the most recently drawn screen available.
   pygame.display.flip()
   

      