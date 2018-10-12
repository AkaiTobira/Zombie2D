import pygame

# biblioteka ze zdarzeniami : jst opis jak uzywac
from events import Events, rise_event
# autorska biblioteka z vectorami
from vector import Vector
from random import randint
from colors import Colors, get_color

import math

class Triangle:
	vertices = [ Vector(0.0,0.0), Vector(0.0,0.0), Vector(0.0,0.0) ]
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
				 (position + self.vertices[2]).to_touple()
			]
	
class Player_move:

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

	
class Player_rotate:

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
		mouse_vec = mouse_point - self.position   
		face_vec = self.face - self.position
		self.rotation_angle = face_vec.norm().angle_between(mouse_vec.norm()) 
		self.rotation_change = True

	def print_rotation_angle(self):
		print("rotate angle: [ " + str(round(self.rotation_angle * 180 / math.pi)) + " ] degrees")

	def get_rotation_angle(self):
		return self.rotation_angle	

	def get_rotation_change(self):
		return self.rotation_change

	def set_rotation_change(self, change):
		self.rotation_change = change


# kazdy obiekt na scenie musi miec metode draw, process_event i update :) z 
# taka samą nazwą i iloscia argumntów
class Player:

	id     			= 0
	THICK  			= 3
	RADIUS			= 10
	COLOR  			= get_color(Colors.LIGHT_RED)
	current_screen 	= None
	player_move		= None
	player_rotate   = None

	current_position  = Vector(0,0)
	previous_position = Vector(0,0)
	velocity          = Vector(0,0)
	mouse_point		  = Vector(0,0)

	graphic = Triangle(0)

	
	# Construktor 
	def __init__(self, position, screen):
		self.graphic            = Triangle( 10 )
		self.current_position  	= position
		self.previous_position 	= position
		self.current_screen 	= screen
		self.player_move 		= Player_move(position)
		self.player_rotate		= Player_rotate(position)


	# funkcja odpowiedzialna za rysowanie [ current_screen to okno ]
	def draw(self):
		pygame.draw.polygon (
			self.current_screen,  
			self.COLOR, 
			self.graphic.to_draw(self.current_position), 
			self.THICK )

		# linia od gracza do kursora myszy
		pygame.draw.line(self.current_screen, get_color(Colors.YELLOW),self.current_position.to_table(), self.mouse_point.to_table())

		# kursor myszy - okrag
		pygame.draw.circle(self.current_screen, get_color(Colors.YELLOW), self.mouse_point.to_table(), 10, 2)
		

	# funkcja odpowiedzialna za obsluge zdarzen
	def process_event(self, event):

		if event.type == Events.COLLIDE:
			self.current_position = event.where
			
			if event.stuck :
				self.current_position  = Vector(randint(0,self.screen_size.x), randint(0,self.screen_size.y))
				self.previous_position = self.current_position		
 	
		if event.type == pygame.MOUSEMOTION :
			self.mouse_point = (Vector(event.pos[0], event.pos[1]))
			self.player_rotate.process_event(self.mouse_point)
	
		if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
			self.player_move.process_event(event)

		
	# funcja odpowiedzialna ze aktualizacje stanu/ ruch, kolor
	def __move(self):
		self.previous_position = self.player_move.get_current_position()
		self.velocity 		   = self.player_move.get_velocity()
		self.current_position  += self.velocity
		self.player_rotate.update_position(self.current_position)
	
	def update(self, delta):				
		self.__move()

		self.player_move.handle_orientation_key_press()	
		
		if self.player_rotate.get_rotation_change() :
			self.graphic.rotate(self.player_rotate.get_rotation_angle())
			self.player_rotate.set_rotation_change(False)

		pass