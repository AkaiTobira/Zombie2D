import pygame

from vector import Vector
from random import *
from events import *

class UnitManager:
	entity_list = []
	

	zombie_counter = 0
	player         = None
	screen         = None 
	mv_system      = None
	cl_system      = None
	
	def __init__(self, units, player, screen,screen_size):
		self.entity_list      = units
		for unit in units:
			if unit.state != "Const": self.zombie_counter += 1
		self.screen           = screen
		self.mv_system        = MoveSystem(units, player)
		self.cl_system        = CollisionSystem(units, player,screen_size)
		self.player           = player
		
	def draw(self):
		self.screen.fill((20,30,47))
		for obj in self.entity_list:
			obj.draw()
		self.player.draw()
		pygame.display.flip()
		
	def process_input(self,event):
	
		if event.type == Events.COLLIDE:
			if event.who == 0:
				self.player.process_event(event)
				return 
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
		self.zombie_counter += 1
		entity_list.append(unit)

	def has_more_zombie(self):
		return self.zombie_counter != 0

	def remove_unit(self,unit):
		self.zombie_counter -= 1
#		entity_list.remove
		pass		
	
	
class MoveSystem:
	entity_list = []
	player      = None
	
	def __init__(self, units, player):
		self.entity_list = units
		self.player      = player

	def __line_intersect(self, position):
		for unit in self.entity_list:
			if unit.state == "Const":
				if position.distance_to(unit.current_position).len() < unit.RADIUS:
					return unit
		return None


	def __run_before_player_destination(self ):
		destination = Vector( randint(0,1024), randint(0, 720) )

		while destination.distance_to(self.player.current_position).len() < 300:
			destination = Vector( randint(0,1024), randint(0, 720) )

		return destination
	
	def update(self, delta):
		for unit in self.entity_list:
			if unit.state == "Wait":
				destination = self.__run_before_player_destination()
				unit.move_to(destination)
			elif unit.state == "Move":
				
				unit_far   = self.__line_intersect( unit.seing_ahead )   
				unit_short = self.__line_intersect( unit.seing_ahead_short )
			
				force = Vector(0.0,0.0)
			
				if unit_far == None:
					if unit_short == None:
						pass
					else:
						force = (unit.seing_ahead - unit_short.current_position).norm() * 10						
				else:
					force = (unit.seing_ahead - unit_far.current_position).norm() * 10

				unit.apply_force(force)
				unit.update(delta)
				
		self.player.update(delta)
					
class CollisionSystem:
	entity_list = []
	player      = None
	ZERO_VECTOR = Vector(0,0)
	screen_size = Vector(0,0)
	OFFSET      = 1
	
	def __init__(self, units, player, screen_size):
		self.entity_list = units
		self.player      = player
		self.screen_size = Vector( screen_size[0], screen_size[1] ) 
	
	def __is_colliding(self, unit, unit_2, distance):
		if unit == unit_2: return False
		if distance > 60.0: return False
		if distance <= math.fabs( unit.RADIUS + unit_2.RADIUS + self.OFFSET ) : return True

	def __is_stuck(self, unit, unit_2, distance):
		if distance <= math.fabs(unit_2.RADIUS - unit.RADIUS + self.OFFSET): return True
		return False

	def __detect_collision_with_unit(self, unit):
		for unit_2 in self.entity_list:
			distance = ( unit.current_position + unit.velocity ).distance_to(unit_2.current_position + unit_2.velocity).len()
			if self.__is_colliding(unit,unit_2,distance):
				self.__send_collision_message(unit, unit_2, self.__is_stuck(unit,unit_2,distance))
				if not unit_2.velocity.is_zero_len():
					self.__send_collision_message( unit_2, unit, self.__is_stuck(unit_2,unit,distance))

	def __send_collision_message(self, unit, unit_2, is_stuck):
		rise_event(Events.COLLIDE, { "who" : unit.id, "stuck" : is_stuck, "with" : unit_2.id, "where" : unit.current_position - unit.velocity  } )

	def __detect_collision_with_wall(self, unit):
		if (unit.current_position + unit.velocity).is_behind( self.ZERO_VECTOR ) or not (unit.current_position + unit.velocity).is_behind( self.screen_size ):
			rise_event(Events.COLLIDE, { "who" : unit.id, "stuck" : False, "with" : -1, "where" : unit.current_position - unit.velocity  } )

	def __detect_collision_for_player(self):
		self.__detect_collision_with_unit(self.player)
		self.__detect_collision_with_wall(self.player)

	def __detect_collision_for_enemies(self):
		for unit in self.entity_list:
			if not unit.velocity.is_zero_len():
				self.__detect_collision_with_unit(unit)
				self.__detect_collision_with_wall(unit)

	def update(self, delta):
		self.__detect_collision_for_player()
		self.__detect_collision_for_enemies()
