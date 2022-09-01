import sys
import time
import pygame

from pygame import mixer
#from random import randint
from settings import Settings
from game_stats import Gamestats
from scoreboard import Scoreboard
from button import Button
from soldier import Soldier
#from monster import monster
from monster import Monster
from bullet_two import Bullet
#from monsterbolt import monsterBolt
from new_loop import MonsterInvasion
#from main import Moon

class Zino:
 """overall class to manage game assets and behaviour"""
 
 def __init__(self):
  """initialize the game,& create game resources."""
  pygame.init()
  self.settings = Settings()
  
  self.screen = pygame.display.set_mode((1366,768))
  self.background = pygame.image.load('images/grassland.png')
  #self.back = pygame.image.load('images/Floral.jpg')
  
  
  #self.settings.screen_width = self.screen.get_rect().width
  #self.settings.screen_height = self.screen.get_rect().height
  pygame.display.set_caption("Zino")
  
  self.stats = Gamestats(self)
  self.sb = Scoreboard(self)
  #self.flag = False
  self.soldier = Soldier(self,'helpzino2')
  self.bullets = pygame.sprite.Group()
  self.monsterbolts = pygame.sprite.Group()
  self.monsters = pygame.sprite.Group()
  self.monsters = pygame.sprite.Group()
  self.start_time = time.time()
  self.new = MonsterInvasion()
  bazz = True
  self.bazz = bazz
  self.clock = pygame.time.Clock()
  self.fps = 60
  self.scroll = 0
  
    
  self._create_horde()   
  
  
  #make the buttons.
  self.play_button = Button(self,'you died')  
  self.inter =  Button(self,'Continue>>')
  self.see =  Button(self,'Begin')
  self.mark =  Button(self,'start')
  
  #music
  
  
  
 def run_game(self):
  """start the main loop for the game"""
  mixer.music.load('sounds/battle-march.wav')
  mixer.music.play()
  self.stats.hope = False
  self.stats.binge = False
  pygame.mouse.set_visible(True)
  #time.sleep(5.0)
  while True:
   self._check_events()
 
   if self.stats.game_active or self.stats.game_interlude:
    if self.stats.hope:
     if self.stats.binge:
      self.soldier.update()
      self._update_bullet()
      self._update_monsters() 
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
     self.starting(mouse_pos)
     self.wow(mouse_pos)
     self._check_interlude_button(mouse_pos)
     self._check_play_button(mouse_pos)
     
     
 def starting(self,mouse_pos):
   
   button_clicked = self.see.rect.collidepoint(mouse_pos)
   if button_clicked and not self.stats.hope:
    self.stats.hope = True
    mixer.music.load('sounds/horror-ambience.wav')
    mixer.music.play()
    #self._check_play_button(mouse_pos)
    #self.stats.binge = False
    
 def wow(self,mouse_pos):
   button_clicked = self.mark.rect_two.collidepoint(mouse_pos)
   if button_clicked and not self.stats.binge:
     self.stats.binge = True
     mixer.music.load('sounds/spirit-in-the-woods.wav')
     mixer.music.play()
     #mixer.music.stop()
     self._check_play_button(mouse_pos)
     
 def _check_play_button(self,mouse_pos):
  """start a new game when the player clicks play"""
  
  button_clicked = self.play_button.rect.collidepoint(mouse_pos)
  
  if button_clicked and not self.stats.game_active: 
     #reset the game settings
     self.settings.initialize_dynamic_settings()
     #horde = mixer.Sound('sounds/Large-Zombie-Horde.wav')
     #horde.play()
     #reset the game statistics
     self.stats.reset_stats()
     self.stats.game_active = True
     self.sb.prep_score()
     self.sb.prep_level()
     self.sb.prep_soldiers()
   
     #get rid of them
     self.monsters.empty() 
     self.bullets.empty()
     #create new fleet
     self._create_horde()
     self.soldier.main_soldier()
     #hide mouse
     pygame.mouse.set_visible(False)
     
 def _check_interlude_button(self,mouse_pos):
   button_clicked = self.inter.rect.collidepoint(mouse_pos)
   #mixer.music.stop()
   if button_clicked and not self.stats.game_interlude:
    self.new.make_game()
    
    
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
      gun = mixer.Sound('sounds/mgun_burst3.wav')
      gun.play()
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
  """create a new bullet and add it to the bullets group."""
  if len(self.bullets) < self.settings.bullet_allowed:
   new_bullet = Bullet(self)
   self.bullets.add(new_bullet)
     

 def _update_bullet(self):
  #updates bullet positions
  self.bullets.update()
  #get rid of disappeared bullets.
  for bullet in self.bullets.copy():
    size=self.screen.get_rect()
    if bullet.rect.right >= size.right:
     self.bullets.remove(bullet)
  self._check_bullet_monster_collisions()
   
  
 def _check_bullet_monster_collisions(self):  
  #check any bullets that have hit monsters
  #if so, get rid of the bullets and monster
  
  coollisions = pygame.sprite.groupcollide(
      self.bullets,self.monsters,True,True)      
  if coollisions:
     death = mixer.Sound('sounds/enemy-death-voice.wav')
     death.play()
     for monsters in coollisions.values():    
      self.stats.score += self.settings.monster_points*len(monsters)
  self.sb.prep_score()
  self.sb.check_high_score()
  self._all_monsters_killed()
   
 def _all_monsters_killed(self): 
  
   if not self.monsters:
    
    #destroy existing bullets and create new monsters.
    self.bullets.empty()
    self.settings.increase_speed()   
    #increase level.
    self.stats.level += 1
    self.sb.prep_level()
    if self.stats.level == 2: 
     self.monsters.empty()
     #if pygame.time.get_ticks() - s < well:
     self.stats.game_interlude = False
     mixer.music.load('sounds/The_Lord_Of_The_Rings_2_The_Hornburg.mp3')
     mixer.music.play()
     pygame.mouse.set_visible(True)
    else:
     self._create_horde()
     
    
   
 def _create_horde(self):
  """create the fleet of monsters"""
  #make an monster.
  monster = Monster(self)
  monster_width, monster_height = monster.rect.size
  available_space_y = (self.settings.screen_height)
  #(2*monster_height) - soldier_height)
  number_row =2

  #create the full horde of monster.
  for row_number in range(6):
   for monster_number in range(number_row):
    self._create_monster(monster_number,row_number)
  
 def _create_monster(self, monster_number,row_number):
   #setting the coordinates (x,y) of each monster.  
   monster = Monster(self)
   screen = self.screen.get_rect()
   monster_width, monster_height = monster.rect.size
   monster.x = screen.width + monster_height*monster_number
   monster.rect.x = monster.x
   monster.rect.y = monster_height*row_number
   #create a monster and place it in a row.
   #for i in range(3):
   self.monsters.add(monster)

   
   
     
   
 def _update_monsters(self):
   """check if the horde is at an edge, then update the positions of all monsters in the horde."""
   #self._check_horde_edges()
   self.monsters.update()
   #look for monster-soldier collisions.
   if pygame.sprite.spritecollideany(self.soldier, self.monsters):
    self._guy_hit()
   self._check_monsters_bottom()
    
 def _guy_hit(self):
  """responds to the soldier being hit by an monster or monster."""
  if self.stats.soldiers_left > 0:
   #reduce soldiers_left, and update scoreboard.
   self.stats.soldiers_left -= 1
   self.sb.prep_soldiers()
   #remove remaining monsters, monsters and bullets.
   if self.monsters:
    self.monsters.empty()
    self.bullets.empty()   
    #create new horde and center soldier
    self._create_horde()
    self.soldier.main_soldier()
  
   #pause
   time.sleep(0.5)
  else:
   self.stats.game_active = False
   pygame.mouse.set_visible(True)
    
 def _check_monsters_bottom(self):
  """check if monsters have reched bottom"""
  screen_rect = self.screen.get_rect()
  for monster in self.monsters.sprites():
   if monster.rect.left < screen_rect.left:
    self._guy_hit()
    break
  
     
 
    
         
 def _update_screen(self):
   """redraw the screen during each pass tru the loop/
   updates images on the screen"""
   self.screen.fill(self.settings.bg_color)
   self.screen.blit(self.background,(0,0))
   self.soldier.blitme()
   for bullet in self.bullets.sprites():
    bullet.draw_bullet()
   self.monsters.draw(self.screen)
   
   #draw the score info
   #self.sb.show_score()
   
   #draw the play button if the game is inactive.
   if not self.stats.game_active:
    self.play_button.draw_button()
   if not self.stats.game_interlude:
    self.inter.draw_button_for_next()
   if not self.stats.binge:
    self.mark.stories()
   if not self.stats.hope:  
    self.see.seeing()   
   
 
   #make the most recently drawn screen available.
   pygame.display.flip()
   
if __name__ == '__main__':
 #make a game instance, and run the game.
 zi=Zino()
 zi.run_game()