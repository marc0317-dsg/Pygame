"""
@author: Jue Chen AND Yuqi Wu

"""

"""
Please refer to the picture on the right, 
click the block to switch positions with the blank block , 
when all the blocks are put back to the same position as 
the picture on the right, you will win!
"""
#Import packages
import pygame
import random

pygame.init()

# initialization

hight = 600
width = 800
screen = pygame.display.set_mode((width, hight))# window size

# load image

big_i = pygame.image.load('images/big.jpg')
small_i= pygame.image.load('images/small.jpg')
win_i = pygame.image.load('images/win1.jpg')
question_i = pygame.image.load('images/help.jpg') 
gohome_i = pygame.image.load('images/gohome.jpg')
key_i = pygame.image.load('images/howtoplay.jpg')
back_i =pygame.image.load('images/back.jpg')

# load music

sound = pygame.mixer.Sound('sound/sound.mp3')
pygame.mixer.music.load('sound/bg.mp3')
error1 = pygame.mixer.Sound('sound/error1.mp3')

# game image and win image

G_img = [[0, 1, 2],
         [3, 4, 5],
         [6, 7, 8]]

W_img = [[0, 1, 2],
         [3, 4, 5],
         [6, 7, 8]]



# chang position

def cp(y, x, img) :   
    # switch the line
    if y - 1 >= 0 and img[y - 1][x] == 8 :
        img[y][x], img[y - 1][x] = img[y - 1][x], img[y][x]
        #sound.play()
        return True
    elif y + 1 <= 2 and img[y + 1][x] == 8 :
        img[y][x], img[y + 1][x] = img[y + 1][x], img[y][x]
        #sound.play()
        return True
    # switch the colum
    elif x - 1 >= 0 and img[y][x - 1] == 8 :
        img[y][x], img[y][x - 1] = img[y][x - 1], img[y][x]
        #sound.play()
        return True
    elif x + 1 <= 2 and img[y][x + 1] == 8 :
        img[y][x], img[y][x + 1] = img[y][x + 1], img[y][x]
        #sound.play()
        return True






# random image

def randimg(img) :    
    for i in range(1000) :
        x = random.randint(0, 2)
        y = random.randint(0, 2)
        cp(y, x, img)

# show text       

def show(text) :    
    font = pygame.font.Font(pygame.font.get_default_font(), 20)# load font   
    surface =  font.render(text, False, (255,0,0))# draw text 
    screen.blit(surface, (650, 20))# show text
    
# show help

def tohelp() :    
    screen.blit(key_i,(0,0))# show "how to play"
    screen.blit(back_i,(100,500))# show "back"
    sound.stop()# stop music


# set display

def setting() :   
    screen.fill((255, 255, 255))# set background color   
    show(f"steps = {steps}")# show text   
    screen.blit(gohome_i, (650, 100))# show "home" 
    screen.blit(question_i, (650, 250))# show "?"

    # draw image
    for y in range(3) :
        for x in range(3) :
            i = G_img[y][x]
            if i == 8:  # do not need to draw G_img[y][x]=8
                continue
            dx = (i % 3) * 199  # calculate the drawing offset
            dy = (int(i / 3)) * 199
            screen.blit(big_i, (x * 199, y * 199), (dx, dy, 199, 199))

    
    screen.blit(small_i, (600, 400))# draw reference image
    
    pygame.display.flip()# update the surface


randimg(G_img)# random game image    

# main game

def play() :
    global steps
    steps = 0  # account steps
    pygame.mixer.music.load('sound/bg.mp3')
    pygame.mixer.music.play(-1, 0.0, 0)# play background music
    while True :
                
        pygame.time.delay(32)# delay 32ms
        setting()
        
        for event in pygame.event.get() :      
            if event.type == pygame.QUIT :# window closing event
                quit()
                #pygame.quit()
                #exit()
                
            elif event.type == pygame.MOUSEBUTTONDOWN :  # mouse click event
                if pygame.mouse.get_pressed() == (1, 0, 0) :  # press the left mouse button
                    #sound.play()
                    mx, my = pygame.mouse.get_pos()  # gets the current mouse coordinates
                    if mx < 597 and my < 597 :  # check whether the mouse is in the operating range
                        x = int(mx / 199)  # calculate which block the mouse clicked on
                        y = int(my / 199) 
                        if G_img[y][x] != 8 :
                            #sound.play()
                            if cp(y, x, G_img) == 1:# change position of block
                                steps += 1# account steps
                                sound.play()
                            elif cp(y, x, G_img) != 1:
                                error1.play()


                            
                        if G_img == W_img :  # determine win
                            screen.blit(win_i, (0, 0))# show win
                            pygame.display.flip()# update the surface
                            pygame.time.delay(1000)# delay 1000ms                            
                            randimg(G_img)# random image again
                            pygame.mixer.music.stop()# stop music
                            return True# return homepage

                    elif mx > 650 and mx < 750 :# return homepage
                        if my > 100 and my < 200 :
                            randimg(G_img)# random image again
                            pygame.mixer.music.stop()# stop music
                            return True# return homepage
                                        
                        elif my > 250 and my < 350 :# to help page

                            tohelp()
                            pygame.display.flip()
                            while True:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:  # window closing event
                                        #pygame.quit()
                                        quit()
                                    elif event.type == pygame.MOUSEBUTTONDOWN:  # mouse click event
                                        if pygame.mouse.get_pressed() == (1, 0, 0):  # press the left mouse button
                                            #sound.play()
                                            mx, my = pygame.mouse.get_pos()  # gets the current mouse coordinates
                                            if mx > 100 and mx < 200:  # back to play
                                                if my > 500 and my < 550:
                                                    play()
                                                    #pygame.mixer.music.play(-1, 0.0, 0)

                                                return











