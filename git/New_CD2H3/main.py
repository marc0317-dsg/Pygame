"""
@author: CD2H3 members

"""
import pygame
import sys
import os
import time
from pygame.locals import *
import random
import hanoi
import puzzlegame
import sudoku

pygame.init()
size=(800,600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Christmas game")# window tittle
bg = pygame.mixer.Sound('sound/Christmas music.mp3')
back1 =pygame.image.load('images/back1.png')
about =pygame.image.load('images/about.jpg')
about1 =pygame.image.load('images/about1.png')


def show_image(image):
	background = pygame.image.load(image).convert()  
	screen = pygame.display.set_mode(size)
	screen.blit(background,(0,0))
	pygame.display.update()

def toabout() :
    screen.blit(about,(0,0))# show "how to play"
    screen.blit(back1,(100,500))# show "back"
    bg.stop()# stop music

def main():
    show_image("images/Background.png") #main page background
    screen.blit(about1, (600, 500))
    pygame.display.flip()  # update the surface
    bg.set_volume(0.2)
    bg.play(-1) # Keep playing music
    while True:
        # quit game
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            #Mouse triggers three games   
            elif event.type==MOUSEBUTTONDOWN:
                x=event.pos[0]
                y=event.pos[1]
                if (x in range(500,580) or x in range(700,780)) and y in range(335,360):
                    bg.stop()
                    puzzlegame.play()  # play the Jigsaw Puzzle game
                    # when the player win or exit the game
                    # call main recursively to show the main interface and waiting for input form
                    # user
                    main()
                elif x in range(270,407) and y in range(424,470):#if the user clicks the middle window
                    bg.stop()
                    hanoi.play()#play the hanoi game
                    #when the player win or exit the game
                    #call main recursively to show the main interface and waiting for input form
                    #user
                    main()
                elif x in range(533,642) and y in range(182,210):
                    bg.stop()
                    sudoku.play()  # play the sudoku game
                    # when the player win or exit the game
                    # call main recursively to show the main interface and waiting for input form
                    # user
                    main()
                elif x in range(600,700) and y in range(500,550):
                    #bg.stop()
                    toabout()
                    pygame.display.flip()
                    while True:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:  # window closing event
                                # pygame.quit()
                                quit()
                            elif event.type == pygame.MOUSEBUTTONDOWN:  # mouse click event
                                if pygame.mouse.get_pressed() == (1, 0, 0):  # press the left mouse button
                                    # sound.play()
                                    mx, my = pygame.mouse.get_pos()  # gets the current mouse coordinates
                                    if mx > 100 and mx < 200:  # back to play
                                        if my > 500 and my < 550:
                                            main()
                                            # pygame.mixer.music.play(-1, 0.0, 0)

                                        return
                else:
                    pass





if __name__=="__main__":
    main()