#import sys
#import time
#import pygame

#from random import randint
from zino import Zino


class Moon:
 """overall class to manage game assets and behaviour"""
 
 def __init__(self):
  
  self.inva = Zino()
  self.control_game()
  
 def control_game(self):
  #start the main loop for the game"""
  while True:
   self.inva.run_game()
   
