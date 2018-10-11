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
	


# kazdy obiekt na scenie musi miec metode draw, process_event i update :) z 
# taka samą nazwą i iloscia argumntów
class Player:

	id     			= 0
	THICK  			= 3
	RADIUS			= 10
	COLOR  			= get_color(Colors.LIGHT_RED)
	current_screen 	= None
	direction 		= "up"

	key_pressed     = { 
						"up"   : 
						{ 
							"scancode": [72, 17],
							"enable"  : False,
							"rotation": 0,
							"velocity": Vector(0.0, -1.0)
						},
						"down"   : 
						{ 
							"scancode": [80, 31],
							"enable"  : False,
							"rotation": math.pi,
							"velocity": Vector(0.0, 1.0)
						},
						"left"   : 
						{ 
							"scancode": [77, 32],
							"enable"  : False,
							"rotation": math.pi/2,
							"velocity": Vector(1.0, 0.0)
						},
						"right"   : 
						{ 
							"scancode": [75, 30],
							"enable"  : False,
							"rotation": -math.pi/2,
							"velocity": Vector(-1.0, 0.0)
						}
					}


	current_position  = Vector(0,0)
	previous_position = Vector(0,0)
	velocity          = Vector(0,0)
	face              = Vector(0,0)
	mouse_point       = Vector(0,0)
	mouse_vec 		  = Vector(0,0)
	
	graphic = Triangle(0)
	
	rotation_angle = 0.0
	rotation_change = False
	
	# Construktor 
	def __init__(self, position, screen):
		self.graphic            = Triangle( 10 )
		self.current_position  	= position
		self.previous_position 	= position
		self.current_screen 	= screen

				
	# funkcja odpowiedzialna za rysowanie [ current_screen to okno ]
	def draw(self):
		pygame.draw.polygon (
			self.current_screen,  
			self.COLOR, 
			self.graphic.to_draw(self.current_position), 
			self.THICK )

		self.face = Vector(
			self.current_position.x,
			self.current_position.y - 200)
		# linia od gracza pionowo do gory	
		#pygame.draw.line(self.current_screen, get_color(Colors.YELLOW),self.current_position.to_table(), self.face.to_table())

		 # linia od gracza do kursora myszy
		pygame.draw.line(self.current_screen, get_color(Colors.YELLOW),self.current_position.to_table(), self.mouse_point.to_table())

		# kursor myszy - okrag
		pygame.draw.circle(self.current_screen, get_color(Colors.YELLOW), self.mouse_point.to_table(), 10, 2)
		
		

	def set_direction(self, velocity, direction, angle): # nazwa do ustalenia
		self.velocity += velocity
		self.velocity = self.velocity.norm()
		if self.direction != direction:
			self.direction = direction
			self.rotation_change = True

			
	def scancode_to_direction(self, scancode): # to by się już dało tylko dziedziczeniem
		for key in self.key_pressed.keys():
			if scancode in self.key_pressed[key]["scancode"]:
				return str(key)
		return None
			
	def enable_key_pressed(self, direction):
		if direction == None: return
		self.key_pressed[direction]["enable"] = True

	def disable_key_pressed(self, direction):
		if direction == None: return
		self.key_pressed[direction]["enable"] = False

	def handle_direction_key_press(self): # da się zrefaktorować ale przestanie się obracać
		for key in self.key_pressed.keys():
			if self.key_pressed[key]["enable"]:
				self.set_direction(self.key_pressed[key]["velocity"], str(key), self.key_pressed[key]["rotation"])

	# funkcja odpowiedzialna za obsluge zdarzen
	def process_event(self, event):
 	
		if event.type == pygame.MOUSEMOTION :
			self.mouse_point = (Vector(event.pos[0], event.pos[1]))
			self.mouse_vec = self.mouse_point - self.current_position   
			face_vec = self.face - self.current_position
			self.rotate_angle = face_vec.norm().angle_between( self.mouse_vec.norm() ) 
			#print ("rotate angle: " + str(round(self.rotate_angle * 180 / math.pi)) )
			self.rotation_change = True
			pass
	
		if event.type == Events.COLLIDE:
			self.current_position = event.where
			
			if event.stuck :
				self.current_position = Vector(randint(0,self.screen_size.x), randint(0,self.screen_size.y))
				self.previous_position   = self.current_position
	
		if event.type == pygame.KEYDOWN:
			self.enable_key_pressed(self.scancode_to_direction(event.scancode))
		elif event.type == pygame.KEYUP:
			self.disable_key_pressed(self.scancode_to_direction(event.scancode))
			self.velocity = Vector(0,0)

		
	# funcja odpowiedzialna ze aktualizacje stanu/ ruch, kolor
	def __move(self):
		self.previous_position = self.current_position
		self.current_position  += self.velocity
	
	def update(self, delta):				
		self.__move()

		self.handle_direction_key_press()	
		
		if self.rotation_change :
			self.graphic.rotate(self.rotate_angle)
			self.rotation_change = False

		
		pass