import pygame, sys
from pygame.locals import *
from PIL import Image
import numpy as np
import os
import math


def main():
    frameCount = 0
    
    WINDOWWIDTH = 640
    WINDOWHEIGHT = 480
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    fpsClock = pygame.time.Clock()
    font = pygame.font.Font(None,32)
    fontSmall = pygame.font.Font(None,24)
    
    k_box = pygame.Rect(40,WINDOWHEIGHT-56, 140,32)
    pygame.display.set_caption('Image Compression')
    BLUE  = (  0,   0, 255)
    WHITE = (255, 255, 255)
    BLACK = (0,0,0)
    color_writing = pygame.Color('blue3')
    color_notWrit = pygame.Color('dodgerblue2')
    box_color = color_notWrit
    
    DISPLAYSURF.fill(WHITE)
    icon = pygame.image.load("icon.png")
    pygame.display.set_icon(icon)
    text = ""
    writing = False
    backspacing = False
    k_value = -1
    formatImage("dog.png") #reformat for consistent image compression comparision
    comp_img = pygame.image.load("dog.png")
    comp_img = pygame.transform.scale(comp_img, (WINDOWWIDTH, WINDOWHEIGHT-84))
    
    while True: # main game loop
        for event in pygame.event.get():
            
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                #if they click in the box
                if k_box.collidepoint(event.pos):
                    writing = not writing
                else:
                    writing = False
                #let them know they're typing
                if writing:
                    box_color = color_writing
                else:
                    box_color = color_notWrit

            if event.type == pygame.KEYDOWN:
                if writing:
                    if event.key == pygame.K_RETURN:
                        #print(text) execut svd compression update
                        try:
                            k = int(text)
                            #print(k)
                            if k < 1:
                                raise Exception("Invalid Input")
                            lineSingularValue(k, 40)
                            comp_img = pygame.image.load("current_k.png")
                            comp_img = pygame.transform.scale(comp_img, (WINDOWWIDTH, WINDOWHEIGHT-84)) 
                        except:
                            print("K-value must be an integer greater than 0")
                            #text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                        backspacing = True
                    else:
                        text += event.unicode
                        
        DISPLAYSURF.fill(WHITE)
        #draw text
        enter_n = font.render("n:", True, pygame.Color("dodgerblue2"))
        
        side_output_1 = fontSmall.render("Original Size:" + str(), True, pygame.Color("dodgerblue2"))
        side_output_2 = fontSmall.render("New Size:", True, pygame.Color("dodgerblue2"))
        side_output_3 = fontSmall.render("Compression Percent:", True, pygame.Color("dodgerblue2"))
        
        out_values = getFileSizes()
        resultArr = []
        
        for i in range(3):
            resultArr.append(fontSmall.render(out_values[i], True, pygame.Color("dodgerblue2")))
        
        
        text_surface = font.render(text, True, box_color)
        #check if box is correct size
        box_width = max(200, text_surface.get_width() + 10)
        k_box.w = box_width
        #blit text onto the screen 
        DISPLAYSURF.blit(text_surface, (k_box.x+5, k_box.y+5))
        DISPLAYSURF.blit(enter_n, (10, WINDOWHEIGHT-52))
        DISPLAYSURF.blit(side_output_1, (WINDOWWIDTH - 300, WINDOWHEIGHT-70))
        DISPLAYSURF.blit(side_output_2, (WINDOWWIDTH - 300, WINDOWHEIGHT-50))
        DISPLAYSURF.blit(side_output_3, (WINDOWWIDTH - 300, WINDOWHEIGHT-30))  
        for i in range(3):
            DISPLAYSURF.blit(resultArr[i], (WINDOWWIDTH - 100, WINDOWHEIGHT - ((20*(i+1)) + 10)))
        #dipslay svd compression onto the screen
        DISPLAYSURF.blit(comp_img, (0,0))
        #draw box
        pygame.draw.rect(DISPLAYSURF, box_color, k_box, 2)
        
        #pygame.display.flip()
        pygame.display.update()
        frameCount = frameCount + 1
        fpsClock.tick(60)


def singularValue(k_value):
    picture = Image.open("dog.png").convert('L') #get image
    arr_pic = np.array(picture) #numpy array of pixel values
    print(arr_pic)
    u,s,v = np.linalg.svd(arr_pic, full_matrices=False)
    k = k_value  
    arr_pic = np.matrix(u[:,:k]) * np.diag(s[:k]) * np.matrix(v[:k, :]) 

    img = Image.fromarray(arr_pic).convert('RGB') #convert back to image
    img.save("current_k.png")
    
def blockSingularValue(k_value, blocks):
    picture = Image.open("dog.png").convert('L') #get image
    arr_pic = np.array(picture) #numpy array of pixel values
    original = arr_pic
    k = k_value  
    #print(arr_pic)
    block_length = int((len(arr_pic) / blocks))
    piece = []
    full = [[]]
    for i in range(blocks):
        piece = []
        for j in range(blocks):
            block_height = int((len(arr_pic[i]) / blocks))
            section = arr_pic[ i*block_length : (i+1)*block_length , j *block_height : (j+1)*block_height ]
            try:
                u,s,v = np.linalg.svd(section, full_matrices=False)
                svd = np.matrix(u[:,:k]) * np.diag(s[:k]) * np.matrix(v[:k, :])
            except:
                print("Error")
            
            piece = vertPlus(piece, svd, i)
        
        full = horiPlus(full, piece, j)
        
    arr_pic = full

    img = Image.fromarray(arr_pic).convert('RGB') #convert back to image
    img.save("current_k.png")    
    
def lineSingularValue(k_value, blocks):
    picture = Image.open("dog.png").convert('L') #get image
    arr_pic = np.array(picture) #numpy array of pixel values
    original = arr_pic
    k = k_value  
    #print(arr_pic)
    piece = [[]]
    block_length = int((len(arr_pic) / blocks))
    for i in range(blocks):
        
        section = arr_pic[ i*block_length : (i+1)*block_length]
        
        try:
            u,s,v = np.linalg.svd(section, full_matrices=False)
            svd = np.matrix(u[:,:k]) * np.diag(s[:k]) * np.matrix(v[:k, :])
        except:
            print("Error")
        piece = horiPlus(piece, svd, i)
    arr_pic = piece

    img = Image.fromarray(arr_pic).convert('RGB') #convert back to image
    img.save("current_k.png")  
    
def getFileSizes():
    cur_path = "./"
    dogSize = int(os.path.getsize(cur_path + "dog.png")/1000)

    try:
        newSize = os.path.getsize(cur_path + "current_k.png")
    except: #file was not found
        newSize = dogSize
    newSize = int(newSize/1000)
    if newSize > dogSize:
        newSize = dogSize
    percent = int((100* newSize / dogSize)) 
    return str(percent), str(newSize), str(dogSize)

def formatImage(image):
    picture = Image.open(image).convert('L') #get image
    arr_pic = np.array(picture) #numpy array of pixel values
    img = Image.fromarray(arr_pic).convert('RGB') #convert back to image
    img.save("dog.png")
    
def horiPlus(first, second,i):
    first = np.array(first)
    second = np.array(second)
    #print(first.shape)
    #print(second.shape)
    if first.shape != (0,0) and first.shape[1] == second.shape[1]:
        first = np.row_stack((first,second))
    else:
        first = second
    return first

def vertPlus(first, second, j):
    first = np.array(first)
    second = np.array(second)
    #print(second)
    #print(str(len(first[0])) + "   " + str(len(second[0])))
    if first.shape != (0,0) and first.shape[0] == second.shape[0]:
        first = np.column_stack((first,second))
    else:
        first = second
    return first

if __name__ == '__main__':    
    pygame.init()
    main()
    pygame.quit()
    