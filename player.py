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
		self.enable   = False

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

	def disable_all_keys(self):
		for o in self.orientation:
			self.orientation[o].disable_orientation()

	def __init__(self, position):
		self.position = position
		self.disable_all_keys()

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

	shoot			= False # Shot started

	is_ready		= True  # Check if can shoot 
	can_draw     	= True  # Ready to draw
	r_to_draw       = True

	player_position = Vector(0,0)
	mouse_position  = Vector(0,0)
	pt_to			= Vector(1,1)
	

	def __init__(self, screen, position):
		self.player_position = position
		self.screen = screen


	def draw_railgun(self):

		pygame.draw.line(
			self.screen, 
			self.railgun_color, 
			self.player_position.to_table(), 
			self.pt_to.to_table(), 
			self.railgun_thick)		
	

	def call_shoot_event(self):
		self.pt_to   = self.player_position + (1260 * (self.mouse_position - self.player_position).norm())
		rise_event( Events.SHOOT, { 
			"pt_from" : self.player_position,
			"pt_to" : self.pt_to } )


	def distance(self, P1, P2):
		return math.sqrt(( (P1.x - P2.x) ** 2 ) + ( (P1.y - P2.y) ** 2 ) )		
	

	def process_event(self, event):

		if event.type == Events.IS_READY:
			self.is_ready = True

		if event.type == pygame.MOUSEBUTTONDOWN:
			if self.is_ready: 
				self.shoot    = True
				self.can_draw = False
				self.is_ready = False
				self.mouse_position = (Vector(event.pos[0], event.pos[1]))
				self.call_shoot_event()
			
		if event.type == Events.INTERSECTION:
			if event.point.distance_to(self.player_position).len() < self.pt_to.distance_to(self.player_position).len():
				self.pt_to = event.point
			self.can_draw = True
			

	def draw(self):
		if not self.is_ready and self.shoot  and self.can_draw :
			rise_event( Events.HIT_ENEMY_CHECK, { 
			"pt_from" : self.player_position,
			"pt_to" : self.pt_to } )
			self.draw_railgun()

	def update(self, delta, position):
		self.player_position = position
		if self.shoot:	
			self.sum_delta += delta
			if(self.sum_delta > 0.08):
				self.shoot = False
				self.sum_delta = 0

class Player:

	id     			  = 0
	HP				  = 0	
	THICK  			  = 3
	RADIUS			  = 10
	COLOR_OUT		  = get_color(Colors.LIGHT_RED)
	COLOR_IN		  = get_color(Colors.LIGHTER_RED)
	screen			  = None
	move_behavior	  = None
	rotate_behavior   = None
	actions_behavior  = None


	state 			 = "P"
	current_position  = Vector(0,0)
	previous_position = Vector(0,0)
	velocity          = Vector(0,0)
	mouse_point		  = Vector(0,0)
	screen_size       = Vector(0,0)
	graphic 		  = Triangle(0)
	freeze            = False
	speed             = Vector(100.0,100.0)

	def __init__(self, position, screen, hp):
		self.graphic            = Triangle( 12 )
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

		self.actions_behavior.draw()		

		pygame.draw.polygon (
			self.screen,  
			self.COLOR_IN, 
			self.graphic.to_draw(self.current_position))

		pygame.draw.polygon (
			self.screen,  
			self.COLOR_OUT, 
			self.graphic.to_draw(self.current_position), 
			self.THICK )

	def process_event(self, event):
		
		if event.type == Events.COLLIDE:
			self.current_position = event.where - self.velocity
			self.freeze = True

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
		if not self.freeze :
			self.__move(delta)
			self.move_behavior.handle_orientation_key_press()	
		else:
			self.freeze = False
		self.handle_rotation()
		self.actions_behavior.update(delta, self.current_position)

