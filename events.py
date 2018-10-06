import pygame

from vector import *
from enum import IntEnum



# jak uzywac :
# Dopisac kolejny event do Enuma Events 
# wywolac rise_event() tam gdzie zaczelo sie zdarzenie 
# dscription to slownik
# w odpowiednim process_event dodac if-a pasujacego do enuma
# prztworzyc ... tyle



class Events(IntEnum):
	CREATE 		= 0
	K_UP   		= 1
	K_DOWN   	= 2
	K_LEFT   	= 3
	K_RIGHT   	= 4	
	
def rise_event(event_type, description):
	pygame.event.post(pygame.event.Event(int(event_type), description))