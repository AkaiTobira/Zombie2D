import pygame

from vector import Vector
from random import *
from events import *

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
	
		if event.type == Events.COLLIDE:
			for unit in self.entity_list:
				if unit.id == event.who:
					unit.process_event(event)
					return
					
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
		
		for unit in self.entity_list:
			if unit.state == "Move":
				for unit_2 in self.entity_list:
					if unit == unit_2 : 
						continue
					distance = ( unit.current_position + unit.velocity ).distance_to(unit_2.current_position + unit_2.velocity)
					if distance.len() > 60.0:
						continue
					offset = 1
					if distance.len() <= math.fabs( unit.RADIUS + unit_2.RADIUS + offset ) :
						if distance.len() <= math.fabs(unit_2.RADIUS - unit.RADIUS + offset):
							rise_event( Events.COLLIDE,  { "who" : unit.id, "stuck" : True,"with" : unit_2.id, "where" : unit.current_position - unit.velocity } )
						else:
							rise_event(Events.COLLIDE, { "who" : unit.id, "stuck" : False, "with" : unit_2.id, "where" : unit.current_position - unit.velocity  } )
							if unit_2.state == "Move":
								rise_event(Events.COLLIDE, { "who" : unit_2.id, "stuck" : False, "with" : unit.id, "where" : unit_2.current_position - unit_2.velocity  } )
							pass