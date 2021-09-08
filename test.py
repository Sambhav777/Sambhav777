import pygame
import math
import random
import os
import pyttsx3
import time
# from pygame.locals import*

engine = pyttsx3.init('sapi5')
voices= engine.getProperty('voices') #getting details of current voice
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio) 
    engine.runAndWait() 

pygame.init()
pygame.mixer.init()
screen_width = 900
screen_height = 650
gameWindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("BLOCK SNAKE WORLD")

bgimg = pygame.image.load("IDK.png")
bgimg = pygame.transform.scale(bgimg,(screen_width,screen_height)).convert_alpha()

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
ran = (95,195,34)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)
def text_screen(text,color,x,y):
    screen_text = font.render(text,True,color)
    gameWindow.blit(screen_text, [x,y])

def plot_block(gameWindow,color,snk_list,block_size_x,block_size_y):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow,color,[x,y,block_size_y,block_size_y])

def welcome():
    exit_game = False
    pygame.mixer.music.load("welcome.mp3")
    pygame.mixer.music.play()
    
    speak('WELCOME TO BLOCK SNAKES!')
    while not exit_game:
        gameWindow.fill((233,210,229))
        text_screen("Welcome to Block Snakes", black, 200, 250)
        text_screen("Press Space Bar To Play", black, 215, 290)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    gameloop()

        pygame.display.update()
        clock.tick(60)

def gameloop():
    block_x = 5
    block_y = 5
    block_size_x = 20
    block_size_y = 20 
    block_velocity_x = 0
    block_velocity_y = 0
    block_color = (0,255,0)
    fps = 30
    if(not os.path.exists("hiscore.txt")):
                with open("hiscore.txt", "w") as f:
                    f.write("0")

    with open("hiscore.txt", "r") as f:
        hiscore = f.read()

    food_x = random.randint(0,screen_width)
    food_y = random.randint(0,screen_height)
    food_size = random.randint(10,19)
    score = 0
    snk_list = []
    snk_length = 1
    exit_game = False;
    game_over = False;
    pygame.mixer.music.load('InGame.mp3')
    pygame.mixer.music.play()
    while not exit_game:
        if game_over:
            with open("hiscore.txt", "w") as f:
                f.write(str(hiscore))
            gameWindow.fill(white)
            text_screen("Game Over!", red, 345, 250)
            text_screen("Press Space Bar To Continue",red,202,290)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        gameloop()
        else:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        gameWindow.fill(white)
                        # block_x = block_x +10
                        block_velocity_x = 10
                        block_velocity_y = 0
                        pygame.display.update()
                    if event.key == pygame.K_LEFT:
                        gameWindow.fill(red)
                        # block_x = block_x - 10
                        block_velocity_x = -10
                        block_velocity_y = 0
                        pygame.display.update()
                    if event.key == pygame.K_UP:
                        gameWindow.fill(black)
                        # block_y = block_y - 10
                        block_velocity_y = -10
                        block_velocity_x = 0
                        pygame.display.update()
                    if event.key == pygame.K_DOWN:
                        gameWindow.fill(ran)
                        # block_y = block_y + 10
                        block_velocity_x = 0
                        block_velocity_y = 10
                        pygame.display.update()

            block_x = block_x + block_velocity_x
            block_y = block_y + block_velocity_y

            if abs(block_x - food_x)<6 and abs(block_y - food_y)<6:
                score = score +10
                print(score)
                block_size_x = block_size_x + food_size
                # block_size_y = block_size_y + food_size
                food_x = random.randint(0,screen_width-20)
                food_y = random.randint(0,screen_height-20)
                food_size = random.randint(10,19)
                snk_length +=5
                if score>int(hiscore):
                    hiscore = score


            gameWindow.fill(random.choice(black))#[white,black,ran,red]
            text_screen("Score: " + str(score),ran, 5, 5)
            text_screen("High Score:" + str(hiscore),ran,screen_width-280,5)
            #pygame.draw.rect(gameWindow,block_color,[block_x,block_y,block_size_x,block_size_y]) #[x location,y location, lendth x,width x]
            pygame.draw.rect(gameWindow,red,[food_x,food_y,food_size,food_size])

            head = []
            head.append(block_x)
            head.append(block_y)
            snk_list.append(head)
            if len(snk_list)>snk_length:
                del snk_list[0]
            
            if len(snk_list)>snk_length:
                    del snk_list[0]

            if head in snk_list[:-1]:
                    game_over = True
                    pygame.mixer.music.load('gameover.mp3')
                    pygame.mixer.music.play()
                    speak('HaHa LOSER!')

            if block_x<0 or block_x>screen_width or block_y<0 or block_y>screen_height:
                    game_over = True
                    pygame.mixer.music.load('gameover.mp3')
                    pygame.mixer.music.play()
                    speak('TRY AGAIN?')
            plot_block(gameWindow, block_color, snk_list, block_size_x,block_size_y)
        pygame.display.update()
        clock.tick(fps)        

    pygame.quit()
    quit()
welcome()