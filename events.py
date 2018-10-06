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
	CREATE = 0
	
def rise_event( event_type, desciption):
	pygame.event.post(pygame.event.Event(int(event_type), desciption))