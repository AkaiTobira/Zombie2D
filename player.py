import pygame

from events import Events, rise_event
from vector import Vector
from random import randint
from colors import Colors, get_color

import math

class Triangle:
	vertices = []
	basic    = [] 
	
	def __init__(self, size):
		self.vertices = [Vector(0.0,-1.0)*size, Vector(-1.0,1.0)*size, Vector(1.0,1.0)*size]
		self.basic = self.vertices.copy()
		
	def rotate(self, angle):
		for i in range(len(self.vertices)):
			self.vertices[i] = self.basic[i].rotate(angle)
		
	def to_draw(self, position):
		return [ (position + self.vertices[0]).to_touple(),
				 (position + self.vertices[1]).to_touple(),
				 (position + self.vertices[2]).to_touple()]


class Orientation:

	scancode = []
	enable   = False
	velocity = Vector(0,0)

	def __init__(self, scancode, velocity):
		self.scancode = scancode
		self.velocity = velocity

	def get_velocity(self):
		return self.velocity

	def get_scancode_table(self):
		return self.scancode

	def get_enable(self):
		return self.enable			

	def enable_orientation(self):
		self.enable = True	

	def disable_orientation(self):
		self.enable = False		


class PlayerMoveBehavior:

	position	= Vector(0,0)
	velocity	= Vector(0,0)	
	screen		= None


	orientation = {
					"up"    : Orientation([72, 17], Vector(0.0, -1.0)),
					"down"  : Orientation([80, 31], Vector(0.0,  1.0)),
					"right" : Orientation([77, 32], Vector(1.0,  0.0)),
					"left"  : Orientation([75, 30], Vector(-1.0, 0.0)),
				  }

	def __init__(self, position):
		self.position = position

	def set_orientation(self, velocity, orientation):
		self.velocity = (self.velocity + velocity).norm()

	def scancode_to_orientation(self, scancode):
		for key in self.orientation.keys():
			if scancode in self.orientation[key].get_scancode_table():
				return str(key)
		return None
			
	def enable_key_pressed(self, orientation):
		if orientation == None: return
		self.orientation[orientation].enable_orientation()

	def disable_key_pressed(self, orientation):
		if orientation == None: return
		self.orientation[orientation].disable_orientation()

	def handle_orientation_key_press(self):
		for key in self.orientation.keys():
			if self.orientation[key].get_enable():
				self.set_orientation(self.orientation[key].get_velocity(), str(key))

	def process_event(self, event):
		if event.type == pygame.KEYDOWN:
			self.enable_key_pressed(self.scancode_to_orientation(event.scancode))
		elif event.type == pygame.KEYUP:
			self.disable_key_pressed(self.scancode_to_orientation(event.scancode))
			self.velocity = Vector(0,0)

	def get_velocity(self):
		return self.velocity

	def get_current_position(self):
		return self.position

	
class PlayerRotateBehavior:

	position 		  = Vector(0,0)
	face              = Vector(0,0)
	rotation_angle    = 0.0
	rotation_change   = False

	def __init__(self, position):
		self.position = position

	def update_position(self, position):
		self.position = position
		self.face 	  = Vector(position.x, position.y - 200)

	def process_event(self, event):
		self.rotation_angle = (self.face - self.position).norm().angle_between((Vector(event.pos[0], event.pos[1]) - self.position).norm()) 
		self.rotation_change = True

	def print_rotation_angle(self):
		print("rotate angle: [ " + str(round(self.rotation_angle * 180 / math.pi)) + " ] degrees")

	def get_rotation_angle(self):
		self.rotation_change = False
		return self.rotation_angle	

	def get_rotation_change(self):
		return self.rotation_change

	def set_rotation_change(self, change):
		self.rotation_change = change


class PlayerActions:

	screen			= None
	railgun_color	= get_color(Colors.YELLOW)
	railgun_thick	= 2
	sum_delta		= 0
	shoot			= False

	player_position = None
	mouse_position  = Vector(0,0)

	def __init__(self, screen, player):
		self.player_position = player
		self.screen = screen

	def draw_railgun(self):
		rise_event( Events.SHOOT, {} )
		pygame.draw.line(
			self.screen, 
			self.railgun_color, 
			self.player_position.to_table(), 
			(self.player_position + (1260 * (self.mouse_position - self.player_position).norm())).to_table(), 
			self.railgun_thick
			)					

	def process_event(self, event):
		self.shoot = True
		self.mouse_position = (Vector(event.pos[0], event.pos[1]))

	def draw(self):
		if(self.shoot):
			self.draw_railgun()

	def update(self, delta, position):
		self.player_position = position
		if(self.shoot):
			self.sum_delta += delta
			if(self.sum_delta > 0.1):
				self.shoot = False
				self.sum_delta = 0

class Player:

	id     			  = 0
	HP				  = 0	
	THICK  			  = 3
	RADIUS			  = 10
	COLOR  			  = get_color(Colors.LIGHT_RED)
	screen			  = None
	move_behavior	  = None
	rotate_behavior   = None
	actions_behavior  = None

	current_position  = Vector(0,0)
	previous_position = Vector(0,0)
	velocity          = Vector(0,0)
	mouse_point		  = Vector(0,0)
	screen_size       = Vector(0,0)
	graphic 		  = Triangle(0)

	speed             = Vector(20.0,20.0)

	def __init__(self, position, screen, hp):
		self.graphic            = Triangle( 10 )
		self.current_position  	= position
		self.previous_position 	= position
		self.screen				= screen
		self.move_behavior 		= PlayerMoveBehavior(position)
		self.rotate_behavior	= PlayerRotateBehavior(position)
		self.actions_behavior   = PlayerActions(screen, position)
		self.HP					= hp 		

	def get_HP(self):
		return self.HP	
	
	def decrease_HP(self, amount):
		self.HP -= amount

	def draw(self):
		pygame.draw.polygon (
			self.screen,  
			self.COLOR, 
			self.graphic.to_draw(self.current_position), 
			self.THICK )	
		self.actions_behavior.draw()

	def process_event(self, event):
		if event.type == Events.COLLIDE:
			self.current_position = event.where
			
			if event.stuck :
				self.current_position  = Vector(randint(0,self.screen_size.x), randint(0,self.screen_size.y))
				self.previous_position = self.current_position		
 	
		if event.type == pygame.MOUSEBUTTONDOWN:
			self.actions_behavior.process_event(event)

		if event.type == pygame.MOUSEMOTION:
			self.mouse_point = (Vector(event.pos[0], event.pos[1]))
			self.rotate_behavior.process_event(event)

		if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
			self.move_behavior.process_event(event)

	def __move(self,delta):
		self.previous_position = self.move_behavior.get_current_position()
		self.velocity 		   = self.move_behavior.get_velocity()
		self.current_position  += (self.velocity*delta)*self.speed
		self.rotate_behavior.update_position(self.current_position)
	
	def handle_rotation(self):
		if self.rotate_behavior.get_rotation_change() :
			self.graphic.rotate(self.rotate_behavior.get_rotation_angle())

	def update(self, delta):				
		self.__move(delta)
		self.move_behavior.handle_orientation_key_press()	
		self.handle_rotation()
		self.actions_behavior.update(delta, self.current_position)

