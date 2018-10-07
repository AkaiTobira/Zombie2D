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
		#print( self.basic )
	
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

	key_pressed     = { 
						"up"   : 
						{ 
							"scancode": [72, 17],
							"enable"  : False,
							"rotation": 0,
							"velocity": Vector( 0.0, -1.0)
						},
						"down"   : 
						{ 
							"scancode": [80, 31],
							"enable"  : False,
							"rotation": math.pi,
							"velocity": Vector( 0.0, 1.0)
						},
						"left"   : 
						{ 
							"scancode": [77, 32],
							"enable"  : False,
							"rotation": math.pi/2,
							"velocity": Vector( 1.0, 0.0)
						},
						"right"   : 
						{ 
							"scancode": [75, 30],
							"enable"  : False,
							"rotation": -math.pi/2,
							"velocity": Vector( -1.0, 0.0)
						}
					}
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
		

	def set_direction(self, velocity, direction, angle): # nazwa do ustalenia
		self.velocity += velocity
		self.velocity = self.velocity.norm()
		if self.direction != direction:
			self.direction = direction
			self.rotate_angle = angle
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
			self.enable_key_pressed(self.scancode_to_direction(event.scancode))
		elif event.type == pygame.KEYUP:
			self.disable_key_pressed(self.scancode_to_direction(event.scancode))
			self.velocity = Vector(0,0)

		
	# funcja odpowiedzialna ze aktualizacje stanu/ ruch, kolor, kwiatki,
	# baranki .. i kucyki ... zawsze kucyki 
	
	def __move(self):
		self.previous_position = self.current_position
		self.current_position  += self.velocity
	
	def update(self, delta):				
		self.__move()

		self.handle_direction_key_press()	
		
		if self.rotation_change :
	#		self.relative_point.rotate(self.rotate_angle)
			self.graphic.rotate(self.rotate_angle)
			self.rotation_change = False

		
		pass