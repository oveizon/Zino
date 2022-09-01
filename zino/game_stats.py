class Gamestats():
 """track statistics for zino"""

 def __init__(self, ai_game):
  self.settings = ai_game.settings
   
  self.reset_stats()
  #start zino in an active state.
  self.game_active = True
  #high score should never be reset_stats
  self.high_score = 0
  self.game_interlude = True
  self.hope = True
  self.binge = True
  

 
 def reset_stats(self):
  """initialize statistics that can change during the game."""
  self.soldiers_left = self.settings.soldier_limit
  self.score = 0
  self.level = 1
  
 