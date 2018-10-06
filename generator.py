import pygame



from events import *
from obstacle import *

class ObjectsGenerator:
	screen 				= None
	number_of_enemy     = 0
	number_of_obstacles = 0
	
	def __init__(self, screen, enemy_counter, obstacle_counter):
		self.screen 		 	 = screen
		self.number_of_enemy 	 = enemy_counter
		self.number_of_obstacles = obstacle_counter
		
	def generate_enemy(self):
		pass
	
	def get_spawned_player(self, position):
		return Player((255,255,255),[512,360],10,self.screen)
		
	def generate_obstacles(self):
		pass
		
	def create_objects(self):
		
		rise_event(Events.CREATE, { "name" : "Create_EVent" } )
		
		return []
		
		