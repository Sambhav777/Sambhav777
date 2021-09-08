import pygame
import math
import random
import os
import time
print
pygame.init()
screen_width = 900
screen_height = 650
gameWindow = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PHYSCIS")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)


#colors
white = (255, 255, 255)
green = (0,225,0)
blue = (0,0,225)
sky_blue = (0,191,255)
red = (255, 0, 0)
black = (0, 0, 0)
ran = (95,195,34)

def text_screen(text,color,x,y):
    screen_text = font.render(text,True,color)
    gameWindow.blit(screen_text, [x,y])

def mod(x):
    if x >=0:
        return x;
    else:
        return -x; 

def gravity(block_y,ground_y,block_mass,ground_mass,block_inVel_y,ground_inVel_yblock_inVel_y):
    r = abs(block_y - ground_y) + 6.3781*10e6
    Fg = ((6.67408*10e-11)*(block_mass)*(ground_mass))/(r*r) #Gm1m2/r2
    block_g = Fg/block_mass# Fg = ma
    ground_g = Fg/ground_mass
    block_inVel_y = block_inVel_y + block_g
    ground_inVel_yblock_inVel_y = ground_inVel_yblock_inVel_y + ground_g
    return [block_inVel_y,ground_inVel_yblock_inVel_y,block_g];
    # a = v2 - v1/t
def friction(block_x,block_mass,block_inVel_x,block_a,block_g,u):
    f = u*block_mass*block_g  # f= umg
    if(block_inVel_x > 0):
        block_a = f/block_mass
        if(block_inVel_x - block_a>=0):
            block_inVel_x = block_inVel_x - block_a
        else:
            block_inVel_x = 0
    elif(block_inVel_x <0):
        block_a = f/block_mass
        if((-block_inVel_x) - block_a>=0):
            block_inVel_x = block_inVel_x + block_a
        else:
            block_inVel_x =0
    return block_inVel_x
    
def collision(block_mass,block_mass1,block_x,block_x1,block_y,block_y1,block_inVel_x,block_inVel_x1):
    # print(mod(block_x - block_x1))
    if(mod(block_x - block_x1) < 30 or block_x - block_x1 == 0) and mod(block_y - block_y1)<10:
        if block_inVel_x != 0:
            if(block_inVel_x == block_inVel_x1 and block_mass == block_mass1):
                block_inVel_x = 0
                block_inVel_x1 = 0
            #print(block_inVel_x,block_inVel_x1)
            temp_vel =  block_inVel_x1
            block_inVel_x1 = (((block_mass*(block_inVel_x - block_inVel_x1))+((block_mass*block_inVel_x) + (block_mass1*block_inVel_x1)))/(block_mass+block_mass1)) 
            #m0v0 + m11v11 = m02v02 + m13v13  ... m0v0 = m02v02 + m13v13
            #(m0v0+m11v11-m13v13)/m02 = v02 .... (m0v0 - m13v13)/m02 = v02
            #v13 -v02 = v0 - v11.  ----- v13 -v02 = v0 ---- v13 - m0v0/m02 - m13v13/m02 = v0 -- v13(m02-m13)/m02 = (m02v0 + m0v0)/m02 --- 
            # v13 - (-m13v13/m02 + (m0v0+m11v11)/m02) = v0 - v11
            # (v13(m02+m13))/m02 = v0 - v11 + (m0v0+m11v11)/m02
            # v13 = (m02(v0-v11) + m0v0+m11v11)/m02+m13
            # v13 = ((2m02)v0)/m02+m13
            # v02 = -v0 + v11 + v13 
            #print(block_inVel_x,block_inVel_x1)
            block_inVel_x = block_inVel_x1 + temp_vel - block_inVel_x #v-v1 = v3-v2 ... v3 + v1 -v
        elif block_inVel_x1 != 0:
            #print(block_inVel_x,block_inVel_x1)
            span_vel = block_inVel_x
            block_inVel_x = block_inVel_x1
            block_inVel_x1 = span_vel
            temp_vel =  block_inVel_x1
            block_inVel_x1 = (((block_mass*(block_inVel_x - block_inVel_x1))+((block_mass*block_inVel_x) + (block_mass1*block_inVel_x1)))/(block_mass+block_mass1)) 
            block_inVel_x = block_inVel_x1 + temp_vel - block_inVel_x
            if(block_mass1 <= 2*block_mass):
                span_vel = block_inVel_x
                block_inVel_x = block_inVel_x1
                block_inVel_x1 = span_vel
            #print(block_inVel_x,block_inVel_x1)
    return [block_inVel_x,block_inVel_x1]

def start():
    exit_game = False
    while not exit_game:
        gameWindow.fill((233,210,229))
        text_screen("DON'T TOUCH THE BORDER", red, 180, 150)
        text_screen("Press 1 For 1 Player", sky_blue, 235, 270)
        text_screen("Press 2 For 2 Players", blue, 235, 325)
        text_screen("HOW TO PLAY? [C]",green,247,385)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    multi_play = False
                    main(multi_play)
                if event.key == pygame.K_2:
                    multi_play = True
                    main(multi_play)
                if event.key == pygame.K_c:
                    exit_game = True
                    how_to_play()
                    

        pygame.display.update()
        clock.tick(60)

def how_to_play():
    exit_game = False
    while not exit_game:
        gameWindow.fill(black)
        text_screen("HOW TO PLAY", green, 300, 30)
        text_screen("1st Player Controls: Left Arrow key",red,0,75)
        text_screen("Rigth Arrow key",red,375,120)
        text_screen("Up Arrow Key/Space Bar",red,375,160)
        text_screen("2nd Player Controls: D key to move right",blue,0,200)
        text_screen("A key to move left",blue,385,240)
        text_screen("W Key to jump",blue,385,280)
        text_screen("Avoid hitting the horizontal sides to win",green,57,380)
        text_screen("Press ANY KEY TO CONTINUE",(23,98,54),150,500)
        text_screen('Made by Sambhav',sky_blue,0,600)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                start()
        pygame.display.update()
        clock.tick(60)
def gameover(winner):
    exit_game = False
    while not exit_game:
        gameWindow.fill(sky_blue)
        text_screen(winner + "Won this game!",white,150,300)
        text_screen("Press Space Bar to play again",white,150,440)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start()
        pygame.display.update()
        clock.tick(60)



def main(multi_play):
    exit_game = False
    game_over = False
    game_over1 = False
    game_overAI = False
    respawn = True
    respawn1 = True
    respawnAI = True
    #block1
    position = [15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120,125,130,135,140,145,150,155,160,165,170,175,180,185,190,195,200,205,210,215,220,225,230,235,240,245,250,255,260,265,270,275,280,285,290,295,300,305,310,315,320,325,330,335,340,345,350,355,360,365,370,375,380,385,390,395,400,405,410,415,420,425,430,435,440,445,450,455,460,465,470,475,480,485,490,495,500,505,510,515,520,525,530,535,540,545,550,555,560,565,570,575,580,585,590,595,600,605,610,615,620,625,630,635,640,645,650,655,660,665,670,675,680,685,690,695,700,705,710,715,720,725,730,735,740,745,750,755,760,765,770,775,780,785,790,795,800,805,810,815,820,825,830,835,840,845,850,855,860,865,870,875,880,885]
    block_x = random.choice(position)
    block_y = 5
    block_mass = 50
    block_g = 0
    block_a = 0
    block_inVel_y = 0
    block_inVel_x = 0
    #block2
    block_x1 = random.choice(position)
    block_y1 = 5
    block_mass1 = 50
    block_g1 = 0
    block_a1 = 0
    block_inVel_y1 = 0
    block_inVel_x1 = 0
    #AI
    ai_x1 = random.choice(position)
    ai_y1 = 5
    ai_mass1 = 50
    ai_g1 = 0
    ai_a1 = 0
    ai_inVel_y1 = 0
    ai_inVel_x1 = 0
    #ground
    ground_x = 0
    ground_y = 500
    ground_rely = 500
    ground_mass =6*10e24
    ground_g = 0
    ground_inVel_yblock_inVel_y = 0
    fps = 30

    if(not os.path.exists("win_streakP1.txt")):
                with open("win_streakP1.txt", "w") as f:
                    f.write("0")
    if(not os.path.exists("win_streakP2.txt")):
                with open("win_streakP2.txt", "w") as f:
                    f.write("0")
    if(not os.path.exists("win_streakSolo.txt")):
                with open("win_streakSolo.txt", "w") as f:
                    f.write("0")
    if(not os.path.exists("temp_score.txt")):
                with open("temp_score.txt", "w") as f:
                    f.write("0")
    with open("win_streakP1.txt", "r") as f:
        win_streakP1 = f.read()
    with open("win_streakP2.txt", "r") as f:
        win_streakP2 = f.read()
    with open("win_streakSolo.txt", "r") as f:
        win_streakSolo = f.read()
    with open("temp_score.txt", "r") as f:
        temp_score = int(f.read())
    count_down = 0 
    ct = ['3','2','1','Go']
    while count_down < 4:
        gameWindow.fill(sky_blue)
        text_screen(ct[count_down],white,450,300)
        count_down = count_down+1
        pygame.draw.rect(gameWindow,red,[block_x,block_y,20,20])
        if(multi_play == True):
            pygame.draw.rect(gameWindow,blue,[block_x1,block_y1,20,20])
        elif(multi_play == False):
            pygame.draw.rect(gameWindow,(75,23,28),[block_x1,block_y1,20,20])
        pygame.draw.rect(gameWindow,black,[ai_x1,ai_y1,20,20])
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    break
        time.sleep(1)
    while not exit_game:
        if game_over and game_over1:
            if(not multi_play):
                with open("temp_score.txt", "w") as f:
                    f.write('0')
                #temp_score = 0
            gameover('AI (Black)')
        if game_over1 and game_overAI:
            if(multi_play == True):
                with open("win_streakP1.txt", "w") as f:
                    f.write(str(int(win_streakP1) + 1))
            elif(not multi_play):
                if(temp_score>=int(win_streakSolo)):
                    with open("win_streakSolo.txt", "w") as f:
                        f.write(str(int(win_streakSolo) + 1))
                    with open("temp_score.txt", "w") as f:
                        f.write(str(temp_score+1))
                else:
                    with open("temp_score.txt", "w") as f:
                        f.write(str(temp_score+1))
                    #temp_score = temp_score+1
            gameover('Player 1 (Red)')
        if game_over and game_overAI:
            if not multi_play:
                with open("temp_score.txt", "w") as f:
                    f.write('0')
                #temp_score = 0
                gameover('AI (BROWN)')
            else:
                with open("win_streakP2.txt", "w") as f:
                    f.write(str(int(win_streakP2) + 1))
                gameover('Player 2 (Blue)')
        gameWindow.fill(sky_blue)
        if not game_over:
            g = gravity(block_y,ground_y,block_mass,ground_mass,block_inVel_y,ground_inVel_yblock_inVel_y)
            block_inVel_y = g[0]
        if not game_over1:
            g1 = gravity(block_y1,ground_y,block_mass1,ground_mass,block_inVel_y1,ground_inVel_yblock_inVel_y)
            block_inVel_y1 = g1[0]
        if not game_overAI:
            gai = gravity(ai_y1,ground_y,ai_mass1,ground_mass,ai_inVel_y1,ground_inVel_yblock_inVel_y)
            ai_inVel_y1 = gai[0]

        ground_inVel_yblock_inVel_y = g[1]
        if round(block_y) > ground_rely+42 and block_inVel_y > 0:#round(block_y) > ground_rely+42: 
            block_inVel_y = -block_inVel_y/2
            ground_inVel_yblock_inVel_y = 0
            if mod(block_inVel_y) < 10:
                if block_inVel_y < 0.5:
                    block_inVel_y = 0
                c = collision(block_mass,ground_mass,block_x,ground_x,block_y,ground_y,block_inVel_y,ground_inVel_yblock_inVel_y)
                block_inVel_y = block_inVel_y + c[0]
                ground_inVel_yblock_inVel_y = ground_inVel_yblock_inVel_y + c[1]
        if round(block_y1) > ground_rely+42 and block_inVel_y1 > 0 :#round(block_y) > ground_rely+42: 
            block_inVel_y1 = -block_inVel_y1/2
            #ground_inVel_yblock_inVel_y = 0
            if mod(block_inVel_y1) < 10:
                if block_inVel_y1 < 0.5:
                    block_inVel_y1 = 0
                c = collision(block_mass1,ground_mass,block_x1,ground_x,block_y1,ground_y,block_inVel_y1,ground_inVel_yblock_inVel_y)
                block_inVel_y1 = block_inVel_y1 + c[0]
                ground_inVel_yblock_inVel_y = ground_inVel_yblock_inVel_y + c[1]
        if round(ai_y1) > ground_rely+42 and ai_inVel_y1 > 0 :#round(block_y) > ground_rely+42: 
            ai_inVel_y1 = -ai_inVel_y1/2
            #ground_inVel_yblock_inVel_y = 0
            if mod(ai_inVel_y1) < 10:
                if ai_inVel_y1 < 0.5:
                    ai_inVel_y1 = 0
                c = collision(ai_mass1,ground_mass,ai_x1,ground_x,ai_y1,ground_y,ai_inVel_y1,ground_inVel_yblock_inVel_y)
                ai_y1 = ai_y1 + c[0]
                ground_inVel_yblock_inVel_y = ground_inVel_yblock_inVel_y + c[1]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_SPACE or event.key == pygame.K_UP) and block_y > 500:
                    block_inVel_y = block_inVel_y - 75
                if event.key == pygame.K_RIGHT and block_inVel_x < 20:
                    block_inVel_x = block_inVel_x + 25
                if event.key == pygame.K_LEFT and block_inVel_x > -20:
                    block_inVel_x = block_inVel_x - 25
                if(multi_play == True):                    
                    if event.key == pygame.K_w and block_y1 > 500:
                        block_inVel_y1 = block_inVel_y1 - 75
                    if event.key == pygame.K_d and block_inVel_x1 < 20:
                        block_inVel_x1 = block_inVel_x1 + 25
                    if event.key == pygame.K_a and block_inVel_x1 > -20:
                        block_inVel_x1 = block_inVel_x1 - 25
                if event.key == pygame.K_0:
                    main(multi_play)
        #print(block_y)

        # Non multi AI
        if(multi_play == False):
            if(mod(block_x-block_x1)>mod(ai_x1-block_x1) and not game_over) or mod(block_y-block_y1) < mod(ai_y1-block_y1):
                if block_x-block_x1 < 0:
                    if(mod(block_inVel_x1)<25):
                        block_inVel_x1 = block_inVel_x1 - 7
                if (block_x-block_x1) > 0:
                    if(mod(block_inVel_x1)<25):
                        block_inVel_x1 = block_inVel_x1 + 7
                if (block_y - block_y1) <0 and block_inVel_y !=0:
                    block_inVel_y1 = block_inVel_y1 - 10
            else:#if(mod(block_x-block_x1)< mod(ai_x1-block_x1) and not game_overAI):
                if ai_x1-block_x1 < 0:
                    if(mod(block_inVel_x1)<25):
                        block_inVel_x1 = block_inVel_x1 - 7
                if (ai_x1-block_x1) > 0:
                    if(mod(block_inVel_x1)<25):
                        block_inVel_x1 = block_inVel_x1 + 7
                if (ai_y1 - block_y1) <0 and ai_inVel_y1 !=0:
                    block_inVel_y1 = block_inVel_y1 - 10
         # AI       
        if(mod(block_x1-ai_x1)>mod(block_x-ai_x1) and not game_over):
            if block_x-ai_x1 < 0:
                if(mod(ai_inVel_x1)<25):
                    ai_inVel_x1 = ai_inVel_x1 - 5
            if (block_x-ai_x1) > 0:
                    if(mod(ai_inVel_x1)<25):
                        ai_inVel_x1 = ai_inVel_x1 + 5
            if (block_y - ai_y1) <0 and block_inVel_y !=0 :
                ai_inVel_y1 = ai_inVel_y1 - 10
                #  if block_inVel_y == 0:
                #      ai_inVel_y1 == 0
        else:#if(mod(block_x1-ai_x1)< mod(block_x-ai_x1) and not game_over1):
            if block_x1-ai_x1 < 0:
                if(mod(ai_inVel_x1)<25):
                    ai_inVel_x1 = ai_inVel_x1 - 5
            if (block_x1-ai_x1) > 0:
                    if(mod(ai_inVel_x1)<25):
                        ai_inVel_x1 = ai_inVel_x1 + 5
            if (block_y1 - ai_y1) <0 and block_inVel_y1 !=0 :
                ai_inVel_y1 = ai_inVel_y1 - 10

        if block_x1 > screen_width-5 or block_x1 < 5:
            if block_inVel_x1 <0:
                block_inVel_x1 = 10
            elif block_inVel_x1>0:
                block_inVel_x1 = -10
            else:
                block_inVel_x1 = -block_inVel_x1
        if block_x > screen_width-5 or block_x < 5:
            if block_inVel_x <0:
                block_inVel_x = 10
            elif block_inVel_x>0:
                block_inVel_x = -10
            # else:
            #     block_inVel_x = -block_inVel_x
        # if mod(block_x-screen_width) < 10:
        #     block_inVel_x = 0
        # if mod(ai_x1)-mod(screen_width) < 10:
        #     ai_inVel_x1 = 0
        

        if(block_y>=500):
            block_inVel_x = friction(block_x,block_mass,block_inVel_x,block_a,g[2],0.35)
        elif(block_y<500):
            block_inVel_x = friction(block_x,block_mass,block_inVel_x,block_a,g[2],0.021)
        if(block_y1>=500):
            block_inVel_x1 = friction(block_x1,block_mass1,block_inVel_x1,block_a1,g1[2],0.35)
        elif(block_y1<500):
            block_inVel_x1 = friction(block_x1,block_mass1,block_inVel_x1,block_a1,g1[2],0.021)
        if(ai_y1>=500):
            ai_inVel_x1 = friction(ai_x1,ai_mass1,ai_inVel_x1,ai_a1,gai[2],0.35)
        elif(ai_y1<500):
            ai_inVel_x1 = friction(ai_x1,ai_mass1,ai_inVel_x1,ai_a1,gai[2],0.021)
        if not game_over:
            c = collision(block_mass,block_mass1,block_x,block_x1,block_y,block_y1,block_inVel_x,block_inVel_x1)
            block_inVel_x = c[0]
            block_inVel_x1 = c[1]
        if not game_over:
            c = collision(block_mass,ai_mass1,block_x,ai_x1,block_y,ai_y1,block_inVel_x,ai_inVel_x1)
            block_inVel_x = c[0]
            ai_inVel_x1 = c[1]
        if not game_overAI:
            c = collision(block_mass1,ai_mass1,block_x1,ai_x1,block_y1,ai_y1,block_inVel_x1,ai_inVel_x1)
            block_inVel_x1 = c[0]
            ai_inVel_x1 = c[1]

        if block_x1 > screen_width+0 or block_x1 < 0-15 and respawn1 == True:
            block_x1 = 550
            block_y1  = 5
            block_inVel_y1 =0
            game_over1 = True
            respawn1 = False
        if block_x > screen_width+0 or block_x < 0-15 and respawn == True:
            block_x = 600
            block_y  = 5
            block_inVel_y = 0
            game_over = True
            respawn = False
        if ai_x1 > screen_width+0 or ai_x1 < 0-15 and respawnAI == True:
            ai_x1 = 600
            ai_y1  = 5
            ai_inVel_y1 = 0
            game_overAI = True
            respawnAI = False
        if(block_inVel_x1 == block_inVel_x and block_x == block_x1):
            pygame.draw.rect(gameWindow,red,[block_x,block_y,20,20])
            pygame.draw.rect(gameWindow,blue,[block_x1,block_y1,20,20])
            pygame.display.update() 
            time.sleep(0.03)
        block_y = block_y + block_inVel_y
        block_x = block_x + block_inVel_x
        block_y1 = block_y1 + block_inVel_y1
        block_x1 = block_x1 + block_inVel_x1
        ai_y1 = ai_y1 + ai_inVel_y1
        ai_x1 = ai_x1 + ai_inVel_x1
        #ground_y = ground_y + ground_inVel_yblock_inVel_y

        time.sleep(0.03)
        pygame.draw.rect(gameWindow,green,[ground_x,ground_y,screen_width,150])
        pygame.draw.rect(gameWindow,red,[block_x,block_y,20,20])
        if(multi_play == True):
            pygame.draw.rect(gameWindow,blue,[block_x1,block_y1,20,20])
        elif(multi_play == False):
            pygame.draw.rect(gameWindow,(75,23,28),[block_x1,block_y1,20,20])
        pygame.draw.rect(gameWindow,black,[ai_x1,ai_y1,20,20])
        if(not multi_play):
            text_screen("Highest Solo win streak: "+win_streakSolo,red,5,600)
        else:
            text_screen("Player 1: "+ win_streakP1,red,5,600)
            text_screen("Player 2: "+ win_streakP2,blue,500,600)
        pygame.display.update()
    clock.tick(fps)    
    pygame.quit()
    quit()

start()