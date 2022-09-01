class Settings:
 '''a class to store all settings for zino.'''
 
 def __init__(smurf):
  '''initialize the game's static settings.'''
  #screen settings
  smurf.screen_width = 1366
  smurf.screen_height = 768
  smurf.bg_color = (230, 230, 230)
   
  #bullet settings
  
  smurf.bullet_width = 3
  smurf.bullet_height = 10 
  smurf.bullet_side_width = 10
  smurf.bullet_side_height = 3
  smurf.bullet_color = (80,80,80)
  smurf.bullet_allowed = 8
  
  #djinn settings
  
  smurf.flock_drop_speed = 20
  smurf.djinn_bolt_width = 10
  smurf.djinn_bolt_height = 30
  smurf.djinn_bolt_color = (0,0,0)
  smurf.djinn_bolt_allowed = 8
  smurf.djinn_bolt_speed = 6
  
  #demon settings
  smurf.demon_bolt_width = 40
  smurf.demon_bolt_height = 40
  smurf.demon_bolt_allowed = 8
  smurf.demon_bolt_speed = 6
  
  #monster settings
  smurf.horde_drop_speed = 20
  
  smurf.assembly_drop_speed = 20
  
  
  #soldier settings
  smurf.soldier_limit = 0
  
  
  #how quickly the game speeds update
  smurf.speedup_scale = 1.1
  
  #how quickly the djinn point values increases
  smurf.score_scale = 1.5
  smurf.initialize_dynamic_settings()
  
 def initialize_dynamic_settings(smurf):
  """initialize settings that change throughout the game."""
  smurf.soldier_speed = 4
  smurf.bullet_speed = 4.0
  smurf.djinn_speed = 2.0
  smurf.monster_speed = 2.0
  smurf.demon_speed = 1.5
  
  #scoring
  smurf.djinn_points = 50
  smurf.monster_points = 50
  smurf.demon_points = 50
  
  #flock_direction of 1 represents right; -1 represents left.
  smurf.flock_direction = 1
  
  smurf.assembly_direction = 1
  
 def increase_speed(smurf):
  """increase speed settings and character value points"""
  smurf.soldier_speed *= smurf.speedup_scale
  smurf.djinn_speed *= smurf.speedup_scale
  smurf.bullet_speed *= smurf.speedup_scale
  smurf.monster_speed *= smurf.speedup_scale
  smurf.demon_speed *= smurf.speedup_scale
  
  smurf.djinn_points = int(smurf.djinn_points * smurf.score_scale)
  smurf.monster_points = int(smurf.monster_points * smurf.score_scale)
  smurf.demon_points = int(smurf.demon_points * smurf.score_scale) 