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

class Cursor:
	position  = 0.0
	COLOR     = get_color(Colors.YELLOW)	
	RADIUS	  = 12	
	THICK	  = 1	

	def __init__(self, position):
		self.position = position

	def draw(self, screen, mouse_point):
		pygame.draw.circle(screen, self.COLOR, mouse_point.to_table(), self.RADIUS, self.THICK)
		pygame.draw.line(screen, self.COLOR, Vector(mouse_point.x-self.RADIUS, mouse_point.y).to_table(), Vector(mouse_point.x+self.RADIUS, mouse_point.y).to_table(), self.THICK)
		pygame.draw.line(screen, self.COLOR, Vector(mouse_point.x, mouse_point.y-self.RADIUS).to_table(), Vector(mouse_point.x, mouse_point.y+self.RADIUS).to_table(), self.THICK)

class PlayerMoveBehavior:

	position  		= Vector(0,0)
	velocity  		= Vector(0,0)	
	current_screen	= None

	orientation 	= ""

	key_pressed     = { 
						"up"   : 
						{ 
							"scancode": [72, 17],
							"enable"  : False,
							"velocity": Vector(0.0, -1.0)
						},
						"down"   : 
						{ 
							"scancode": [80, 31],
							"enable"  : False,
							"velocity": Vector(0.0, 1.0)
						},
						"left"   : 
						{ 
							"scancode": [77, 32],
							"enable"  : False,
							"velocity": Vector(1.0, 0.0)
						},
						"right"   : 
						{ 
							"scancode": [75, 30],
							"enable"  : False,
							"velocity": Vector(-1.0, 0.0)
						}
					}	

	def __init__(self, position):
		self.position = position

	def set_orientation(self, velocity, orientation):
		self.velocity = (self.velocity + velocity).norm()
		if self.orientation != orientation:
			self.orientation = orientation

	def scancode_to_orientation(self, scancode):
		for key in self.key_pressed.keys():
			if scancode in self.key_pressed[key]["scancode"]:
				return str(key)
		return None
			
	def enable_key_pressed(self, orientation):
		if orientation == None: return
		self.key_pressed[orientation]["enable"] = True

	def disable_key_pressed(self, orientation):
		if orientation == None: return
		self.key_pressed[orientation]["enable"] = False

	def handle_orientation_key_press(self):
		for key in self.key_pressed.keys():
			if self.key_pressed[key]["enable"]:
				self.set_orientation(self.key_pressed[key]["velocity"], str(key))

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

	def process_event(self, mouse_point):
		self.rotation_angle = (self.face - self.position).norm().angle_between((mouse_point - self.position).norm()) 
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


class Player:

	id     			  = 0
	THICK  			  = 3
	RADIUS			  = 10
	COLOR  			  = get_color(Colors.LIGHT_RED)
	current_screen 	  = None
	move_behavior	  = None
	rotate_behavior   = None
	cursor	 		  = None

	current_position  = Vector(0,0)
	previous_position = Vector(0,0)
	velocity          = Vector(0,0)
	mouse_point		  = Vector(0,0)

	graphic 		  = Triangle(0)

	def __init__(self, position, screen):
		self.graphic            = Triangle( 10 )
		self.current_position  	= position
		self.previous_position 	= position
		self.current_screen 	= screen
		self.move_behavior 		= PlayerMoveBehavior(position)
		self.rotate_behavior	= PlayerRotateBehavior(position)
		self.cursor				= Cursor(position)

	def draw_line_to_cursor(self):
		pygame.draw.line(self.current_screen, get_color(Colors.YELLOW), self.current_position.to_table(), self.mouse_point.to_table())

	def draw(self):
		pygame.draw.polygon (
			self.current_screen,  
			self.COLOR, 
			self.graphic.to_draw(self.current_position), 
			self.THICK )

		#self.draw_line_to_cursor()
		self.cursor.draw(self.current_screen, self.mouse_point)

	def process_event(self, event):
		if event.type == Events.COLLIDE:
			self.current_position = event.where
			
			if event.stuck :
				self.current_position  = Vector(randint(0,self.screen_size.x), randint(0,self.screen_size.y))
				self.previous_position = self.current_position		
 	
		if event.type == pygame.MOUSEMOTION :
			self.mouse_point = (Vector(event.pos[0], event.pos[1]))
			self.rotate_behavior.process_event(self.mouse_point)
	
		if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
			self.move_behavior.process_event(event)

	def __move(self):
		self.previous_position = self.move_behavior.get_current_position()
		self.velocity 		   = self.move_behavior.get_velocity()
		self.current_position  += self.velocity
		self.rotate_behavior.update_position(self.current_position)
	
	def update(self, delta):				
		self.__move()
		self.move_behavior.handle_orientation_key_press()	
		
		if self.rotate_behavior.get_rotation_change() :
			self.graphic.rotate(self.rotate_behavior.get_rotation_angle())
