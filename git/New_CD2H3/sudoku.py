"""
@author: Yihang Fang AND Ziyi Zhao

"""
"""
Choose the difficulty level at the beginning.
Fill in the numbers 1-9 in the blank space .
The wrong number will appear in red.
Space can return the main page.

"""
#Import packages
import easygui as eg
import pygame
import sys
from pygame.locals import *
import random
import main

#Initialize pygame
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("Sudoku game")# window tittle
#Load music
pygame.mixer.music.load("sound/Merry Christmas.wav")
pygame.mixer.music.set_volume(0.2)  # Set the volume to 0.2

#set colours and screen size
width = 800
height = 600
WHITE = (246, 255, 247)
RED = (187, 52, 32)
DG = (19, 58, 27)
LG = (185, 183, 96)
#Initialize font
font_addr = pygame.font.get_default_font()
font = pygame.font.Font('simkai.ttf', 50)

screen = pygame.display.set_mode((width,height))

class Button(object):
    '''
                            Define button in game
  **kwargs: Multiple keyword parameters, kwargs itself is a dictionary type, 
  and the incoming parameters are presented in the form of a dictionary
  
  Reference link: https://zhuanlan.zhihu.com/p/78637310
    '''
    def __init__(self, text, color, x=None, y=None, **kwargs):
        self.surface = font.render(text, True, color)
        self.WIDTH = self.surface.get_width()
        self.HEIGHT = self.surface.get_height() 
   # **kwargs: Send a variable number of parameter lists of key-value pairs to the function


        if 'mid_x' in kwargs and kwargs['mid_x']:  #if we need position of button in middle of screen
            self.x = width // 2 - self.WIDTH // 2
        else:
            self.x = x

        if 'mid_y' in kwargs and kwargs['mid_y']:
            self.y = height // 2 - self.HEIGHT // 2
        else:
            self.y = y
            
   # Place buttuon position         
    def display(self):
        screen.blit(self.surface, (self.x, self.y))  


    def check_click(self, position):
        '''
        This function check the click position
        :param position: The position of mouse click
        :return: True or False
        '''
        x_match = position[0] > self.x and position[0] < self.x + self.WIDTH
        y_match = position[1] > self.y and position[1] < self.y + self.HEIGHT

        if x_match and y_match: # if both x and y are matched then return True
            return True
        else:
            return False


def set_sudoku(grid,n):
    '''
    :param grid: represent completed sudoku
    :param n: Number of vacancies in Sudoku
    :return: return an imcompleted sudoku
    '''
    new_grid=[[i for i in j] for j in grid]
    lst=[]
    for i in range(n):
        while True:
            x = random.randint(0,8)
            y = random.randint(0,8)
            if (x,y) not in lst:
                lst.append((x,y))
                new_grid[x][y] = None
                break

    return new_grid

def display(screen,grid,area,errors):
    '''
    This fuction displays sudoku

    :param screen: The screen of pygame
    :param grid: sudoku
    :param area: Mouse selected place
    :param errors: It's a list and store positions if the number in sudoku is wrong
    Reference link: https://github.com/YYX-computer
    This reference link inspired me how to draw grid to interface, and I write this function to display numbers on screen.
    '''

    #set font
    font = pygame.font.Font('simkai.ttf',100)
    width=int(800/3)
    height=200
    font_size=(60,70)
    font_pos=(800/9,600/9)

    #draw grid
    for i in range(9):
        for j in range(9):
            if (j,i) == area:      # if the position is selected
                color = [DG,LG]    #corlor stores color of font and color of filling

            elif (j,i) in errors:  #if the position in errors
                color = [RED,DG]

            else:
                color = [WHITE,DG]

            if grid[i][j] == None: #if there is no font in this position
                no_font = font.render(' ', True, color[0],color[1])  #display none

            else:
                no_font = font.render(str(grid[i][j]),True,color[0],color[1])  #display font

            no_font = pygame.transform.scale(no_font,font_size)   #set fontsize
            screen.blit(no_font,(font_pos[0] * j,font_pos[1] * i))
    #draw rect to divide sudoku
    for i in range(3):
        for j in range(3):
            pygame.draw.rect(screen,WHITE,Rect((width * i,height* j),(width,height)),3)




def instruction():
    '''
    This fuction is an intrduction of sudoku
    :return: if click play button, come into sudoku game; if click back button return main game
    '''

    #load image
    bg = pygame.image.load('images/instruction.png')
    screen.blit(bg, (0, 0))

    #use class Button to define play button and back button
    play_button = Button('Play', RED, None, 360, mid_x=True)
    back_button = Button('Back', WHITE, None, 420, mid_x=True)

    #display the button
    play_button.display()
    back_button.display()

    pygame.display.update()

    while True:

        if play_button.check_click(pygame.mouse.get_pos()):   #if we click button and the color of button will be red, else is white
            play_button = Button('Play', RED, None, 360, mid_x=True)
        else:
            play_button = Button('Play', WHITE, None, 360, mid_x=True)

        if back_button.check_click(pygame.mouse.get_pos()):   #as the same as play button
            back_button = Button('Back', RED, None, 420, mid_x=True)
        else:
            back_button = Button('Back', WHITE, None, 420, mid_x=True)

        #display button again
        play_button.display()
        back_button.display()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:    #quit game
                pygame.quit()
                raise SystemExit

        if pygame.mouse.get_pressed()[0]:   #if click
            if play_button.check_click(pygame.mouse.get_pos()):  #if click play button and check the position we click then get into sudoku game
                return
            if back_button.check_click(pygame.mouse.get_pos()): #if click back button then return main page
                pygame.mixer.music.stop()  #end music
                return main.main()  #return main page

def win():
    '''
    This function defines victory interface
    :return: return back main page
    '''

    #set back button
    #back_button = Button('Back', RED, None, 30, mid_x=True)
    back_button = Button('Back', RED, 0,0)

    #set win page
    background = pygame.image.load("images/win.jpg").convert()
    screen = pygame.display.set_mode((width,height))
    screen.blit(background, (0, 0))
    pygame.display.update()


    while True:
        if back_button.check_click(pygame.mouse.get_pos()): #same in function instruction()
            back_button = Button('Back', RED, 0, 0)
        else:
            back_button = Button('Back', DG, 0, 0)
        back_button.display()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        if pygame.mouse.get_pressed()[0]:
            if back_button.check_click(pygame.mouse.get_pos()):
                return

def play():
    '''
    This fuction plays sudoku game
    '''

    # play music
    pygame.mixer.music.load("sound/Merry Christmas.wav")
    pygame.mixer.music.set_volume(0.2)  # Set the volume to 0.2
    pygame.mixer.music.play()

    instruction()  #come into instruction

    #use easygui to establish interaction with users and users can change the number of Sudoku vacancies
    #reference link: http://easygui.sourceforge.net
    msg="Please select the number of empty"   #message in GUI
    title="Choose number"  #title of GUI
    name=["number (range 1 to 40)"]
    value=[]
    value=eg.multenterbox(msg,title,name)  #this variable 'value' is used to store value of inputs, data type is string

    try:       #try  ... except ... is used to control input

        num=int(value[0])

        if num in range(1,41):    #control range of numbers

            #initialize sudoku as a grid
            grid = [[5, 3, 4, 6, 7, 8, 9, 1, 2],
                    [6, 7, 2, 1, 9, 5, 3, 4, 8],
                    [1, 9, 8, 3, 4, 2, 5, 6, 7],
                    [8, 5, 9, 7, 6, 1, 4, 2, 3],
                    [4, 2, 6, 8, 5, 3, 7, 9, 1],
                    [7, 1, 3, 9, 2, 4, 8, 5, 6],
                    [9, 6, 1, 5, 3, 7, 2, 8, 4],
                    [2, 8, 7, 4, 1, 9, 6, 3, 5],
                    [3, 4, 5, 2, 8, 6, 1, 7, 9]]
            screen = pygame.display.set_mode((width,height),DOUBLEBUF)
            screen.fill(DG)

            ques = set_sudoku(grid,num)         #set the question of sudoku
            area = None                         #area which is selected
            errors = []                         # if number is in error then store positions to list
            valid_input=[str(i) for i in range(1,10)]       #control valid input

            while True:
                if ques == grid:  #judge whether the answer is correct
                    break

                #display sudoku
                display(screen,ques,area,errors)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

                    elif event.type == MOUSEBUTTONDOWN:
                        #(x,y) is the positon of sudoku

                        x= event.pos[0]//88
                        y=event.pos[1]//66

                        if ques[y][x] == None or (x,y) in errors:  #if the number is none or in error then the position can be selected
                            area = (x,y)

                    elif event.type == KEYDOWN:
                        if event.key==K_SPACE:  #if print space the return main page
                            pygame.mixer.music.stop()
                            return

                        elif event.unicode not in valid_input or (not event.unicode) or (not area): #if input is invalid or not select then keep going on
                            continue

                        else:
                            ques[area[1]][area[0]] = int(event.unicode)  #input number to sudoku

                            if grid[area[1]][area[0]] != ques[area[1]][area[0]] and area not in errors: #if number is not equal to answer and position is not in errors, then append error position
                                errors.append(area)

                            if grid[area[1]][area[0]] == ques[area[1]][area[0]] and area in errors: #if add correct number to wrong position, then remove this incorrect position in errors
                                errors.remove(area)
        else:
            return play()
    except:
        return play()   # if input is not numerical, then return back to sudoku game


    win()   #display win page

    pygame.mixer.music.stop()  #end music


