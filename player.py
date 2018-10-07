import pygame

# biblioteka ze zdarzeniami : jst opis jak uzywac
from events import *
# autorska biblioteka z vectorami
from vector import Vector

import math

class Triangle:
	vertices = [ Vector(0.0,0.0), Vector(0.0,0.0), Vector(0.0,0.0) ]
	basic    = [] 
	
	def __init__(self, size):
		
		half_of_size = (0.5 * size)
	
		self.vertices[0].x = 0.0
		self.vertices[0].y = -half_of_size
		
		self.vertices[1].x = -half_of_size
		self.vertices[1].y = half_of_size
		
		self.vertices[2].x = half_of_size 
		self.vertices[2].y = half_of_size
		
		self.basic = self.vertices.copy()
		
	def rotate(self, angle):
		print( self.basic )
	
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

	RADIUS = 10
	id = 0

	# pola klasy
	x 	   = 0.0
	y 	   = 0.0
	r      = 0.0
	thick  = 0.0
	color  = (0,0,0)
	current_screen 	= None

	pressed = [False, False, False, False] # [up, down, left, right]

	direction 		= "up"

	vertices = [(0,0), (0,0), (0,0)]

	step   = 1.0
	
	current_position  = Vector(0,0)
	previous_position = Vector(0,0)
	relative_point    = Vector(0,0)
	velocity          = Vector(0,0)
	
	graphic = Triangle(0)
	
	rotation_angle = 0.0
	rotation_change = False
	
	# Construktor 
	def __init__(self, color, pos_x, pos_y, radius, thickness, screen):
		self.graphic            = Triangle( 20 )
		self.r     			   	= radius
		# for collisions
		self.current_position  	= Vector(pos_x, pos_y)
		self.previous_position 	= Vector(pos_x, pos_y)
		self.relative_point     = Vector(
			self.current_position.x, self.current_position.y + 1).norm()
		self.x 					= pos_x
		self.y 					= pos_y
		self.color				= color
		self.current_screen 	= screen
		self.thick				= thickness

				
	# funkcja odpowiedzialna za rysowanie [ current_screen to okno ]
	def draw(self):
		pygame.draw.polygon (
			self.current_screen,  
			self.color, 
			self.graphic.to_draw(self.current_position), 
			self.thick )
		

	def keydown_event_handler(self, vec, d, angle):
		self.current_position += vec
		if self.direction != d:
			self.direction = d
			self.rotate_angle = angle
			self.rotation_change = True

	def scan_event(self, e, b):
		if e.scancode == 75 or e.scancode == 30:
			self.pressed[3] = b
		if e.scancode == 77 or e.scancode == 32:
			self.pressed[2] = b
		if e.scancode == 72 or e.scancode == 17:
			self.pressed[0] = b
		if e.scancode == 80 or e.scancode == 31:
			self.pressed[1] = b		

	# funkcja odpowiedzialna za obsluge zdarzen
	def process_event(self, event):
 	
	# Za myszką ale ciągle nie gotowe :/ problem jest w obliczaniu kąta pomniedzy dwoma wektorami
	# Jeden jest wyznaczony przez połozenie myszki, a drugi nie wiem :)
	# Matematyka na wektorach :)  btw => nie dobałem wartości poniżej nie chciało mi się
	# Jakby trzeba było to masz biblioteke operacji na wektorach ... moją ale zawsze coś, i zawsze
	# można coś brakującego dopisać
	
	
	#	if event.type == pygame.MOUSEMOTION :
	#		face           = Vector(1,0).norm()
	#		mouse_point    = (Vector(event.pos[0], event.pos[1])).norm()	
	#		self.rotate_angle = face.angle_between( mouse_point ) 
	#		self.rotation_change = True
	#		self.rotation_change = True
	#		pass
	
		if event.type == Events.COLLIDE:
			self.current_position = event.where
			
			if event.stuck :
				self.current_position = Vector(randint(0,self.screen_size.x), randint(0,self.screen_size.y))
				self.previous_position   = self.current_position
	
	
		if event.type == pygame.KEYDOWN:
			self.scan_event(event, True)
		elif event.type == pygame.KEYUP:
			self.scan_event(event, False)			

		
	# funcja odpowiedzialna ze aktualizacje stanu/ ruch, kolor, kwiatki,
	# baranki .. i kucyki ... zawsze kucyki 
	def update(self, delta):				
		self.previous_position = self.current_position

		if self.pressed[0]:
			self.keydown_event_handler(Vector(0.0, -1.0), "up", 0)
		if self.pressed[1]:
			self.keydown_event_handler(Vector(0.0, 1.0), "down", math.pi)
		if self.pressed[2]:
			self.keydown_event_handler(Vector(1.0, 0.0), "left", math.pi/2)
		if self.pressed[3]:	
			self.keydown_event_handler(Vector(-1.0, 0.0), "right", -math.pi/2)			
		
		if self.rotation_change :
	#		self.relative_point.rotate(self.rotate_angle)
			self.graphic.rotate(self.rotate_angle)
			self.rotation_change = False

		
		pass