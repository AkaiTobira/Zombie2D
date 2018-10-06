import pygame

from random   import randint
from events   import *
from obstacle import *
from player   import *
from enemy    import *
from colors   import *

def generate_random_color():
	return ( generate_int(0,255),generate_int(0,255),generate_int(0,255) )
	
def generate_random_position(left_up, right_down):
	return [ generate_int(left_up[0],right_down[0]), generate_int(left_up[1],right_down[1]) ] 

def generate_random_size(v_min, v_max):
	return generate_int(v_min, v_max)
	
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
				get_color(Colors.LIGHT_BLUE),
				6,
				6, # dla pelnego zamalowania 6
				self.screen,
				Vector(1024,720)
				)
				)
	
	def get_spawned_player(self, position):
	#	return Player((255,21,82), [512,360], 12, 12, self.screen)
		return Player(get_color(Colors.LIGHT_RED), 512, 360, 10, 3, self.screen)
		
	def generate_obstacles(self):	
		for i in range(self.number_of_obstacles):
			size = generate_random_size(15, 30)
			self.object_list.append(Obstacle(
				get_color(Colors.LIGHT_PURPLE),
				generate_random_position( [0,0], [1024,720] ),
				size,
				2, # pełne zamalowanie: size
				self.screen)
				)
		
	def create_objects(self):
		
		self.generate_obstacles()
		self.generate_enemy()
		
		rise_event(Events.CREATE, { "name" : "Create_Event" } )
		
		return self.object_list
		

