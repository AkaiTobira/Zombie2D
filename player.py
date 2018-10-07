import pygame

#biblioteka ze zdarzeniami : jst opis jak uzywac
from events import *
#autorska biblioteka z vectorami
from vector import Vector


#kazdy obiekt na scenie musi miec metode draw, process_event i update :) z 
#taka samą nazwą i iloscia argumntów
class Player:
	# pola klasy
	x 	   = 0.0
	y 	   = 0.0
	r      = 0.0
	thick  = 0.0
	color  = (0,0,0) # 255, 21, 82
	current_screen = None
	
	current_position  = Vector(0,0)
	previous_position = Vector(0,0)
	
	#Construktor 
	def __init__(self,color,pos_x, pos_y,radius, thickness, screen):
		self.r     			= radius
		#for collisions
		self.current_position  = Vector(pos_x, pos_y)
		self.previous_position = Vector(pos_x, pos_y)

		self.x 				= pos_x
		self.y 				= pos_y
		self.color			= color
		self.current_screen = screen
		self.thick			= thickness

	
	#funkcja odpowiedzialna za rysowanie [ current_screen to okno ]
	def draw(self):
	#	pygame.draw.circle(self.current_screen,  self.color, [self.x, self.y], self.r, self.thick )
		pygame.draw.polygon(
			self.current_screen,  
			self.color, 
			[(self.x,self.y-self.r),(self.x-self.r,self.y+(self.r/2)),(self.x+self.r,self.y+(self.r/2))], 
			self.thick)
		
	#funkcja odpowiedzialna za obsluge zdarzen
	def process_event(self,event):
	
		if event.type == pygame.KEYDOWN:
			if event.scancode == 75:
				self.x -= 0.5
			print( event )
		
		if event.type == Events.CREATE:
			print( event.name )
	
		pass
		
	#funcja odpowiedzialna ze aktualizacje stanu/ ruch, kolor, kwiatki,
	#	baranki .. i kucyki ... zawsze kucyki 
	def update(self, delta):
		self.previous_position = self.current_position
		self.current_position  = Vector(self.x, self.y)
		pass