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
from demon import Demon
from bullet import Bullet
from demonbolt import DemonBolt
from random import choice



class DemonInvasion:
 """overall class to manage game assets and behaviour"""
 
 def __init__(self):
  """initialize the game,& create game resources."""
  pygame.init()
  
  self.settings = Settings()

  
  self.screen = pygame.display.set_mode((1366,768))
  self.background = pygame.image.load('images/landscape_three.png')
  
  
  pygame.display.set_caption("Zino")
  
  #create an instance to store game statistics.
  #and create a scoreboard.
  
  self.stats = Gamestats(self)
 
  self.sb = Scoreboard(self)
  
  self.soldier = Soldier(self,'zino2')
  self.bullets = pygame.sprite.Group()
  self.demonbolts = pygame.sprite.Group()
  self.demons = pygame.sprite.Group()
  self.bullet_cooldown = 3000
  self.begin_time = pygame.time.get_ticks()
  self.start_time = time.time()
  
  
    
  
  self._create_assembly()
  
  #make the play button.
  self.play_button = Button(self,'you died')
  self.inter = Button(self,'Victory!')
  self.blast = 0

  
 def drill_game(self):
  mixer.music.load('sounds/horror-ambience.wav')
  mixer.music.play()
  """start the main loop for the game"""
  while True:
   self._check_events()
   
   if self.stats.game_active or self.stats.game_interlude:
    self.soldier.update()
    self._update_bullet()
    self._update_demons()  
    self.demons_fire()
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
  """start a new game when the player clicks play"""
  button_clicked = self.play_button.rect.collidepoint(mouse_pos)
  if button_clicked and not self.stats.game_active: 
   
   import main
   main.Moon()
   
  
   
 def _check_interlude_button(self,mouse_pos):
   button_clicked = self.inter.rect.collidepoint(mouse_pos)
   if button_clicked and not self.stats.game_interlude: 
    pygame.mouse.set_visible(False)
    self.stats.game_active = True
    self.stats.soldiers_left = 0
    self._soldier_hit()
    
 
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
      rifle = mixer.Sound('sounds/mgun_burst3.wav')
      rifle.play()
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
   
 def demons_fire(self):
  """demons fire"""
  time_now = pygame.time.get_ticks()
  #elapsed_time = time_now - self.start_time
  if time_now - self.begin_time > self.bullet_cooldown:
   violent = choice(self.demons.sprites())
   big_bullet = DemonBolt(self, violent.rect.x, violent.rect.bottom)
   self.demonbolts.add(big_bullet) 
   self.begin_time = time_now
   self.blast = mixer.Sound('sounds/thunderrumble.wav')
   self.blast.play()
     

 def _update_bullet(self):
  #updates bullet positions
  self.bullets.update()
  #get rid of disappeared bullets.
  for bullet in self.bullets.copy():
    if bullet.rect.bottom <= 0:
     self.bullets.remove(bullet)
  self._check_bullet_demon_collisions()
  """demon bullets"""
  self.demonbolts.update()
  #get rid of disappeared bullets.
  for bullet in self.demonbolts.copy():
    if bullet.rect.bottom <= 0:
     self.demonbolts.remove(bullet)
  self._check_bullet_soldier_collisions()
  
 
 def _check_bullet_soldier_collisions(self):
   if pygame.sprite.spritecollideany(self.soldier, self.demonbolts):
    self._soldier_hit()
   
  
 def _check_bullet_demon_collisions(self):  
  #check any bullets that have hit demons
  #if so, get rid of the bullets and demon
  elapsed_time = int(time.time() - self.start_time)
  if elapsed_time % 4 == 0:
    collisions = pygame.sprite.groupcollide(
      self.bullets,self.demons,True,True)   
    if collisions:
     kill = mixer.Sound('sounds/giant-monster-roar.wav')
     kill.play()
     for demons in collisions.values():
      self.stats.score += self.settings.demon_points*len(demons)
    self.sb.prep_score()
    self.sb.check_high_score()
  self._all_demons_killed()
   
 def _all_demons_killed(self):  
  if not self.demons:
    #destroy existing bullets and create new demons.
    self.bullets.empty()
    self.demonbolts.empty() 
    self._create_assembly()
    self.settings.increase_speed()   
    #increase level.
    self.stats.level += 1
    self.sb.prep_level()
    self.blast.stop
    self.stats.game_interlude = False
    mixer.music.load('sounds/Pirates_Of_The_Caribbean_At_Worlds_End_Up_Is_Down.mp3')
    mixer.music.play()
    pygame.mouse.set_visible(True)

    
 def _create_assembly(self):
  #create the assembly of demons 
  demon = Demon(self)
  number_demons_x = 3
  number_row = 1 
  #create the full assembly of demons.
  for row_number in range(number_demons_x):
   for demon_number in range(number_row):
    self._create_demon(demon_number,row_number)
    
  
 def _create_demon(self,demon_number,row_number):
   #setting the coordinates (x,y) of each demon.  
   demon = Demon(self)

   x = [200,800,300,420,1000,550,200,1000,670,800]
   y = [1,1,230,350,320,300,250,270,100,200]
   ran = randint(0,9)
   for i in range(1):
    demon.x = x[ran]
   demon.rect.x = demon.x
   for m in range(1):
    demon.y = y[ran] #CHEECK THIS GUY!!
    demon.rect.y = demon.y
   #create an demon and place it in a row.
   self.demons.add(demon)

   
      
 def _update_demons(self):
   """check if the assembly is at an edge, then update the positions of all demons in the assembly."""
   self._check_assembly_edges()
   self.demons.update()
   #look for demon-soldier collisions.
   if pygame.sprite.spritecollideany(self.soldier, self.demons):
    self._soldier_hit()
   self._check_demons_bottom()
   
    
 def _soldier_hit(self):
  """responds to the soldier being hit by an demon or monster."""
  if self.stats.soldiers_left > 0:
   #reduce soldiers_left, and update scoreboard.
   self.stats.soldiers_left -= 1
   
  
  else:
   self.stats.game_active = False
   pygame.mouse.set_visible(True)
   
   
  
 def _check_demons_bottom(self):
  """check if demons have reched bottom"""
  screen_rect = self.screen.get_rect()
  for demon in self.demons.sprites():
   if demon.rect.bottom >= screen_rect.bottom:
    self._soldier_hit()
    break
  
 
 def _check_assembly_edges(self):
   """ respond appropriately if edges"""
   for demon in self.demons.sprites():
    if demon.check_edges():
     self._change_assembly_direction()
     break
     
  
 def _change_assembly_direction(self):
   """drop the assembly and change direction,"""
   for demon in self.demons.sprites():
    demon.rect.y +=self.settings.assembly_drop_speed
   self.settings.assembly_direction *= -1
    
         
 def _update_screen(self):
   """redraw the screen during each pass tru the loop/
   updates images on the screen"""
   self.screen.fill(self.settings.bg_color)
   self.screen.blit(self.background,(0,0))
   self.soldier.blitme()
   for bullet in self.bullets.sprites():
    bullet.draw_bullet()
   for demonbolt in self.demonbolts.sprites():
    demonbolt.blitme()
   self.demons.draw(self.screen) 
   
   #draw the score info
   #self.sb.show_score()
   
   #draw the play button if the game is inactive.
   if not self.stats.game_active:
    self.play_button.draw_button()
   if not self.stats.game_interlude:
    self.inter.draw_button_for_end()
 
   #make the most recently drawn screen available.
   pygame.display.flip()
   

      