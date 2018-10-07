import pygame

from vector import Vector
from random import *

class UnitManager:
	entity_list = []
	
	player      = None
	screen      = None 
	mv_system   =  None
	cl_system   =  None
	
	def __init__(self, units, player, screen):
		self.entity_list      = units
		self.screen           = screen
		self.mv_system        = MoveSystem(units, player)
		self.cl_system        = CollisionSystem(units, player)
		self.player           = player
		
	def draw(self):
		self.screen.fill((20,30,47))
		for obj in self.entity_list:
			obj.draw()
		self.player.draw()
		pygame.display.flip()
		
	def process_input(self,event):
		for obj in self.entity_list:
			obj.process_event(event)
			self.player.process_event(event)
		pass
		
	def process_physic(self,delta):
		self.mv_system.update(delta)
		self.cl_system.update(delta)
	
	def add_unit(self,unit):
		entity_list.append(unit)
		
	
	
class MoveSystem:
	entity_list = []
	player      = None
	
	def __init__(self, units, player):
		self.entity_list = units
		self.player      = player

	def update(self, delta):
		for unit in self.entity_list:
			if unit.state == "Wait":
				destination = Vector( randint(0,1024), randint(0, 600) )
				velocity    = unit.current_position.distance_to(destination).norm()# * delta
				unit.move_by(velocity, destination)
			elif unit.state == "Move":
				unit.update(delta)
				


	
class CollisionSystem:
	entity_list = []
	player      = None
	
	def __init__(self, units, player):
		self.entity_list = units
		self.player      = player
	
	def update(self, delta):
		for obj in self.entity_list:
			obj.update(delta)
			self.player.update(delta)