import pygame
 
 
from time import sleep

from game     import Game 
 
def main():

	game = Game((1024,720), "Zombie2D")

	#
    # load and set the logo
    #logo = pygame.image.load("logo32x32.png")
    #pygame.display.set_icon(logo)
	
	while game.is_running():
		fps = pygame.time.get_ticks()
		game.draw()
		game.process_input()
		game.process_physic()
		while (pygame.time.get_ticks() - fps )/1000 <= 1/60:
			#print( ( fps - pygame.time.get_ticks())/1000  )
			sleep(0.0001)
     
     
if __name__=="__main__":
	main()