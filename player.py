import pygame

# biblioteka ze zdarzeniami : jst opis jak uzywac
from events import *
# autorska biblioteka z vectorami
from vector import Vector

class Triangle:
	vertices = [ Vector(0.0,0.0), Vector(0.0, 0.0), Vector(0.0, 0.0)]
	basic    = [] 
	
	def __init__(self, size ):
		
		half_of_size = (0.5 * size)
	
		self.vertices[0].x = - half_of_size
		self.vertices[0].y = - half_of_size
		
		self.vertices[1].x = half_of_size
		self.vertices[1].y = - half_of_size
		
		self.vertices[2].x = 0.0 
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
	# pola klasy
	x 	   = 0.0
	y 	   = 0.0
	r      = 0.0
	thick  = 0.0
	color  = (0,0,0) # 255, 21, 82
	current_screen 	= None

	pressed_left   	= False	
	pressed_right   = False	
	pressed_up   	= False	
	pressed_down   	= False	

	direction 		= "up"

	vertices = [(0,0), (0,0), (0,0)]

	step   = 0.08
	
	current_position  = Vector(0,0)
	previous_position = Vector(0,0)
	relative_point    = Vector(0,0)
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
		self.relative_point     = Vector(self.current_position.x, self.current_position.y + 1).norm()
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
	
		if event.type == pygame.KEYDOWN:
			if event.scancode == 75 or event.scancode == 30:
				self.current_position += Vector(-1.0, 0.0)
				if self.direction != "right":
					self.direction = "right"
					self.rotate_angle = 3.14/2
					self.rotation_change = True
				
			if event.scancode == 77 or event.scancode == 32:
				self.current_position += Vector(1.0, 0.0)
				if self.direction != "left":
					self.direction = "left"	
					self.rotate_angle = -3.14/2
					self.rotation_change = True
			if event.scancode == 72 or event.scancode == 17:
				self.current_position += Vector(0.0, 1.0)
				if self.direction != "up":
					self.direction = "up"
					self.rotate_angle = 3.14
					self.rotation_change = True
			if event.scancode == 80 or event.scancode == 31:
				self.current_position += Vector(0.0, -1.0)
				if self.direction != "down":
					self.direction = "down"
					self.rotate_angle = 0
					self.rotation_change = True
		
		
		
	# funcja odpowiedzialna ze aktualizacje stanu/ ruch, kolor, kwiatki,
	# baranki .. i kucyki ... zawsze kucyki 
	def update(self, delta):				
		self.previous_position = self.current_position
		
		if self.rotation_change :
	#		self.relative_point.rotate(self.rotate_angle)
			self.graphic.rotate(self.rotate_angle)
			self.rotation_change = False

		
		pass