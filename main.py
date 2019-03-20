import pygame
from pygame.locals import *
from pygame import *
import sys
import time
from random import randint
import pandas as pd
import csv
import grovepi
from grovepi import*
from grove_rgb_lcd import *

# Setting
pygame.init()

surface = pygame.display.get_surface()
SCREEN_WIDTH_Complete,SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h 
screen = pygame.display.set_mode((SCREEN_WIDTH_Complete, SCREEN_HEIGHT), FULLSCREEN)  # , FULLSCREEN
SCREEN_WIDTH = SCREEN_WIDTH_Complete - (SCREEN_WIDTH_Complete * 15 / 80)
pygame.display.set_caption('Berry Buster')
pygame.mouse.set_visible(False)                     # sets mouse to not visible
clock = pygame.time.Clock()

# global variables 
panel_width = int(SCREEN_WIDTH  * 0.1111)
panel_x = 0
tong_width = int(SCREEN_WIDTH * 0.15385)
panel_range_max = SCREEN_WIDTH - tong_width
panel_y = SCREEN_HEIGHT * 5.05 / 6
panel_half_width = panel_width / 2
panel_height = SCREEN_HEIGHT * 1 / 60
panel_vel = 30
n_text = 0                                     
change_time1 = 5
mold_time = 10
end_time = 75

# main colors
PANEL_COLOR = (40, 30, 10)
BACK_COLOR = (90, 150, 70)
BALL_COLOR = (255, 0, 0)

# most used fonts - specifications
pygame.font.init()  # you have to call this at the start,
myfont = pygame.font.SysFont('Lobster Two', int(3*SCREEN_WIDTH/80))

# scores - positions
scorex = int(SCREEN_WIDTH_Complete * (7.2 / 8))
scorey = (int(SCREEN_HEIGHT - (SCREEN_HEIGHT * 0.75)))
score_pos = (scorex,scorey)
mold_score_pos = (SCREEN_WIDTH_Complete * (7.2 / 8), (SCREEN_HEIGHT - int(SCREEN_HEIGHT * 0.4333)))

# Raspberry Images
rasperry_image = pygame.image.load("image/00 rasperry.png").convert()
transColor = rasperry_image.get_at((0, 0))
rasperry_image.set_colorkey(transColor)
rasperry_image = pygame.transform.scale(rasperry_image, (int(SCREEN_WIDTH * 0.06923), int(SCREEN_WIDTH * 0.06923)))

rasperry_image_2 = pygame.image.load("image/02 rasperry.png").convert()
transColor = rasperry_image_2.get_at((0, 0))
rasperry_image_2.set_colorkey(transColor)
rasperry_image_2 = pygame.transform.scale(rasperry_image_2, (int(SCREEN_WIDTH * 0.06923), int(SCREEN_WIDTH * 0.06923)))

rasperry_image_4 = pygame.image.load("image/04 rasperry_gammel.png").convert()
transColor = rasperry_image_4.get_at((0, 0))
rasperry_image_4.set_colorkey(transColor)
rasperry_image_4 = pygame.transform.scale(rasperry_image_4, (int(SCREEN_WIDTH * 0.06923), int(SCREEN_WIDTH * 0.06923)))


# sensor
light_sensor = 2
light_list =[]
rot_sensor = 0
rot_sensor2 = 0
bew = 8

# led - port specifications
led_green = 4
led_blue = 7
led_red = 3
led = 2  # set light string on on default
digitalWrite(led, 1)

# music - used song list
index = ["music/maingame.mp3", "music/credits.mp3",
         "music/menu.mp3", "music/deathsound.mp3"]

# music function
def nextsong(nr):
    global index
    pygame.mixer.music.load(index[nr])
    pygame.mixer.music.play(-1)     # loops song 


# starts  main song when game is opend
nextsong(2)



# distance function - used for collision check for two circles
def distance(x1, y1, x2, y2):
    dx = x1 - x2
    dy = y1 - y2
    if (dx ** 2 + dy ** 2) <= 0:
        return 0
    else:
        return abs(dx ** 2 + dy ** 2) ** (1 / 2)



# restart after dying
def restart(current_score, restart_text):
    score(current_score)

    re_image = pygame.image.load("image/Restart.png").convert()  # Load Restart background
    re_image = pygame.transform.scale(re_image, (SCREEN_WIDTH_Complete, SCREEN_HEIGHT))  # Transform image to fit in screen
    screen.blit(re_image, [0, 0])  # Draw image

    restart2 = pygame.image.load("image/Restart2.png").convert()
    transColor = restart2.get_at((0, 0))
    restart2.set_colorkey(transColor)
    restart2 = pygame.transform.scale(restart2, (int(SCREEN_WIDTH_Complete*0.275), int(SCREEN_HEIGHT*0.333)))

    restart3 = pygame.image.load("image/Restart3.png").convert()
    transColor = restart3.get_at((0, 0))
    restart3.set_colorkey(transColor)
    restart3 = pygame.transform.scale(restart3, (int(SCREEN_WIDTH_Complete*0.275), int(SCREEN_HEIGHT*0.333)))

    restart2_2 = pygame.transform.flip(restart2, True, False)

    restart3_2 = pygame.transform.flip(restart3, True, False)

    restart_grave = pygame.image.load("image/Restart_grave.png").convert()
    transColor = restart_grave.get_at((0, 0))
    restart_grave.set_colorkey(transColor)
    restart_grave = pygame.transform.scale(restart_grave, (SCREEN_WIDTH_Complete, SCREEN_HEIGHT))

    ghost_y = SCREEN_HEIGHT*1/6
    x_count = SCREEN_WIDTH_Complete*0.6875
    y_count = 0

    list_ghost = [restart2, restart3]
    list_ghost2 = [restart2_2, restart3_2]
    ghost = 0
    ghost2 = 0

    while True:
        mselapsed = clock.tick(100)
        if x_count == SCREEN_WIDTH_Complete*0.6875:
            switch = True
        if x_count == -(SCREEN_WIDTH_Complete*0.0125):
            switch = False

        if switch == True:
            x_count -= 4
        if switch == False:
            x_count += 4

        if x_count < -(SCREEN_WIDTH_Complete*0.275):
            x_count = SCREEN_WIDTH_Complete + (SCREEN_WIDTH_Complete*0.03125)

        y_count = SCREEN_HEIGHT*0.167

        if x_count % (SCREEN_WIDTH_Complete*0.0125) == 0:
            if ghost == 0:
                ghost = 1
            elif ghost == 1:
                ghost = 0

        if x_count % (SCREEN_WIDTH_Complete*0.0125) == 0:
            if ghost2 == 0:
                ghost2 = 1
            elif ghost2 == 1:
                ghost2 = 0

        screen.blit(re_image, [0, 0])                           # draw background

        if switch == True:
            screen.blit(list_ghost[ghost], [x_count, y_count])      # draw ghost berry
            screen.blit(restart_grave, [0, 0])                      # draw grave over berry
        if switch == False:
            screen.blit(restart_grave, [0, 0])                    # draw grave under berry
            screen.blit(list_ghost2[ghost2], [x_count, y_count])  # draw ghost berry


        text = myfont.render(restart_text, False, (50, 50, 50)) # draw text
        screen.blit(text, (SCREEN_WIDTH_Complete*0.35, SCREEN_HEIGHT*0.483))
        score_text = "Score: " + str(current_score)
        text = myfont.render(score_text, False, (50, 50, 50))  # draw text
        screen.blit(text, (SCREEN_WIDTH_Complete*0.37, SCREEN_HEIGHT*0.567))

        # Update frames each run through
        pygame.display.update()

       # Quit game if x sign or esc is pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                digitalWrite(led, 0)
                pygame.quit()
                exit(0)
            if event.type == KEYDOWN:
                if event.key == K_KP1:
                    digitalWrite(led, 0)
                    exit()
            if event.type == KEYDOWN:
                if event.key == K_KP0:
                    digitalWrite(led, 0)
                    exit()
                if event.key == K_KP4:
                    nextsong(2)
                    menu()



# Defines how the panel moves: horizontal movement by pressed keys
def panel_move(pw):
    global panel_x
    global panel_y

    key = pygame.key.get_pressed()
    if key[K_BACKSPACE]:                         # marked as right arrow
        if panel_x + pw < SCREEN_WIDTH:
            panel_x += panel_vel
    if key[K_KP_PLUS]:                           # marked as left arrow
        if panel_x >= 0:
            panel_x -= panel_vel



# Defines how panel moves in game with distance sensor
listultra = [] 
def panel_move_two():
    global panel_x
    global panel_y
    global bew
    global panel_range_max
    global listultra

    if len(listultra) > 4:    
        if abs(ultrasonicRead(bew) - average) <= 10: # if sensorvalue is unreasonable -> ignore             
            listultra.append(ultrasonicRead(bew))
        average = listultra[0] + listultra[-1] + listultra[-2] + listultra[-2] + listultra[-3] 
        average = average/5                         # averages last inputs for smoother movement and less distortions
    else:
        average = (ultrasonicRead(bew))

    # translates hand position into tounge position
    if panel_x <= panel_range_max:
        panel_x = (panel_range_max * (average-2) ) /30
    if panel_x >= panel_range_max:
        panel_x = panel_range_max
    
    
    
# defines features and methods for the ball used
class Ball:
    def __init__(self, vel_y, rad=10.0, pos_x=150.0, pos_y=150.0, diam=20.0, vel_x=0.0):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.diam = diam
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.rad = rad
        self.vel = (vel_x ** 2 + vel_y ** 2) ** (1 / 2)

    def move(self, panel_x, panel_y,panel_width):
    # Define Ball movement
        global SCREEN_WIDTH; global SCREEN_HEIGHT
        global light_sensor

    # right limitation
        if (self.pos_x + self.rad  >= SCREEN_WIDTH):
            self.vel_x = - self.vel_x   # Richtungswechsel: VZ pos_x

    # left limitation
        if self.pos_x - self.rad <= 0:
            self.vel_x = - self.vel_x

    # top limitation
        if self.pos_y - self.rad <= 0:
            self.vel_y = - self.vel_y

    # Panel Collision
        if panel_y + self.vel_y >= self.pos_y + self.rad >= panel_y:
            if panel_x <= self.pos_x <= panel_x + panel_width:
                x_faktor = 8 * ((self.pos_x - panel_x - (panel_width/2)) / panel_width)
                self.vel_x = self.vel_x + x_faktor
                res_vel = (self.vel_x**2 + self.vel_y**2)**(1/2)
                vel_ratio = res_vel/ self.vel
                self.vel_x = self.vel_x / vel_ratio
                self.vel_y = -(self.vel_y / vel_ratio)
                
    # panel edge: artificial hitbox optimization at the edges for user satisfaction
        if panel_y + panel_height + self.vel_y + (SCREEN_HEIGHT*0.0333) >= self.pos_y + self.rad >= panel_y:
            if panel_x - (SCREEN_WIDTH*0.0125) <= self.pos_x <= panel_x:
                if self.vel_x > 0:
                    self.vel_x = -self.vel_x
                    self.vel_y = -self.vel_y
                else:
                    self.vel_x = self.vel_x
                    self.vel_y = -self.vel_y
            if panel_x + panel_width <= self.pos_x <= panel_x + panel_width + (SCREEN_WIDTH*0.0125) :
                if self.vel_x > 0:
                    self.vel_x = self.vel_x
                    self.vel_y = -self.vel_y
                else:
                    self.vel_x = self.vel_x
                    self.vel_y = -self.vel_y

    # Brick Collision
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y
        
    # rebound: explained in detail in the project doucmentation
    def rebound(self, p1x, p1y, x, y, lastx, lasty, irad, counter):  # rebound: ball from raspberries
        hx = (x + lastx) / 2
        hy = (y + lasty) / 2
        counter += 1
        # adjusting the collision position of the ball (due to overlapping velocities)
        if counter <= 700:        
            if distance(p1x, p1y, hx, hy) <= irad + self.rad - 5:
                self.rebound(p1x, p1y, x, y, hx, hy, irad, counter)
            elif distance(p1x, p1y, hx, hy) >= irad + self.rad + 5:
                self.rebound(p1x, p1y, hx, hy, lastx, lasty, irad, counter)
            # if it's near the ideal -> calculate the new vel.x and ve.y
            else:
                ortsvektor_x = p1x - hx
                ortsvektor_y = p1y - hy
                if (-p1x * (p1x - hx) + hx * (p1x - hx) - p1y * (p1y - hy) + hy * (p1y - hy)) != 0:
                    t_berechnet = ((p1x ** 2) + p1x * lastx - p1x * hx + lastx * hx + (
                                p1y ** 2) + p1y * lasty - p1y * hy + lastx * hy) / (
                                              -p1x * (p1x - hx) + hx * (p1x - hx) - p1y * (p1y - hy) + hy * (p1y - hy))
                else:
                    t_berechnet = 0
                lot_berechnet_x = hx + t_berechnet * ortsvektor_x
                lot_berechnet_y = hy + t_berechnet * ortsvektor_y
                newx = (lot_berechnet_x - lastx) + lot_berechnet_x
                newy = (lot_berechnet_y - lasty) + lot_berechnet_y
                vel_x_part = newx - hx
                vel_y_part = newy - hy
                if abs((vel_x_part ** 2 + vel_y_part ** 2)) <= 0:
                    res_vel = 0
                else:
                    res_vel = abs((vel_x_part ** 2 + vel_y_part ** 2)) ** (1 / 2)
                vel_ratio = res_vel / self.vel
                if vel_ratio != 0:
                    self.vel_x = vel_x_part / vel_ratio
                    self.vel_y = vel_y_part / vel_ratio
                else:
                    self.vel_x = -self.vel_x
                    self.vel_y = -self.vel_y
        else:
            ortsvektor_x = p1x - hx
            ortsvektor_y = p1y - hy
            if (-p1x * (p1x - hx) + hx * (p1x - hx) - p1y * (p1y - hy) + hy * (p1y - hy)) != 0:
                t_berechnet = ((p1x ** 2) + p1x * lastx - p1x * hx + lastx * hx + (
                            p1y ** 2) + p1y * lasty - p1y * hy + lastx * hy) / (
                                          -p1x * (p1x - hx) + hx * (p1x - hx) - p1y * (p1y - hy) + hy * (p1y - hy))
            else:
                t_berechnet = 0
            lot_berechnet_x = hx + t_berechnet * ortsvektor_x
            lot_berechnet_y = hy + t_berechnet * ortsvektor_y
            newx = (lot_berechnet_x - lastx) + lot_berechnet_x
            newy = (lot_berechnet_y - lasty) + lot_berechnet_y
            vel_x_part = newx - hx
            vel_y_part = newy - hy
            if abs((vel_x_part ** 2 + vel_y_part ** 2)) <= 0:
                res_vel = 0
            else:
                res_vel = abs((vel_x_part ** 2 + vel_y_part ** 2)) ** (1 / 2)
            vel_ratio = res_vel / self.vel
            if vel_ratio != 0:
                self.vel_x = vel_x_part / vel_ratio
                self.vel_y = vel_y_part / vel_ratio
            else:
                self.vel_x = self.vel_x
                self.vel_y = self.vel_y
    
    def light(self, light_sens):
    # Light Bulk
        if ((9/16) * SCREEN_HEIGHT) + (SCREEN_HEIGHT*0.0166) >= self.pos_y + self.rad >= (9/16) * SCREEN_HEIGHT:
            balk_width= (light_sens*SCREEN_WIDTH)/800                # from above
            if self.pos_x >= SCREEN_WIDTH-balk_width/2 or self.pos_x <= balk_width/2:
                self.vel_y = - self.vel_y
                
    def radius(self):
    # Defines radius in stage 3 mode t
        global rot_sensor2
        rot = round((analogRead(rot_sensor2)),0)
        self.diam = (rot*16/1023)+(SCREEN_WIDTH*2/325)                  # rescales into game display size
        if rot > 1023:
            self.diam = int(SCREEN_WIDTH*0.01538)
        self.rad = self.diam/2
	
    
    
# Gamemode S: bars in first phase controlled by light sensor
def light_sensoring():
    global light_sensor
    if len(light_list) > 4:
        if abs(analogRead(light_sensor) - light_sens) <= 10:
            light_list.append(analogRead(light_sensor))
        light_sens = light_list[0] + light_list[-1] + light_list[-2] + light_list[-2] + light_list[-3] 
        light_sens = light_sens/5 
    else:         
        light_sens = analogRead(light_sensor) 
    balk_width= (light_sens*SCREEN_WIDTH)/800                           # 800 => max(light_sensor)
    pygame.draw.rect(screen, (245,245,245), (SCREEN_WIDTH-balk_width/2, (9/16) * SCREEN_HEIGHT, balk_width/2, (SCREEN_HEIGHT*0.0166)), 0)
    pygame.draw.rect(screen, (245,245,245), (0, (9/16) * SCREEN_HEIGHT, balk_width/2, (SCREEN_HEIGHT*0.0166)), 0)
    return light_sens


# defines features of all Raspberries
class Rasperry:

    def __init__(self, pos_x, pos_y, rad):     # use: create random positioned berries in starting_phase
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rad = rad
        self.fall = False

    def r_fall(self):
        self.pos_y += 20                        # after collion, raspberries move down +5p per frame



# Defines starting conditions for gamemode 1/s
def starting_phase(score_start, mold_score_start):
    list_rasp = []                                          # empty list: gets berries assigned
    list_pos_rasp = []                                      # empty list: gets berry positions assigned
    b1 = Ball(-20.0)                                         # create object b1 (ball) with velocity -6 (moves up)

    # Create Raspberries
    for i in range(0, 30):                                  # Create about 30 berries
        x = randint(1, 10)                                  # 10 possible columns/x-values
        y = randint(1, 4)                                   # 4 possibles rows/y-values
        if (x, y) not in list_pos_rasp:                     # checks if berry with such values exists before list assignment
            list_pos_rasp.append((x, y))                    # result: there are max 30 berries, min 1 berry
            list_rasp.append(Rasperry(x * int(SCREEN_WIDTH*0.0923), (SCREEN_HEIGHT*0.033) + y * int(SCREEN_WIDTH*0.0923), (SCREEN_WIDTH * 0.036)))

    # Load and transform images
    # Background green
    bg_image = pygame.image.load("image/background green score.png").convert()
    bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH_Complete, SCREEN_HEIGHT))

    # Foreground face
    fg_image = pygame.image.load("image/Background face only.png").convert()
    transColor = fg_image.get_at((0, 0))
    fg_image.set_colorkey(transColor)
    fg_image = pygame.transform.scale(fg_image, (SCREEN_WIDTH_Complete, SCREEN_HEIGHT))
    
    # Tongue
    to_image = pygame.image.load("image/Zunge.png").convert()
    to_image.set_colorkey(transColor)
    to_image = pygame.transform.scale(to_image, (tong_width, int(tong_width*0.9)))

    # Rasperry
    global rasperry_image                                   # get already defined raspberry image -> alternative to above way
    global panel_width
    pw = panel_width                                        # reassign to pw, for special width (phase 2)


    while True:
        msElapsed = clock.tick(60)                         # set frames per second and save them
        screen.blit(bg_image, [0, 0])                       # blit main image on screen

        # Draw Raspberries
        for i in list_rasp:
            # pygame.draw.circle(screen, BALL_COLOR, (i.pos_x, i.pos_y), i.rad)
            screen.blit(rasperry_image, [i.pos_x - (SCREEN_WIDTH * 0.03846), i.pos_y - (SCREEN_HEIGHT*0.05)])

        # Panel and Ball
        panel_move(pw)                                      # lets user move the panel by above defined function
        screen.blit(to_image, [panel_x-(SCREEN_WIDTH*0.0077), panel_y-(SCREEN_HEIGHT*0.00833)])       # blits tongue on screen, with slightly adjusted values (optic)    
        b1.pos_x = panel_x + panel_half_width               # defines ball position in starting phase (center of panel)
        b1.pos_y = panel_y - 2 * b1.rad
        pygame.draw.circle(screen, BALL_COLOR, (int(b1.pos_x), int(b1.pos_y)), int(b1.diam))

        # Draw Mouth
        screen.blit(fg_image, [0, 0])                       # draw mouth now, as it will be drawn over the already blitted images

        # Write score
        score = myfont.render(str(score_start), False, (200, 60, 100))              # define/blit score
        screen.blit(score, score_pos)
        mold_score = myfont.render(str(mold_score_start), False, (80, 155, 220))    # define/blit mold score
        screen.blit(mold_score, mold_score_pos)

        # allows game start
        key = pygame.key.get_pressed()                      # if Enter (named TAB) gets pressed, main_game one/s starts
        if key[K_KP_ENTER]: # marked as tab
            main_game(b1, list_rasp, rasperry_image, score_start, mold_score_start)

        pygame.display.update()                             # updates screen, sothat everything is visible

        # controls events
        for event in pygame.event.get():                    # pygame event: checks if user e.g. quits by ESC
            if event.type == pygame.QUIT:
                digitalWrite(led, 0)
                pygame.quit()
                exit(0)
            if event.type == KEYDOWN:
                if event.key == K_KP1:
                    digitalWrite(led, 0)
                    exit()
                if event.key == K_KP0:
                    digitalWrite(led, 0)
                    exit()
                if event.key == K_KP4:
                    menu()



# Defines starting conditions for gamemode 2/t
# Less comments as it is nearly identical to starting_phase()
def starting_phase_two(score_start, mold_score_start):
    list_rasp = []
    list_pos_rasp = []
    b1 = Ball(-25.0)

    # Creates Raspberries
    for i in range(0, 30):
        x = randint(1, 10)
        y = randint(1, 4)
        if (x, y) not in list_pos_rasp:
            list_pos_rasp.append((x, y))
            list_rasp.append(Rasperry(x * int(SCREEN_WIDTH*0.0923), (SCREEN_HEIGHT*0.033) + y * int(SCREEN_WIDTH*0.0923), (SCREEN_WIDTH * 0.036)))

    # Background green
    bg_image = pygame.image.load("image/background green score.png").convert()
    bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH_Complete, SCREEN_HEIGHT))

    # Foreground face
    fg_image = pygame.image.load("image/Background face only.png").convert()
    transColor = fg_image.get_at((0, 0))
    fg_image.set_colorkey(transColor)
    fg_image = pygame.transform.scale(fg_image, (SCREEN_WIDTH_Complete, SCREEN_HEIGHT))
    
    # Tongue
    to_image = pygame.image.load("image/Zunge.png").convert()
    to_image.set_colorkey(transColor)
    to_image = pygame.transform.scale(to_image, (tong_width, int(tong_width*0.9)))

    # Rasperry
    global rasperry_image
    global panel_width
    pw = panel_width
    gametime = 0

    while True:
        # Set clock and measure time in seconds
        msElapsed = clock.tick(210)                         # fps set on 60 frames for secondy
        gametime += msElapsed                               # Count While cycles to track time
        time_passed = round(gametime / 1000, 0)             # save time in seconds (millisencondy times 1000)
        screen.blit(bg_image, [0, 0])

        # Draw Raspberries
        for i in list_rasp:
            screen.blit(rasperry_image, [i.pos_x - (SCREEN_WIDTH * 0.03846), i.pos_y - (SCREEN_HEIGHT*0.05)])

        # Panel and Ball
        panel_move_two()
        screen.blit(to_image, [panel_x-(SCREEN_WIDTH*0.0077), panel_y-(SCREEN_HEIGHT*0.00833)]) 
        b1.pos_x = panel_x + panel_half_width               # defines ball position in starting phase (center of panel)
        b1.pos_y = panel_y - 2 * b1.rad
        pygame.draw.circle(screen, BALL_COLOR, (int(b1.pos_x), int(b1.pos_y)), int(b1.diam))

        # Draw Mouth
        screen.blit(fg_image, [0, 0])

        # Write score
        score = myfont.render(str(score_start), False, (200, 60, 100))
        screen.blit(score, score_pos)
        mold_score = myfont.render(str(mold_score_start), False, (80, 155, 220))
        screen.blit(mold_score, mold_score_pos)

        key = pygame.key.get_pressed()                      # start main_game_two, because 2/t was chosen in the menu
        if key[K_KP_ENTER]:
            main_game_two(b1, list_rasp, rasperry_image, score_start, mold_score_start)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                digitalWrite(led, 0)
                pygame.quit()
                exit(0)
            if event.type == KEYDOWN:
                if event.key == K_KP1:
                    digitalWrite(led, 0)
                    exit()
                if event.key == K_KP0:
                    digitalWrite(led, 0)
                    exit()
                if event.key == K_KP4:
                    menu()



# saves new score in csv file
def score(current_score):
    score = float(current_score)                    # translates current score
    r = csv.reader(open('score_list.csv'))          # reads existing highscores
    lines = list(r)                                 # lists highscores

    if float(lines[1][1]) <= score:                 # controls if new score is higher than the highest current score
        for x in range(10, 1, -1):                  # if that's the case: add new best score and shift all following ones
            lines[x][1] = lines[x - 1][1]
        lines[1][1] = str(int(score))
    elif float(lines[1][1]) > score:                # compare all other scores with current one and shift if needed
        for i in range(10, 1, -1):
            if float(lines[i][1]) < score:
                if float(lines[i - 1][1]) >= score:
                    for x in range(10, i, -1):
                        lines[x][1] = lines[x - 1][1]
                    lines[i][1] = str(int(score))

    writer = csv.writer(open('score_list.csv', 'w'))    # rewrite cvs highscores
    writer.writerows(lines)                             



# score menu to view top 10 highscores
def highscore_menu():
    screen.fill(pygame.Color(0, 0, 0))                                  # fills screen with black (not really needed)
    re_image = pygame.image.load("image/score2.png").convert()
    re_image = pygame.transform.scale(re_image, (SCREEN_WIDTH_Complete, SCREEN_HEIGHT))

    screen.blit(re_image, [0, 0])
    screen_r = screen.get_rect()

    # define output: translate from cvs content to useful text to show
    r = csv.reader(open('score_list.csv'))
    lines = list(r)                                                 
    lines_list = ["1.     " + str(lines[1][1]) + "         6.     " + str(lines[6][1]), " "
        , "2.     " + str(lines[2][1]) + "         7.     " + str(lines[7][1]), " "
        , "3.     " + str(lines[3][1]) + "         8.     " + str(lines[8][1]), " "
        , "4.     " + str(lines[4][1]) + "         9.     " + str(lines[9][1]), " "
        , "5.     " + str(lines[5][1]) + "          10.    " + str(lines[10][1])]

    font = pygame.font.SysFont('Lobster Two', 25)                       # defines font and font size
    texts = []                                                          # empty list: gets the follwing r and s assigned

    # render for easier blitting
    for i, line in enumerate(lines_list):                               
        s = font.render(line, 1, (50, 50, 50))                          # assignes color and others to lines
        r = s.get_rect(centerx=screen_r.centerx - (SCREEN_WIDTH*0.0307), y=(SCREEN_HEIGHT*1/3) + i * (SCREEN_WIDTH*0.0307))   # assignes position and movement by changing multiplicator
        texts.append((r, s))

    while True:
        for e in pygame.event.get():
            if e.type == QUIT or e.type == KEYDOWN and e.key == pygame.K_1:
                digitalWrite(led, 0)
                return

        for r, s in texts:                                              # blits text on screen with suitable r and s
            screen.blit(s, r)

        key = pygame.key.get_pressed()
        if key[K_KP4]:
            menu()

        pygame.display.update()
        clock.tick(60)



# main game function
def main_game(b1, list_rasp, rasperry_image, score_start, mold_score_start):
    # Background green
    bg_image = pygame.image.load("image/background green score.png").convert()
    bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH_Complete, SCREEN_HEIGHT))

    # Foreground face
    fg_image = pygame.image.load("image/Background face only.png").convert()
    transColor = fg_image.get_at((0, 0))
    fg_image.set_colorkey(transColor)
    fg_image = pygame.transform.scale(fg_image, (SCREEN_WIDTH_Complete, SCREEN_HEIGHT))

    # Tongue
    to_image = pygame.image.load("image/Zunge.png").convert()
    to_image.set_colorkey(transColor)
    to_image = pygame.transform.scale(to_image, (tong_width, int(tong_width*0.9)))

    # Time: start value, raspberrry change time
    gametime = 0                                      
    global change_time1
    global mold_time
    global end_time
    
    global panel_x
    global panel_y
    global rot_sensor

    while True:
        # Set clock and measure time in seconds
        msElapsed = clock.tick(60)                     # fps set on 60 frames for secondy
        gametime += msElapsed                           # Count While cycles to track time
        time_passed = round(gametime / 1000, 0)         # save time in seconds (millisencondy times 1000)

        # Fill screen_ black
        screen.blit(bg_image, [0, 0])

        # Raspberries-Ball collision and fall
        for i in list_rasp:                             # Check all raspberries
            # Check if distance between rasp. and ball is smaller than the sum of both radiuses
            if b1.pos_y < (SCREEN_HEIGHT*0.5):
                if distance(i.pos_x, i.pos_y, b1.pos_x, b1.pos_y) <= i.rad + b1.rad:
                    counter = 1
                    b1.rebound(i.pos_x, i.pos_y, b1.pos_x, b1.pos_y, b1.pos_x - b1.vel_x, b1.pos_y - b1.vel_y, i.rad,
                               counter)
                    i.fall = True
            if i.fall == True:                          # If collision, then let raspberries fall by function
                i.r_fall()
            if i.pos_y > SCREEN_HEIGHT:                           # if raspberry is over 600 y -> remove it from list
                list_rasp.remove(i)                     
                if time_passed <= mold_time:            # add one score
                    score_start += 1
                else:
                    mold_score_start += 1               # add one moldy score, if mold time has come

        # Rasperry: mature after while by using different images
        for i in list_rasp:
            if time_passed <= change_time1:
                screen.blit(rasperry_image, [i.pos_x - int(SCREEN_WIDTH*0.03846), i.pos_y - int(SCREEN_HEIGHT*0.05)])
            elif change_time1 < time_passed <= mold_time:
                screen.blit(rasperry_image_2, [i.pos_x - int(SCREEN_WIDTH*0.03846), i.pos_y - int(SCREEN_HEIGHT*0.05)])
            elif mold_time < time_passed <= end_time:
                screen.blit(rasperry_image_4, [i.pos_x - int(SCREEN_WIDTH*0.03846), i.pos_y - int(SCREEN_HEIGHT*0.05)])

        # Ball: Draw and move ball via ball class function
        pygame.draw.circle(screen, BALL_COLOR, (int(b1.pos_x), int(b1.pos_y)), int(b1.diam))
        pw = panel_width
        if change_time1 < time_passed <= mold_time:     # panel size defined for second phase in three stages/sizes
            rot = analogRead(rot_sensor)                # range: 0 - 1023
            if rot <= 341:
                pw = int(SCREEN_WIDTH/14)
            elif 341 < rot <= 682:
                pw = int(SCREEN_WIDTH/7)
            elif 682 < rot:
                pw= int(SCREEN_WIDTH*2/7)
                
        b1.move(panel_x, panel_y,pw)

        # Write score
        score = myfont.render(str(score_start), False, (200, 60, 100))
        screen.blit(score, score_pos)
        mold_score = myfont.render(str(mold_score_start), False, (80, 155, 220))
        screen.blit(mold_score, mold_score_pos)
        
        # Sensor by time
        if time_passed <= change_time1:                 # 1. phase: bars with light sensor
            panel_move(panel_width)
            screen.blit(to_image, [panel_x-int(SCREEN_WIDTH*0.0077), panel_y-int(SCREEN_HEIGHT*0.00833)]) 
            light_sensoring()
            b1.light(light_sensoring())
        if change_time1 < time_passed <= mold_time:     # 2. phase: panel with rotation sensor
            panel_move(int(pw))
            to_image = pygame.transform.scale(to_image,(int(pw),int(tong_width*0.9)))
            screen.blit(to_image, [panel_x-int(SCREEN_WIDTH*0.0077), panel_y-int(SCREEN_HEIGHT*0.00833)]) 
        if mold_time < time_passed <= end_time:         # 3. phase: ball with rotation sensor
            panel_move(panel_width)
            to_image = pygame.transform.scale(to_image,(tong_width,int(tong_width*0.9)))
            screen.blit(to_image, [panel_x-int(SCREEN_WIDTH*0.0077), panel_y-int(SCREEN_HEIGHT*0.00833)]) 
            b1.radius()
            
            
        
        # Draw Mouth
        screen.blit(fg_image, [0, 0])
        
        # End game if ball is under the panel or more than 30s passed; Win game if all list_rasp is empty
        # in all death cases: turn all led's off, handles current score over, resets start score, starts restart w/ text 
        if end_time <= time_passed:                     # death by time
            digitalWrite(led, 0)
            current_score = score_start
            score_start = 0
            restart_text = ("Watch your time!")
            restart(current_score, restart_text)
        if not list_rasp:                               # next level -> new level with already earned scores

            digitalWrite(led, 0)
            time.sleep(0.1)
            starting_phase(score_start, mold_score_start)
        if b1.pos_y >= panel_y + b1.rad + (SCREEN_HEIGHT*0.05):           # death by ball loss
            digitalWrite(led, 0)
            current_score = score_start
            score_start = 0
            restart_text = ("Lost your balls...")
            restart(current_score, restart_text)
        if mold_score_start >= 10:                      # death by poisoning by moldies
            digitalWrite(led, 0)
            current_score = score_start
            score_start = 0
            restart_text = ("molding death")
            restart(current_score, restart_text)

        # Update frames each run through
        pygame.display.update()

        # Quit game if x sign or esc is pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                digitalWrite(led, 0)
                pygame.quit()
                exit(0)
            if event.type == KEYDOWN:
                if event.key == K_KP1:
                    digitalWrite(led, 0)
                    exit()
            if event.type == KEYDOWN:
                if event.key == K_KP0:
                    digitalWrite(led, 0)
                    exit()
                if event.key == K_KP4:
                    menu()



# main game version 2
# Less comments as it is nearly identical to main_game()
def main_game_two(b1, list_rasp, rasperry_image, score_start, mold_score_start):
    # Background green
    bg_image = pygame.image.load("image/background green score.png").convert()
    bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH_Complete, SCREEN_HEIGHT))

    # Foreground face
    fg_image = pygame.image.load("image/Background face only.png").convert()
    transColor = fg_image.get_at((0, 0))
    fg_image.set_colorkey(transColor)
    fg_image = pygame.transform.scale(fg_image, (SCREEN_WIDTH_Complete, SCREEN_HEIGHT))

    # Tongue
    to_image = pygame.image.load("image/Zunge.png").convert()
    to_image.set_colorkey(transColor)
    to_image = pygame.transform.scale(to_image, (tong_width, int(tong_width*0.9)))

    # Time
    gametime = 0
    global change_time1
    global mold_time
    global end_time
    
    global panel_x
    global panel_y
    global rot_sensor
    global panel_width

    while True:
        # Set clock and measure time in seconds
        msElapsed = clock.tick(210)                         # fps set on 60 frames for secondy
        gametime += msElapsed                               # Count While cycles to track time
        time_passed = round(gametime / 1000, 0)             # save time in seconds (millisencondy times 1000)

        # Fill screen_ black
        screen.blit(bg_image, [0, 0])

        # Raspberries-Ball collision and fall
        for i in list_rasp:                         # Check all raspberries under 300 pixels
            if b1.pos_y < (SCREEN_HEIGHT*0.5):
                if distance(i.pos_x, i.pos_y, b1.pos_x, b1.pos_y) <= i.rad + b1.rad:
                    counter = 1
                    b1.rebound(i.pos_x, i.pos_y, b1.pos_x, b1.pos_y, b1.pos_x - b1.vel_x, b1.pos_y - b1.vel_y, i.rad,
                               counter)
                    i.fall = True
            if i.fall == True:                      # If collision, then let raspberries fall by function
                i.r_fall()
            if i.pos_y > SCREEN_HEIGHT:                       # Remove Object i, if it's under y=600
                list_rasp.remove(i)  
                if time_passed <= mold_time:
                    score_start += 1                # adds 1 score 
                else:
                    mold_score_start += 1           # adds 1 mold score

        # Rasperry: draw and mold
        for i in list_rasp:
            if time_passed <= change_time1:
                screen.blit(rasperry_image, [i.pos_x - int(SCREEN_WIDTH*0.03846), i.pos_y - int(SCREEN_HEIGHT*0.05)])
            elif change_time1 < time_passed <= mold_time:
                screen.blit(rasperry_image_2, [i.pos_x - int(SCREEN_WIDTH*0.03846), i.pos_y - int(SCREEN_HEIGHT*0.05)])
            elif mold_time < time_passed <= end_time:
                screen.blit(rasperry_image_4, [i.pos_x - int(SCREEN_WIDTH*0.03846), i.pos_y - int(SCREEN_HEIGHT*0.05)])

        # Ball: Draw and move ball via ball class function
        pygame.draw.circle(screen, BALL_COLOR, (int(b1.pos_x), int(b1.pos_y)), int(b1.diam))
        pw = panel_width
        b1.move(panel_x, panel_y,pw)

        # Write score
        score = myfont.render(str(score_start), False, (200, 60, 100))
        screen.blit(score, score_pos)
        mold_score = myfont.render(str(mold_score_start), False, (80, 155, 220))
        screen.blit(mold_score, mold_score_pos)
        
        # panel move by distance sensor: special in mode 1 -> see panel_move_two()
        panel_move_two()
        screen.blit(to_image, [panel_x-(SCREEN_WIDTH*0.0077), panel_y-(SCREEN_HEIGHT*0.00833)]) 
        
        # Draw Mouth
        screen.blit(fg_image, [0, 0])

        # End game if ball is under the panel or more than 30s passed; Win game if all list_rasp is empty
        if end_time <= time_passed:
            digitalWrite(led, 0)
            current_score = score_start
            score_start = 0
            restart_text = ("Watch your time!")
            restart(current_score, restart_text)
        if not list_rasp:
            digitalWrite(led, 0)
            time.sleep(0.1)
            starting_phase(score_start, mold_score_start)
        if b1.pos_y >= panel_y + b1.rad + (SCREEN_HEIGHT*0.05):
            digitalWrite(led, 0)
            current_score = score_start
            score_start = 0
            restart_text = ("Lost your balls...")
            restart(current_score, restart_text)
        if mold_score_start >= 10:
            digitalWrite(led, 0)
            current_score = score_start
            score_start = 0
            restart_text = ("molding death")
            restart(current_score, restart_text)


        # Update frames each run through
        pygame.display.update()

        # Quit game if x sign or esc is pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                digitalWrite(led, 0)
                pygame.quit()
                exit(0)
            if event.type == KEYDOWN:
                if event.key == K_KP1:
                    digitalWrite(led, 0)
                    exit()
            if event.type == KEYDOWN:
                if event.key == K_KP0:
                    digitalWrite(led, 0)
                    exit()
                if event.key == K_KP4:
                    menu()



# credits
def credits():
    screen_r = screen.get_rect()
    font = pygame.font.SysFont('Lobster Two', int(SCREEN_WIDTH_Complete*0.03125), bold=True)  

    # define text with linebreaks
    credit_list = ["BERRY BUSTER", " ", " ", "Developer - Rike & Jenny"
        , " ", "Lead Graphic Designer - Rike & Jenny", " ", "Graphic Designer - Rike & Jenny", " "
        , "Menu System - Rike & Jenny", " ", "Music - Rike & Jenny", " ", "Motion Designer - Rike & Jenny"
        , " ", "Menu sound -  Itty Bitty 8 Bit von"
        , " ", "Kevin MacLeod ist unter der Lizenz "
        , " ", "-Creative Commons Attribution- "
        , " ",    "(https://creativecommons.org/licenses/by/4.0/) lizenziert."
        , " ", "        Quelle: "
        , " ", "    http://incompetech.com/music/royalty-free/index.html?isrc=USUAN1100764"
        , " ", "         Künstler: http://incompetech.com/ "
        , " ", "Credit sound - Sand Castle by Quincas Moreira "
        , " ", "Ingame sound - self made with beepbox.com"
        , " ", "credit code base -"
        , " ", "https://stackoverflow.com/questions/36164524"
        , " ", " ", "Special Thanks to friends :)"
                   ]

    texts = []

    green = pygame.image.load("image/credits.png").convert()
    green = pygame.transform.scale(green, (SCREEN_WIDTH_Complete, SCREEN_HEIGHT))

    for i, line in enumerate(credit_list):
        s = font.render(line, 1, (150, 30, 20))
        # create a Rect for each Surface
        # define starting position
        r = s.get_rect(centerx=screen_r.centerx, y=screen_r.bottom + i * (SCREEN_HEIGHT*0.05))
        texts.append((r, s))

    while True:
        for e in pygame.event.get():
            if e.type == QUIT or e.type == KEYDOWN and e.key == pygame.K_ESCAPE:
                return

        screen.blit(green, [0, 0])

        for r, s in texts:
            r.move_ip(0, -1)                                # move each rect by one pixel each frame
            screen.blit(s, r)                               # draws text

        # if all rects have left the screen -> exit
        if not screen_r.collidelistall([r for (r, _) in texts]):
            nextsong(2)                                     # menu song starts
            menu()

        key = pygame.key.get_pressed()
        if key[K_KP4]:
            nextsong(2)
            menu()

        pygame.display.update()

        clock.tick(60)



# Tutorial: basic game logic in 5 images
def tutorial():
    gametime = 0
    list_tut = ["image/tut1.png", "image/tut2.png", "image/tut_general.png", "image/tut35.png", "image/tut45.png"]
    lastclick = 0
    click = 0
    image = pygame.image.load(list_tut[click]).convert()             # Load Restart background
    image = pygame.transform.scale(image, (SCREEN_WIDTH_Complete, SCREEN_HEIGHT))                # Transform image to fit in screen

    while True:
        mselapsed = clock.tick(100)                                  # fps set on 60 frames for secondy
        gametime += mselapsed                                        # Count While cycles to track time
        screen.blit(image, [0, 0])

        key = pygame.key.get_pressed()                               # If Space gets pressed -> switch to menu
        if key[K_BACKSPACE]:                                         # right arrow to switch to new image
            if lastclick + 300 < gametime:
                lastclick = gametime
                click += 1
                if click == 5:
                    click = 0
                image = pygame.image.load(list_tut[click]).convert() # Load Restart background
                image = pygame.transform.scale(image, (SCREEN_WIDTH_Complete, SCREEN_HEIGHT))    # Transform image to fit in screen

        if key[K_KP_PLUS]:                                           # left arrow to go back to last image
            if lastclick + 300 < gametime:
                lastclick = gametime
                click -= 1
                if click == -1:
                    click = 4
                image = pygame.image.load(list_tut[click]).convert()  
                image = pygame.transform.scale(image, (SCREEN_WIDTH_Complete, SCREEN_HEIGHT))  

        key = pygame.key.get_pressed()                               # If Space gets pressed -> switch to menu
        if key[K_KP4]:
            menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                digitalWrite(led, 0)
                pygame.quit()
                exit(0)
            if event.type == KEYDOWN:
                if event.key == K_KP1:
                    digitalWrite(led, 0)
                    exit()
            if event.type == KEYDOWN:
                if event.key == K_KP0:
                    digitalWrite(led, 0)
                    exit()
                if event.key == K_KP4:
                    menu()

        pygame.display.update()



# menu: let's player choose between main game, credit, scores and quit
def menu():
                            # turns off all leds 
    
    
    digitalWrite(led, 1)                            # turns on LED string

    menu_image = pygame.image.load("image/menu.png").convert()
    menu_image = pygame.transform.scale(menu_image, (SCREEN_WIDTH_Complete, SCREEN_HEIGHT))

    score_start = 0
    mold_score_start = 0
    
    nextsong(2)                                     # menu song starts playing (see nextsong() -> will be looped)

    while True:
        screen.blit(menu_image, [0, 0])

        key = pygame.key.get_pressed()
        if key[K_KP2]:                              # marked as s
            nextsong(0)
            starting_phase(score_start, mold_score_start)
            
        if key[K_KP3]:                              # marked as t
            nextsong(0)
            starting_phase_two(score_start, mold_score_start)
            
        if key[K_KP6]:                              # marked as C
            nextsong(1)
            credits()

        if key[K_KP9]:                              # marked as R
            highscore_menu()

        if key[K_KP_MULTIPLY]:                      # marked as tutorial
            tutorial()
            
        if key[K_0]:
            exit()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                digitalWrite(led, 0)
                pygame.quit()
                exit(0)
            if event.type == KEYDOWN:
                if event.key == K_KP1:
                    digitalWrite(led, 0)
                    exit()
                if event.key == K_KP7:                              # marked as G
                    pygame.mixer.music.pause()
                    import Gami_sec



# Welcome animation
def welcome_opening():
    global SCREEN_WIDTH_Complete
    width = SCREEN_WIDTH_Complete

    green_image = pygame.image.load("image/green.png").convert()
    green_image = pygame.transform.scale(green_image, (SCREEN_WIDTH_Complete, SCREEN_HEIGHT))

    # Define falling raspberries - Raspberry(pos.x, pos.y, rad) - defined in class above
    rad_berry = int(SCREEN_WIDTH * 0.036)
    r1 = Rasperry((SCREEN_WIDTH_Complete * 0.025),  -rad_berry, rad_berry)
    r2 = Rasperry((SCREEN_WIDTH_Complete * 0.0625),  -rad_berry, rad_berry)
    r3 = Rasperry((SCREEN_WIDTH_Complete * 0.1875), -rad_berry, rad_berry)
    r4 = Rasperry((SCREEN_WIDTH_Complete * 0.375), -rad_berry, rad_berry)
    r5 = Rasperry((SCREEN_WIDTH_Complete * 0.5625), -rad_berry, rad_berry)
    r6 = Rasperry((SCREEN_WIDTH_Complete * 0.775), -rad_berry, rad_berry)
    r7 = Rasperry((SCREEN_WIDTH_Complete * 0.95), -rad_berry, rad_berry)

    gametime = 0
    time_passed = 250

    def anim_fall(rasp, time):                      # if time has come -> rasp.fall will set to be True
        if i >= time:
            rasp.fall = True
        if rasp.fall == True:                       # if rasp.fall  equals True -> Berry falls 
            rasp.r_fall()
        screen.blit(rasperry_image_2, [rasp.pos_x - int(SCREEN_WIDTH_Complete*0.03125), rasp.pos_y - int(SCREEN_WIDTH_Complete*0.0375)])

    for i in range(0, time_passed):                 # actual "animation" of falling raspberries depening on actual time
        screen.fill((0, 0, 0))
        screen.blit(green_image, [0, 0])

        anim_fall(r1, 1)
        anim_fall(r2, 160)
        anim_fall(r3, 30)
        anim_fall(r4, 60)
        anim_fall(r5, 170)
        anim_fall(r6, 90)
        anim_fall(r7, 140)

        time.sleep(0.005)                         
        pygame.display.update()

    list_name = ["b", "e", "r", "r2", "y", "b2", "u", "s", "t", "e2", "r3"]     # defines images used 
    for i in range(0, 11):                                                      # every 0.2s a new image will be blitted
        image = ("image/" + str(list_name[i]) + ".png")
        image = pygame.image.load(image).convert()
        image = pygame.transform.scale(image, (SCREEN_WIDTH_Complete, SCREEN_HEIGHT))
        screen.blit(image, (0, 0))

        time.sleep(0.2)
        pygame.display.update()

    time.sleep(1)
    tutorial()                                     # tutorial automatically starts -> then skipping to menu is possible 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)


#menu()


welcome_opening()
