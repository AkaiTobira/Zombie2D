import pygame
 
 

from game     import Game 
 
def main():

	game = Game((1024,720), "Zombie2D")

	#
    # load and set the logo
    #logo = pygame.image.load("logo32x32.png")
    #pygame.display.set_icon(logo)
	
	while game.is_running():
		game.draw()
		game.process_input()
		game.process_physic()
     
     
if __name__=="__main__":
	main()