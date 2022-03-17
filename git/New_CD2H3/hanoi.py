"""
@author: Junyi Guan AND Jieying Huang

"""
"""
You can control the Christmas tree through the keyboard, assemble each 
position to get a gift, and complete three tasks！

"""
#Import packages
import pygame
from pygame.locals import *
import sys
pygame.init()
pygame.mixer.init()

"""
                            loading graphics
"""


trunk = pygame.image.load('images/trunk.PNG')   # a trunk picture
Ptrunk = pygame.image.load('images/Ptrunk.PNG') # a trunk with an arrow
first = pygame.image.load('images/first.PNG')   # Top layer of the christmas tree
middle = pygame.image.load('images/middle.PNG') # middle layer of the christmas tree
last = pygame.image.load('images/last.PNG')     # bottom layer of the christmas tree
helpText = pygame.image.load('images/Tree of Hanoi.png') # help text picture
gift = pygame.image.load('images/gift1.png') #gift picture
question = pygame.image.load('images/question_mark.png') # question mark picture
home = pygame.image.load('images/home.png')
winPicture = pygame.image.load('images/win-hanoi.jpg') # a question mark
"""
                            loading music 
"""
move_sound = pygame.mixer.Sound('sound/Sand.mp3') #sound effect for a correct action
error_sound = pygame.mixer.Sound('sound/error.mp3') #sound effect Incorrect action


"""
                            variable initialization
"""
width = 800 
high = 600
screen = pygame.display.set_mode((width,high))#create a display with 800*600
numTrees = 3 #There are 3 trees
Selected_trees = [] # a list to represent the trees are selected
trunk_y = high - trunk.get_rect()[-1] # the y coordinate of each trunk

# a list to repersent the coordinate of each trunk
trunkPos = [(0,trunk_y),\
            ((width - trunk.get_rect()[-2]) // 2,\
             trunk_y),(width - trunk.get_rect()[-2],trunk_y)]

# different layer picture 
layers_Pic = [first,middle,last]
radiusq = (question.get_rect()[2])//2 # The radius of question mark
center_xq , center_yq = width - radiusq , radiusq # The center of question mark

radiush = (question.get_rect()[2])//2 # The radius of home mark
center_xh , center_yh = radiush , radiush # The center of home mark
clock = pygame.time.Clock()
done = False #the game is not finish

class Blakground():
    bottom = 16384 - high
    bgPic = pygame.image.load('images/color.png')
    speed = 1 #The speed of snow
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def update(self):#repead the snow
        """
        update the blakground and draw it
        """
        self.y = self.y - Blakground.speed
        if self.y < 0:
            self.y = Blakground.bottom
        screen.blit(Blakground.bgPic,(0,0),(self.x,self.y,width,high))
bg = Blakground(0,0)
        
"""
create a Forest class
the attribute matrix is used to represent 3 Tress
the 0 index is  list  to represent the left tress
the 1 index is  list  to represent the middle tress
the 2 index is  list  to represent the right tress

In each tree(list) 
0 to repersent the first layer
1 to repersent the second layer
2 to repersent the third layer

the gifts is a list to represent which tree has a gifts below
The index of the list also used to pointing the tree

The pointer points to the tree that the player wants to cut

"""        
class Forest():
    def __init__(self,matrix):
        self.matrix = matrix
        self.gifts = [0,0,0]
        self.pointer = None
    def draw(self):
        """
        draw all trees and gifts and arrow
        """
        for i in range(numTrees):
            x , y = trunkPos[i][0] , trunkPos[i][1]   #present the trunk
            if self.pointer == i:
                screen.blit(Ptrunk,(x,y))     #preset the arrow if the trunk is chosen
                self.pointer == None
            else:
                screen.blit(trunk,(x,y))   #hide the arrow if the is not chosen
            if self.gifts[i] == 1:         #present the gift if the tree is finish
                screen.blit(gift,(x,y))
            for layer in self.matrix[i]:   #present the layer of tree
                layerHight = layers_Pic[layer].get_rect()[-1]
                y = y - layerHight
                screen.blit(layers_Pic[layer],(x ,y))        
        
            
    def moveTree(self,lst):
        """
        if the lenth of the list is 1 which means the player 
        has alredy choose a tree he want to cut,in this case use a pointer
        to refer it
        
        if the lenth of the list is 2 which means the player choose a sorce 
        if it is a valid move check if a complete  christmas tree is built
        if true we allocate a gift to it.Finally reset the Selected trees as 
        an empty list
        
        """
        if len(lst) == 1:
            self.pointer = lst[0]      #show the arrow, the tree was chosen     
        if len(lst) == 2:
            self.pointer = None        #  remove arrow
            sorceTree = lst[0]         
            DestiTree = lst[1]         
            matrix = self.matrix
            if matrix[sorceTree] == []:
                error_sound.play()     # if there is no layer, play sound of error
            elif matrix[DestiTree] == [] or\
            matrix[sorceTree][-1] < matrix[DestiTree][-1]: #check if it is a valid move
                layer = matrix[sorceTree].pop()
                matrix[DestiTree].append(layer)     # update the change
                if len(matrix[DestiTree]) == 3:    # the distination tree is finish
                    self.gifts[DestiTree] = 1      #show a gift
                move_sound.play()                  # play the sound of moving
            else:# not a valid move
                error_sound.play()
            lst[:] = []
    def checkWin(self):   #check whether the play finish the whole game
        global done
        if sum(self.gifts) == 3:   #while all 3 gifts are presented
            pygame.time.delay(500)
            screen.blit(winPicture,(0,0))      #show the win picture      
            pygame.display.flip()
            pygame.time.delay(1000)
            return True
        return False


forest = Forest([[0],[1],[2]]) #Create a forest


    
"""
            Helping window and Question mark and Return to home Interface function
"""   

def drawQuestion(): #place the question mark
    screen.blit(question,(width - radiusq * 2,0))
def drawtext(): #instruction for playing game
    screen.blit(helpText,(0,0))
def InTheCircle(centerx,centery,radius): # checkCheck whether the mouse is in a given circle
    left_click = pygame.mouse.get_pressed()[0]
    position = pygame.mouse.get_pos()
    if abs(position[0] -centerx)**2 + \
    abs(position[1] -centery)**2 <= \
    radius**2 and left_click:
        return True
    return False
    
def jumToHelp(): # a function to jump to the helping display
    if InTheCircle(center_xq,center_yq,radiusq): #click the question mark to present instruction
        helping()
def helping():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == pygame.K_LEFT: #press <-- to return the main game
                    return
            if event.type ==  MOUSEBUTTONDOWN: #click for return to the game
                    if InTheCircle(center_xq,center_yq,radiusq):
                        return
        bg.update() #snow
        drawQuestion() #present question mark
        drawtext() #instruction
        pygame.display.flip()
def drawHome():  # present the HOME mark
    screen.blit(home,(0,0))
def backHome(): # check if the player click home
    if InTheCircle(center_xh,center_yh,radiush): #click the circle to return
        return True
    return False

"""
                        The paly function for this game
"""
def play():
    global forest
    pygame.mixer.music.load('sound/bgm.mp3') #bgm
    pygame.mixer.music.play(-1) #loop Playback
    while True: 
        if forest.checkWin(): #if win 
            pygame.mixer.music.stop() #music stop
            forest = Forest([[0],[1],[2]]) # reset the forest
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type ==  MOUSEBUTTONDOWN: #If the mouse is pressed
                if backHome(): #if quit
                    pygame.mixer.music.stop() #music stop
                    forest = Forest([[0],[1],[2]])
                    return
                jumToHelp() #check if the user want to seek help
            if event.type == KEYDOWN:               #use keyboard to make a move 
                if len(Selected_trees) < 2:
                    if event.key == pygame.K_LEFT:  # for left tree
                        Selected_trees.append(0)
                    if event.key == pygame.K_DOWN:  # for middle tree
                        Selected_trees.append(1)
                    if event.key == pygame.K_RIGHT: # for right tree
                        Selected_trees.append(2) 
        forest.moveTree(Selected_trees)
        bg.update()    #snow        
        forest.draw()  #forest
        drawHome()     # back to main page
        drawQuestion()     # to help 
        pygame.display.flip()
        clock.tick(60)

      

