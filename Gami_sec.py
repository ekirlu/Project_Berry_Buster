import pygame
from pygame.locals import *
from pygame import *
import time
import random
import math
# import numpy as np
# import sympy as sy
import sys
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

pygame.font.init()  # you have to call this at the start,
myfont = pygame.font.SysFont('Lobster Two', int(3*SCREEN_WIDTH/80))


player_x = SCREEN_WIDTH / 2
player_y = SCREEN_HEIGHT / 2

player_x2 = SCREEN_WIDTH / 2
player_y2 = SCREEN_HEIGHT / 2

rot_sensor1 = 0


class player:
    def __init__(self, rad, vel, col):
        self.rad = rad
        self.vel = vel
        self.col = col

    def move_player1(self):
        global player_x
        global player_y
        key = pygame.key.get_pressed()
        if key[K_BACKSPACE]:    # right: marked as right arrow
            if player_x + self.rad <= SCREEN_WIDTH_Complete:
                player_x += self.vel
        if key[K_KP_MINUS]:  # down: marked as down arrow
            if player_y + self.rad <= SCREEN_HEIGHT:
                player_y += self.vel
        if key[K_KP_PLUS]:  # left: marked as left arrow
            if player_x - self.rad >= 0:
                player_x -= self.vel
        if key[K_KP9]:  # up: marked as R   
            if player_y - self.rad >= 0:
                player_y -= self.vel

    def move_player2(self):
        global player_x2
        global player_y2
        key = pygame.key.get_pressed()
        if key[K_d]:
            if player_x2 + self.rad <= SCREEN_WIDTH_Complete:
                player_x2 += self.vel
        if key[K_s]:
            if player_y2 + self.rad <= SCREEN_HEIGHT:
                player_y2 += self.vel
        if key[K_a]:
            if player_x2 - self.rad >= 0:
                player_x2 -= self.vel
        if key[K_w]:
            if player_y2 - self.rad >= 0:
                player_y2 -= self.vel



def distance(x1, y1, x2, y2):
    dx = x1 - x2
    dy = y1 - y2
    # return math.hypot(dx, dy)
    if (dx ** 2 + dy ** 2) <= 0:
        return 0
    else:
        return abs(dx ** 2 + dy ** 2) ** (1 / 2)



class enemy:
    def __init__(self, vel_x, vel_y, rad=int(SCREEN_HEIGHT*0.0167)):
        self.pox = random.randint(0, SCREEN_WIDTH_Complete)
        self.poy = random.randint(0, SCREEN_HEIGHT)
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.rad = rad
        self.speed = (vel_x ** 2 + vel_y ** 2) ** (1 / 2)

    def run(self):
        self.pox += self.vel_x
        self.poy += self.vel_y

        if self.pox >=  SCREEN_WIDTH_Complete or self.pox <= 0:
            self.vel_x = -self.vel_x
        if self.poy >= SCREEN_HEIGHT or self.poy <= 0:
            self.vel_y = -self.vel_y

    def rebound(self, p1x, p1y, x, y, lastx, lasty, counter):
        hx = (x + lastx) / 2
        hy = (y + lasty) / 2
        counter += 1
        if counter <= 700:
            if distance(p1x, p1y, hx, hy) <= p1.rad + self.rad - 3:
                self.rebound(p1x, p1y, x, y, hx, hy, counter)
            elif distance(p1x, p1y, hx, hy) >= p1.rad + self.rad + 3:
                self.rebound(p1x, p1y, hx, hy, lastx, lasty, counter)
            else:
                # p_x, p_y = hx, hy
                ortsvektor_x = p1x - hx
                ortsvektor_y = p1y - hy
                # t = sy.Symbol('t')
                # lot_x = hx+t*(p1x - hx)
                # lot_y = hy+t*(p1y - hy)
                # t_berechnet = sy.solve(sy.Eq((hx+t*(p1x - hx)-lastx)*ortsvektor_x+(hy+t*(p1y - hy)-lasty)*ortsvektor_y, 0))
                if (-p1x * (p1x - hx) + hx * (p1x - hx) - p1y * (p1y - hy) + hy * (p1y - hy)) != 0:
                    t_berechnet = ((p1x ** 2) + p1x * lastx - p1x * hx + lastx * hx + ( p1y ** 2) + p1y * lasty - p1y * hy + lastx * hy) / (-p1x * (p1x - hx) + hx * (p1x - hx) - p1y * (p1y - hy) + hy * (p1y - hy))
                else:
                    t_berechnet = 0
                # t_berechnet = (p_x * ortsvektor_x + p_y * ortsvektor_y - hx * ortsvektor_x - hy *ortsvektor_y)/((p1x - hx) * ortsvektor_x + (p1y - hy) * ortsvektor_y)
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
                vel_ratio = res_vel / self.speed
                if vel_ratio != 0:
                    self.vel_x = vel_x_part / vel_ratio
                    self.vel_y = vel_y_part / vel_ratio
                else:
                    self.vel_x = vel_x
                    self.vel_y = vel_y
        else:
            # p_x, p_y = hx, hy
            ortsvektor_x = p1x - hx
            ortsvektor_y = p1y - hy
            # t = sy.Symbol('t')
            # lot_x = hx+t*(p1x - hx)
            # lot_y = hy+t*(p1y - hy)
            # t_berechnet = sy.solve(sy.Eq((hx+t*(p1x - hx)-lastx)*ortsvektor_x+(hy+t*(p1y - hy)-lasty)*ortsvektor_y, 0))
            if (-p1x * (p1x - hx) + hx * (p1x - hx) - p1y * (p1y - hy) + hy * (p1y - hy)) != 0:
                t_berechnet = ((p1x ** 2) + p1x * lastx - p1x * hx + lastx * hx + (
                            p1y ** 2) + p1y * lasty - p1y * hy + lastx * hy) / (
                                          -p1x * (p1x - hx) + hx * (p1x - hx) - p1y * (p1y - hy) + hy * (p1y - hy))
            else:
                t_berechnet = 0
            # t_berechnet = (p_x * ortsvektor_x + p_y * ortsvektor_y - hx * ortsvektor_x - hy *ortsvektor_y)/((p1x - hx) * ortsvektor_x + (p1y - hy) * ortsvektor_y)
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
            vel_ratio = res_vel / self.speed
            if vel_ratio != 0:
                self.vel_x = vel_x_part / vel_ratio
                self.vel_y = vel_y_part / vel_ratio
            else:
                self.vel_x = vel_x
                self.vel_y = vel_y

    def goal(self):
        if int(SCREEN_WIDTH_Complete * 0.4375) <= self.pox <= int(SCREEN_WIDTH_Complete * 0.5625) and self.poy <= int(SCREEN_HEIGHT*4/600):
            down = True
            return down
        if int(SCREEN_WIDTH_Complete * 0.4375) <= self.pox <= int(SCREEN_WIDTH_Complete * 0.5625) and self.poy >= SCREEN_HEIGHT - int(SCREEN_HEIGHT*4/600):
            down = True
            return down

    def goal2(self):
        if int(SCREEN_WIDTH_Complete * 0.4375) <= self.pox <= int(SCREEN_WIDTH_Complete * 0.5625) and self.poy <= int(SCREEN_HEIGHT*4/600):
            down = True
            return down
        if int(SCREEN_WIDTH_Complete * 0.4375) <= self.pox <= int(SCREEN_WIDTH_Complete * 0.5625) and self.poy >= SCREEN_HEIGHT - int(SCREEN_HEIGHT*4/600):
            down = True
            return down
        #if 250 <= self.poy <= 350 and self.pox <= 4:
        #    down = True
        #    return down
        #if 250 <= self.poy <= 350 and self.pox >= 796:
        #    down = True
        #    return down

    def draw(self):
        draw.circle(screen, (200, 200, 200,), (int(self.pox), int(self.poy)), self.rad)
        
    def bar_rebound(self):
        rot = round((analogRead(rot_sensor1)),0)            # 0-1023
        x = rot*2*int(SCREEN_WIDTH_Complete * 0.125)/1023
        
        # barrier up
        pygame.draw.rect(screen, (100, 100, 100), (x+int(SCREEN_WIDTH_Complete * 0.4375)-int(SCREEN_WIDTH_Complete * 0.125), 2*int(SCREEN_HEIGHT * 4/800), int(SCREEN_WIDTH_Complete * 0.125), 2*int(SCREEN_HEIGHT * 4/800))) # Y = 0
        if  2*int(SCREEN_HEIGHT * 4/800) <= self.poy - self.rad <= 3*2*int(SCREEN_HEIGHT * 4/800):
            if x+int(SCREEN_WIDTH_Complete * 0.4375)-int(SCREEN_WIDTH_Complete * 0.125) <= self.pox <= x+int(SCREEN_WIDTH_Complete * 0.4375):
                self.vel_y = -self.vel_y
                
        # barrier down
        pygame.draw.rect(screen, (100, 100, 100), (x+int(SCREEN_WIDTH_Complete * 0.4375)-int(SCREEN_WIDTH_Complete * 0.125), SCREEN_HEIGHT-6*int(SCREEN_HEIGHT * 4/800), int(SCREEN_WIDTH_Complete * 0.125), 2*int(SCREEN_HEIGHT * 4/800))) # Y = 0
        if  SCREEN_HEIGHT-4*2*int(SCREEN_HEIGHT * 4/800) <= self.poy + self.rad <= SCREEN_HEIGHT - 3*int(SCREEN_HEIGHT * 4/800):
            if x+int(SCREEN_WIDTH_Complete * 0.4375)-int(SCREEN_WIDTH_Complete * 0.125) <= self.pox <= x+int(SCREEN_WIDTH_Complete * 0.4375):
                self.vel_y = -self.vel_y
                
        # left & right
        pygame.draw.rect(screen, (100, 100, 100), (2*int(SCREEN_HEIGHT * 4/800),x+int(SCREEN_HEIGHT * 0.4167)-int(SCREEN_WIDTH_Complete * 0.125) , 2*int(SCREEN_HEIGHT * 4/800), int(SCREEN_WIDTH_Complete* 0.125 ))) # Y = 0
        if  2*int(SCREEN_HEIGHT * 4/800) <= self.pox - self.rad <= 5*int(SCREEN_HEIGHT * 4/800):
            if x+int(SCREEN_HEIGHT * 0.4167)-int(SCREEN_WIDTH_Complete * 0.125) <= self.poy <= x+int(SCREEN_HEIGHT * 0.4167):
                self.vel_x = -self.vel_x
                
        pygame.draw.rect(screen, (100, 100, 100), (SCREEN_WIDTH_Complete - 6*int(SCREEN_HEIGHT * 4/800),x+int(SCREEN_HEIGHT * 0.4167)-int(SCREEN_WIDTH_Complete * 0.125) , 2*int(SCREEN_HEIGHT * 4/800), int(SCREEN_WIDTH_Complete* 0.125 ))) # Y = 0
        if  SCREEN_WIDTH_Complete - 2*4*int(SCREEN_HEIGHT * 4/800) <= self.pox + self.rad <= SCREEN_WIDTH_Complete - 5*int(SCREEN_HEIGHT * 4/800):
            if x+int(SCREEN_HEIGHT * 0.4167)-int(SCREEN_WIDTH_Complete * 0.125) <= self.poy <= x+int(SCREEN_HEIGHT * 0.4167):
                self.vel_x = -self.vel_x
                
                
p1 = player((SCREEN_WIDTH_Complete * 0.0375), 12, (255, 0, 0))
p2 = player((SCREEN_WIDTH_Complete * 0.0375), 12, (0, 255, 0))
    

def start(scores, enemy_count):
    gametime = 0
    global SCREEN_WIDTH
    global SCREEN_WIDTH_Complete
    global SCREEN_HEIGHT

    list = []
    for i in range(0, enemy_count):
        vel_x = random.choice([-8.5, -8, -7, -6, 6, 7, 8, 8.5])
        vel_y = random.choice([-8.5, -8, -7, -6, 6, 7, 8, 8.5])
        speed = abs(vel_x ** 2 + vel_y ** 2) ** (1 / 2)
        list.append(enemy(vel_x, vel_y))

    while True:
        # Set clock and measure time in seconds
        mselapsed = clock.tick(60)                                      # fps set on 60 frames for secondy
        gametime += mselapsed                                           # Count While cycles to track time
        time_passed = round(gametime / 1000, 0)                         # save time in seconds (millisencondy times 1000)
        screen.fill((0, 0, 0))

        for i in list:
            i.run()
            i.draw()

        p1.move_player1()
        pygame.draw.circle(screen, p1.col, (int(player_x), int(player_y)), int(p1.rad))
        p1x = player_x
        p1y = player_y
        for i in list:  # Check all raspberries
            #i.bar_rebound()                                            # activate bars
            dist = distance(p1x, p1y, i.pox, i.poy)
            if dist <= p1.rad + 10:
                counter = 1
                i.rebound(p1x, p1y, i.pox, i.poy, i.pox - i.vel_x, i.poy - i.vel_y, counter)

        for i in list:
            if i.goal():
                list.remove(i)
                scores += 1
            if not list:
                enemy_count += 1
                start(scores, enemy_count)

        for i in list:
            if int(SCREEN_HEIGHT * 0.4167) <= i.poy <= int(SCREEN_HEIGHT * 0.5833) and ((i.pox - i.speed) <= - i.speed):
                vel_x = random.choice([-8.5, -8, -7, -6, 6, 7, 8, 8.5])
                vel_y = random.choice([-8.5, -8, -7, -6, 6, 7, 8, 8.5])
                speed = abs(vel_x ** 2 + vel_y ** 2) ** (1 / 2)
                list.append(enemy(vel_x, vel_y))
            if int(SCREEN_HEIGHT * 0.4167) <= i.poy <= int(SCREEN_HEIGHT * 0.5833)  and ((i.pox + i.speed) >= SCREEN_WIDTH_Complete + i.speed):
                vel_x = random.choice([-8.5, -8, -7, -6, 6, 7, 8, 8.5])
                vel_y = random.choice([-8.5, -8, -7, -6, 6, 7, 8, 8.5])
                speed = abs(vel_x ** 2 + vel_y ** 2) ** (1 / 2)
                list.append(enemy(vel_x, vel_y))

        pygame.draw.rect(screen, (0, 255, 0), (int(SCREEN_WIDTH_Complete * 0.4375), 0, int(SCREEN_WIDTH_Complete * 0.125), int(SCREEN_HEIGHT * 4/800))) # Y = 0
        pygame.draw.rect(screen, (0, 0, 255), (0, int(SCREEN_HEIGHT * 0.4167), int(SCREEN_WIDTH_Complete * 4/800), int(SCREEN_HEIGHT * 0.125)))
        pygame.draw.rect(screen, (0, 255, 0), (int(SCREEN_WIDTH_Complete * 0.4375), int(SCREEN_HEIGHT * 0.993), int(SCREEN_WIDTH_Complete * 0.125), int(SCREEN_HEIGHT * 4/800))) # Y = full
        pygame.draw.rect(screen, (0, 0, 255), (int(SCREEN_WIDTH_Complete * 0.995), int(SCREEN_HEIGHT * 0.4167),  int(SCREEN_WIDTH_Complete * 4/800), int(SCREEN_HEIGHT * 0.125)))


        text_score = "Score:" + str(scores)
        text = myfont.render(str(text_score), False, (50, 50, 50))
        screen.blit(text, (int(SCREEN_WIDTH_Complete*0.125), int(SCREEN_HEIGHT*0.1)))
        text = myfont.render(("Phase "+str(enemy_count)), False, (50, 50, 50))
        screen.blit(text, (int(SCREEN_WIDTH_Complete*0.125), int(SCREEN_HEIGHT*0.033)))

        if len(list) > 30:
            end(scores)

        pygame.display.update()

        key = pygame.key.get_pressed()  # If Space gets pressed -> switch to menu
        if key[K_KP_ENTER]:             # marked as tab
            menu()
        if key[K_0]:
            exit()

        # Quit game if x sign or esc is pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == KEYDOWN:
                if event.key == K_KP1:
                    exit()


def start2(scores, enemy_count):
    gametime = 0
    time_passed = 0

    list = []
    for i in range(0, enemy_count):
        vel_x = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
        vel_y = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
        speed = abs(vel_x ** 2 + vel_y ** 2) ** (1 / 2)
        list.append(enemy(vel_x, vel_y))

    while True:
        # Set clock and measure time in seconds
        mselapsed = clock.tick(100)  # fps set on 60 frames for secondy
        gametime += mselapsed  # Count While cycles to track time
        time_passed = round(gametime / 1000, 0)  # save time in seconds (millisencondy times 1000)
        screen.fill((0, 0, 0))

        for i in list:
            i.run()
            i.draw()

        p1.move_player1()
        p2.move_player2()
        pygame.draw.circle(screen, p1.col, (int(player_x), int(player_y)), int(p1.rad))
        pygame.draw.circle(screen, p2.col, (int(player_x2), int(player_y2)), int(p2.rad))
        p1x = player_x
        p1y = player_y
        for i in list:  # Check all raspberries
            dist = distance(p1x, p1y, i.pox, i.poy)
            dist2 = distance(player_x2, player_y2, i.pox, i.poy)
            if dist <= p1.rad + 10:
                counter = 1
                i.rebound(p1x, p1y, i.pox, i.poy, i.pox - i.vel_x, i.poy - i.vel_y, counter)
            if dist2 <= p2.rad + 10:
                counter = 1
                i.rebound(player_x2, player_y2, i.pox, i.poy, i.pox - i.vel_x, i.poy - i.vel_y, counter)

        for i in list:
            if i.goal2():
                list.remove(i)
                scores += 1
            if not list:
                enemy_count += 1
                start2(scores, enemy_count)

        for i in list:
            if 250 <= i.poy <= 350 and ((i.pox - i.speed) <= - i.speed):
                vel_x = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
                vel_y = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
                speed = abs(vel_x ** 2 + vel_y ** 2) ** (1 / 2)
                list.append(enemy(vel_x, vel_y))
            if 250 <= i.poy <= 350 and ((i.pox + i.speed) >= 800 + i.speed):
                vel_x = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
                vel_y = random.choice([-4, -3, -2, -1, 1, 2, 3, 4])
                speed = abs(vel_x ** 2 + vel_y ** 2) ** (1 / 2)
                list.append(enemy(vel_x, vel_y))

        pygame.draw.rect(screen, (0, 255, 0), (int(SCREEN_WIDTH_Complete * 0.4375), 0, int(SCREEN_WIDTH_Complete * 0.125), int(SCREEN_HEIGHT * 4/800))) # Y = 0
        pygame.draw.rect(screen, (0, 0, 255), (0, int(SCREEN_HEIGHT * 0.4167), int(SCREEN_WIDTH_Complete * 4/800), int(SCREEN_HEIGHT * 0.125)))
        pygame.draw.rect(screen, (0, 255, 0), (int(SCREEN_WIDTH_Complete * 0.4375), int(SCREEN_HEIGHT * 0.993), int(SCREEN_WIDTH_Complete * 0.125), int(SCREEN_HEIGHT * 4/800))) # Y = full
        pygame.draw.rect(screen, (0, 0, 255), (int(SCREEN_WIDTH_Complete * 0.995), int(SCREEN_HEIGHT * 0.4167),  int(SCREEN_WIDTH_Complete * 4/800), int(SCREEN_HEIGHT * 0.125)))


        text_score = "Score:" + str(scores)
        text = myfont.render(str(text_score), False, (50, 50, 50))
        screen.blit(text, (20, 60))
        text = myfont.render(("Phase " + str(enemy_count)), False, (50, 50, 50))
        screen.blit(text, (20, 20))

        if len(list) > 30:
            end(scores)

        pygame.display.update()

        key = pygame.key.get_pressed()  # If Space gets pressed -> switch to menu
        if [K_KP_ENTER]: # marked as tab
            menu()
        if key[K_0]:
            exit()

        # Quit game if x sign or esc is pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == KEYDOWN:
                if event.key == K_KP1:
                    exit()


def end(scores):
    start = 0
    time = 30
    for i in range(start, time):
        image = ("image/fatality.jpg")
        image = pygame.image.load(image).convert()
        image = pygame.transform.scale(image, (SCREEN_WIDTH_Complete, SCREEN_HEIGHT))
        screen.blit(image, (0, 0))
        pygame.display.update()

    while True:
        screen.fill((0, 0, 0))

        text_score = "Your  final  score  is  " + str(scores)
        text = myfont.render(str(text_score), False, (50, 50, 50))
        screen.blit(text, (int(SCREEN_WIDTH_Complete*0.3125), int(SCREEN_HEIGHT*0.4167)))

        text = myfont.render("Press TAB for menu", False, (50, 50, 50))
        screen.blit(text, (int(SCREEN_WIDTH_Complete*0.3125), int(SCREEN_HEIGHT*0.667)))

        pygame.display.update()

        key = pygame.key.get_pressed()  # If Space gets pressed -> switch to menu
        if key[K_KP_ENTER]:
            menu()
        if key[K_0]:
            exit()

        # Quit game if x sign or esc is pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == KEYDOWN:
                if event.key == K_KP1:
                    exit()


def menu():
    global player_x
    global player_y
    global player_y2
    global player_x2
    player_x = SCREEN_WIDTH / 2
    player_y = SCREEN_HEIGHT / 2
    player_x2 = SCREEN_WIDTH / 2
    player_y2 = SCREEN_HEIGHT / 2

    while True:
        pygame.display.update()

        screen.fill((0, 0, 0))
        text = myfont.render("Surprise minigame", False, (50, 50, 50))
        screen.blit(text, (int(SCREEN_WIDTH_Complete * 0.467), int(SCREEN_HEIGHT * 0.067)))
        text = myfont.render("PRESS -S- for one player mode", False, (50, 50, 50))
        screen.blit(text, (int(SCREEN_WIDTH_Complete * 0.2625), int(SCREEN_HEIGHT * 0.15)))
        text = myfont.render("PRESS -T- for two player mode", False, (50, 50, 50))
        screen.blit(text, (210, 130))
        text = myfont.render("GREENs are your goals", False, (0, 255, 0))
        screen.blit(text, (int(SCREEN_WIDTH_Complete * 0.2625), int(SCREEN_HEIGHT * 0.3167)))
        text = myfont.render("BLUEs add one ball", False, (0, 0, 255))
        screen.blit(text, (int(SCREEN_WIDTH_Complete * 0.2625), int(SCREEN_HEIGHT * 0.4167)))
        text = myfont.render("Try to destroy all balls", False, (50, 50, 50))
        screen.blit(text, (int(SCREEN_WIDTH_Complete * 0.2625), int(SCREEN_HEIGHT * 0.5)))
        text = myfont.render("Return to BERRY BUSTER with SPACE", False, (50, 50, 50))
        screen.blit(text, (int(SCREEN_WIDTH_Complete * 0.2625), int(SCREEN_HEIGHT * 0.6)))
        text = myfont.render("Return to MINI GAME with TAB", False, (50, 50, 50))
        screen.blit(text, (int(SCREEN_WIDTH_Complete * 0.2625), int(SCREEN_HEIGHT * 0.7)))
        pygame.draw.rect(screen, (0, 255, 0), (int(SCREEN_WIDTH_Complete * 0.4375), 0, int(SCREEN_WIDTH_Complete * 0.125), int(SCREEN_HEIGHT * 4/800))) # Y = 0
        pygame.draw.rect(screen, (0, 0, 255), (0, int(SCREEN_HEIGHT * 0.4167), int(SCREEN_WIDTH_Complete * 4/800), int(SCREEN_HEIGHT * 0.125)))
        pygame.draw.rect(screen, (0, 255, 0), (int(SCREEN_WIDTH_Complete * 0.4375), int(SCREEN_HEIGHT * 0.993), int(SCREEN_WIDTH_Complete * 0.125), int(SCREEN_HEIGHT * 4/800))) # Y = full
        pygame.draw.rect(screen, (0, 0, 255), (int(SCREEN_WIDTH_Complete * 0.995), int(SCREEN_HEIGHT * 0.4167),  int(SCREEN_WIDTH_Complete * 4/800), int(SCREEN_HEIGHT * 0.125)))

        key = pygame.key.get_pressed()  # If Space gets pressed -> switch to menu
        if key[K_0]:
            exit()
        if key[K_KP2]:  # marked as s
            scores = 0
            enemy_count = 1
            start(scores, enemy_count)
        if key[K_KP3]: # marked as t
            scores = 0
            enemy_count = 1
            start2(scores, enemy_count)


        # Quit game if x sign or esc is pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == KEYDOWN:
                if event.key == K_KP1:
                    exit()
                if event.key == K_KP4:
                    pygame.mixer.music.unpause()
                    import main

menu()

