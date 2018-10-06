import pygame

#biblioteka ze zdarzeniami : jst opis jak uzywac
from events import *

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

	
	#Construktor 
	def __init__(self,color,pos_x, pos_y,radius, thickness, screen):
		self.r     			= radius
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
	
		if event.type == Events.CREATE:
			print( event.name )
	
		pass
		
	#funcja odpowiedzialna ze aktualizacje stanu/ ruch, kolor, kwiatki,
	#	baranki .. i kucyki ... zawsze kucyki 
	def update(self, delta):
		pass