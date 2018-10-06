import pygame

#biblioteka ze zdarzeniami : jst opis jak uzywac
from events import *

#kazdy obiekt na scenie musi miec metode draw, process_event i update :) z 
#taka samą nazwą i iloscia argumntów
class Player:
	#pola classy
	r     = 0.0
	pos   = [0.0,0.0]
	color = (0,0,0)
	current_screen = None
	
	
	#Construktor 
	def __init__(self,color,position,radius, screen):
		self.r     			= radius
		self.pos   			= position
		self.color			= color
		self.current_screen = screen
	
	#funkcja odpowiedzialna za rysowanie [ current_screen to okno ]
	def draw(self):
		pygame.draw.circle(self.current_screen,  self.color, self.pos, self.r )
		
	#funkcja odpowiedzialna za obsluge zdarzen
	def process_event(self,event):
	
		if event.type == Events.CREATE:
			print( event.name )
	
		pass
		
	#funcja odpowiedzialna ze aktualizacje stanu/ ruch, kolor, kwiatki,
	#	baranki .. i kucyki ... zawsze kucyki 
	def update(self, delta):
		pass