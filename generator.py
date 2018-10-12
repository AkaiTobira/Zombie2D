import pygame

from random   import randint,random
from obstacle import Obstacle
from player   import Player
from enemy    import Enemy
from colors   import Colors, get_color
from vector   import Vector

class ObjectsGenerator:
	screen 				= None
	number_of_enemy     = 0
	number_of_obstacles = 0
	enemy_list          = [] 
	obstacle_list       = []
	id_counter          = 1
	resulution          = Vector(0,0)
	
	def __init__(self, screen, enemy_counter, obstacle_counter, resulution):
		self.resulution          = resulution
		self.screen 		 	 = screen
		self.number_of_enemy 	 = enemy_counter
		self.number_of_obstacles = obstacle_counter
		
	def generate_enemy(self):
		for i in range(self.number_of_enemy):
			self.enemy_list.append(Enemy( self.screen, self.resulution, self.id_counter) )
			self.id_counter += 1
	
	def get_spawned_player(self, position):
		return Player(position, self.screen, self.resulution)
		
	def generate_obstacles(self):	
		for i in range(self.number_of_obstacles):
			self.obstacle_list.append(Obstacle(self.screen,self.resulution,self.id_counter))
			self.id_counter += 1
		
	def create_objects(self):
		self.generate_obstacles()
		self.generate_enemy()
		return [ self.enemy_list, self.obstacle_list ]
		

