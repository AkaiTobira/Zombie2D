import pygame
 
 
from time     import sleep
from game     import Game 

 
def main():

	game = Game((1024,720), "Zombie2D")
	clock = pygame.time.Clock()
    #logo = pygame.image.load("logo32x32.png")
    #pygame.display.set_icon(logo)
	while game.is_running():
		delta = clock.tick()/1000
	#	sumi = delta
		game.draw()
		game.update(delta)
		game.process_input()
	#	while sumi <= 1/45:
	#		sumi += clock.tick()/1000
	#		sleep(0.0001)
     
if __name__=="__main__":
	main()