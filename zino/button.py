import pygame.font
import pygame


class Button:
 def __init__(self, ai_game, msg):
  """initialize button attributes"""
  self.screen = ai_game.screen
  self.screen_rect = self.screen.get_rect()
  self.clock = pygame.time.Clock()
  self.fps = 60
  self.scroll = 0
  self.newback = pygame.image.load('images/face.png')
  self.back = pygame.image.load('images/abstract.jpg')
  self.more = pygame.image.load('images/test23.png')
  self.end = pygame.image.load('images/ending.png')
  self.way = pygame.image.load('images/zinomain.png')
  self.story = pygame.image.load('images/Floral.jpg')
  
  
  #set the deimensions and properties of the button.
  self.width, self.height = 200, 50
  self.button_color = (25,25,25)
  self.text_color = (255, 255, 255)
  self.font = pygame.font.SysFont(None,48)
  
  #build the button's rect object and center it.
  self.rect = pygame.Rect(0,0,self.width,self.height)
  self.rect.center = self.screen_rect.center
  
  self._prep_msg(msg)
  
  self.rect_two = pygame.Rect(0,0,self.width,self.height)
  self.rect_two.center = (1100,600)
  
  #the button message needs to be prepped only once.
  if msg == 'start':
   self._msg(msg)
  
 def _prep_msg(self,msg):
  """turn msg into a rendered image and center text on the button"""
  self.msg_image = self.font.render(msg, True, self.text_color,
   self.button_color)
  self.msg_image_rect = self.msg_image.get_rect()
  self.msg_image_rect.center = self.rect.center
  
 def _msg(self,msg):
  """turn msg into a rendered image and center text on the button"""
  self.msg_image = self.font.render(msg, True, self.text_color,
   self.button_color)
  self.msg_image_rect = self.msg_image.get_rect()
  self.msg_image_rect.center = self.rect_two.center
  
  
  
 def draw_button(self):
  #draw blank button and then draw message.
  self.screen.blit(self.newback,(0,0))
  self.screen.fill(self.button_color,self.rect)
  self.screen.blit(self.msg_image,self.msg_image_rect)
  
 def draw_button_for_next(self):
  self.screen.blit(self.back,(0,0))
  self.screen.fill(self.button_color,self.rect)
  self.screen.blit(self.msg_image,self.msg_image_rect)
  
 
 def draw_button_for_more(self):
   self.screen.blit(self.more,(0,0))
   self.screen.fill(self.button_color,self.rect)
   self.screen.blit(self.msg_image,self.msg_image_rect)
   
 def draw_button_for_end(self):
   self.screen.blit(self.end,(0,0))
   self.screen.fill(self.button_color,self.rect)
   self.screen.blit(self.msg_image,self.msg_image_rect)
   
 def seeing(self):
   #main background image
   #self.clock.tick(self.fps)
   #width = self.way.get_width()
   #for i in range(2):      
   #self.screen.blit(self.way,(i*width+self.scroll,0))
   #self.screen.blit(self.background,(i*width+self.scroll,0))
   #self.scroll -=5
   #if abs(self.scroll) > width:
   #self.scroll = 0
   self.screen.blit(self.way,(0,0))
   self.screen.fill(self.button_color,self.rect)
   self.screen.blit(self.msg_image,self.msg_image_rect)
   
 def stories(self):
 
   self.screen.blit(self.story,(0,0))
   self.screen.fill(self.button_color,self.rect_two)
   self.screen.blit(self.msg_image,self.msg_image_rect)
  
  