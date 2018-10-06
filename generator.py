import pygame


from random import *
from events import *
from obstacle import *
from player import *
from enemy import *

def generate_random_color():
	return ( generate_int(0,255),generate_int(0,255),generate_int(0,255) )
	
def generate_random_position(left_up, right_down):
	return [ generate_int(left_up[0],right_down[0]), generate_int(left_up[1],right_down[1]) ] 
	
def generate_int(lower, upper):
	return int(random()*upper) + lower 


class ObjectsGenerator:
	screen 				= None
	number_of_enemy     = 0
	number_of_obstacles = 0
	object_list         = []
	
	
	
	def __init__(self, screen, enemy_counter, obstacle_counter):
		self.screen 		 	 = screen
		self.number_of_enemy 	 = enemy_counter
		self.number_of_obstacles = obstacle_counter
		
	def generate_enemy(self):
		for i in range(self.number_of_enemy):
			self.object_list.append(Enemy(
				(255,0,0),
				generate_random_position( [0,0], [1024,720] ),
				5,
				self.screen)
				)
	
	def get_spawned_player(self, position):
		return Player((255,255,255),[512,360],10,self.screen)
		
	def generate_obstacles(self):	
		for i in range(self.number_of_obstacles):

			self.object_list.append(Obstacle(
				(0,123,123),
				generate_random_position( [0,0], [1024,720] ),
				20,
				self.screen)
				)
		
	def create_objects(self):
		
		self.generate_obstacles()
		self.generate_enemy()
		
		rise_event(Events.CREATE, { "name" : "Create_EVent" } )
		
		return self.object_list
		

