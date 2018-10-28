import pygame
import math

from vector import Vector
from random import randint
from events import Events, rise_event
from colors import Colors, get_color
from ai     import *

class UnitManager:
	obstacle_list = []
	enemy_list    = []
	

	zombie_counter = 0
	player         = None
	screen         = None 
	mv_system      = None
	cl_system      = None
	
	def __init__(self, units, player, screen,screen_size):
		self.enemy_list       = units[0]
		self.obstacle_list    = units[1]
		self.zombie_counter   = len(self.enemy_list)
		self.screen           = screen
		self.mv_system        = MoveSystem(units, player)
		self.cl_system        = CollisionSystem(units, player,screen_size)
		self.player           = player
		
	def draw(self):
		self.screen.fill(get_color(Colors.NAVYBLUE))
		for obj in ( self.enemy_list + self.obstacle_list ):
			obj.draw()
		self.player.draw()
		
	def process_input(self,event):
	
		if event.type == Events.COLLIDE:
			if event.who == 0:
				self.player.process_event(event)
				self.player.decrease_HP(1)
				return 
			for unit in self.enemy_list:
				if unit.id == event.who:
					unit.process_event(event)
					return
					
		for obj in self.enemy_list:
			obj.process_event(event)
			self.player.process_event(event)
		pass
		
	def process_physic(self,delta):
		self.mv_system.update(delta)
		self.cl_system.update(delta)

	def add_unit(self,unit):
		self.zombie_counter += 1
		self.enemy_list.append(unit)

	def has_more_zombie(self):
		return self.zombie_counter != 0

	def remove_unit(self,unit):
		self.zombie_counter -= 1
		pass		
	
class EnemySteeringBehaviours:
	maxSpeed         = Vector(2,2)
	mass             = 1
	current_position = Vector(0,0)
	velocity         = Vector(0,0)
	target_pos       = Vector(0,0)

	head             = Vector(0,0)
	side             = Vector(0,0)

	def __init__(self, current_position):
		self.current_position = current_position
		self.head             = Vector(0,1).norm()
		self.side             = self.head.perp()

	def __get_steering(self):
		return self.__seek()

	def calculate_behaviour(self):
		steering      = self.__get_steering()
		acceleration  = steering / self.mass
		self.velocity += acceleration * 0.018
		self.velocity = self.velocity.trunc(self.maxSpeed)

		self.head     = self.velocity.norm() 
		self.side     = self.head.perp()
		return self.velocity

	def set_target(self, target):
		self.target_pos    =  target 

	def __seek(self):
		return (self.target_pos - self.current_position).norm() * self.maxSpeed - self.velocity

	def __flee(self):
		return (self.current_position - self.target_pos ).norm() * self.maxSpeed - self.velocity

	def __arrive(self):
		pass

	def __wander(self):
		pass
	
	def __hide(self):
		pass

	def __group(self):
		pass

	def __kill(self):
		pass



class MoveSystem:
	obstacle_list = []
	enemy_list    = []
	player        = None
	
	def __init__(self, units, player):
		self.obstacle_list = units[1]
		self.enemy_list    = units[0] 
		self.player        = player

	def __line_intersect(self, position):
		for unit in self.obstacle_list:
			if position.distance_to(unit.current_position).len() < unit.RADIUS:
				return unit
		return None
	
	def update(self, delta):
		for enemy in self.enemy_list:
			enemy.ai.update(delta, self.player)
			enemy.update(delta)

		self.player.update(delta)
					
class CollisionSystem:
	enemy_list    = []
	obstacle_list = []
	player      = None
	ZERO_VECTOR = Vector(0,0)
	screen_size = Vector(0,0)
	OFFSET      = 1
	
	def __init__(self, units, player, screen_size):
		self.enemy_list =  units[0] 
		self.obstacle_list = units[1] 
		self.player      = player
		self.screen_size = Vector( screen_size[0], screen_size[1] ) 
	
	def __is_colliding(self, unit, unit_2, distance):
		if unit == unit_2: return False
		if distance > 60.0: return False
		if distance <= math.fabs( unit.RADIUS + unit_2.RADIUS + self.OFFSET ) : return True

	def __is_stuck(self, unit, unit_2, distance):
		if distance <= math.fabs(unit_2.RADIUS - unit.RADIUS + self.OFFSET): return True
		return False

	def __detect_collision_with_obstacle(self, unit,delta):
		for unit_2 in self.obstacle_list:
			distance = ( unit.current_position + unit.velocity*delta ).distance_to(unit_2.current_position + unit_2.velocity*delta).len()
			if self.__is_colliding(unit,unit_2,distance):
				self.__send_collision_message(unit, unit_2, self.__is_stuck(unit,unit_2,distance),delta)

	def __detect_collision_with_unit(self, unit,delta):
		for unit_2 in self.enemy_list:
			distance = ( unit.current_position + unit.velocity*delta ).distance_to(unit_2.current_position + unit_2.velocity*delta).len()
			if self.__is_colliding(unit,unit_2,distance):
				self.__send_collision_message(unit, unit_2, self.__is_stuck(unit,unit_2,distance),delta)
				if not unit_2.velocity.is_zero_len():
					self.__send_collision_message( unit_2, unit, self.__is_stuck(unit_2,unit,distance),delta)

	def __send_collision_message(self, unit, unit_2, is_stuck,delta):
		rise_event(Events.COLLIDE, { "who" : unit.id, "stuck" : is_stuck, "with" : unit_2.id, "where" : unit.current_position - unit.velocity*delta  } )

	def __detect_collision_with_wall(self, unit,delta):
		if (unit.current_position + unit.velocity*delta).is_behind( self.ZERO_VECTOR ) or not (unit.current_position + unit.velocity*delta).is_behind( self.screen_size ):
			rise_event(Events.COLLIDE, { "who" : unit.id, "stuck" : False, "with" : -1, "where" : unit.current_position - unit.velocity*delta  } )

	def __detect_collision_for_player(self,delta):
		self.__detect_collision_with_obstacle(self.player,delta)
		self.__detect_collision_with_unit(self.player,delta)
		self.__detect_collision_with_wall(self.player,delta)

	def __detect_collision_for_enemies(self,delta):
		for unit in self.enemy_list:
			if not unit.velocity.is_zero_len():
				self.__detect_collision_with_unit(unit,delta)
				self.__detect_collision_with_obstacle(unit,delta)
	#			self.__detect_collision_with_wall(unit)

	def update(self, delta):
		self.__detect_collision_for_player(delta)
	#	self.__detect_collision_for_enemies(delta)
