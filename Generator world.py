#/ сделать горы через тектанические плиты

import pygame
import numpy as np
from random import*
from pygame.locals import *
import math

global map_size
map_size=64 #00
max_map_size=128

global pixel_size
pixel_size=512//32

global min_pixel_size
min_pixel_size=16

global vrem_per 
vrem_per=1

global map_screen
map_screen=np.zeros((map_size,map_size),dtype='int16')

landscape = {
        0: (14,83,167),    # вода
        1: (0,195,34),     # земля
        2: (0,40,200),     # не закрепленая река
        3: (0,40,230),     # закрепленая река
        4: (255,40,230)
    }

temperature = { 
    0: (255, 0, 0),    # 32
    1: (255, 50, 0),   # 26
    2: (255, 94, 0),   # 20
    3: (255, 136, 0),  # 14
    4: (255, 173, 0),  # 8
    5: (255, 218, 0),  # 2
    6: (255, 248, 0),  # -4
    7: (189, 255, 0),  # -10
    8: (89, 255, 0),   # -16
    9: (0, 222, 255),  # -22
    10: (0, 217, 255), # -28
    11: (0, 180, 255), # -34
    12: (0, 141, 255), # -40
    13: (0, 82, 255),  # -46
    14: (0, 23, 255),  # -52
    15: (95, 0, 255),  # -58
    16: (170, 0, 255), # -64       
}

pygame.init()

screen_width = 1024
screen_height = 1024
screen = pygame.display.set_mode((screen_width, screen_height))
screen.fill((0,0,0))

def gen_map_temperature():
    global map_temperature
    map_temperature=np.zeros((max_map_size,max_map_size),dtype='int32')
    for y in range(max_map_size):
        for x in range(max_map_size):
            if y<32: map_temperature[y][x]=(17*(y**0.5)) -64 + randint(-10,10)
            else: map_temperature[y][x]=(17*((64-y)**0.5)) -64 + randint(-10,10)

def map_size_64():
    map_size=64
    global map_screen
    map_screen=np.zeros((map_size,map_size),dtype='int16')

def create_continent():
    for y in range(map_size):
        for x in range(map_size):
            map_screen[y][x]=0
            if randint(0,100)>=40: map_screen[y][x]=1
    #otl_print(map_screen)

def day_night(a,b,c):
    for a in  range(a):
        for y in range(1,map_size-1):
            for x in range(1,map_size-1):
                count_1=0
                if map_screen[y-1][x-1]==1:count_1+=1
                if map_screen[y-1][x+1]==1:count_1+=1
                if map_screen[y+1][x-1]==1:count_1+=1
                if map_screen[y+1][x+1]==1:count_1+=1
                if map_screen[y-1][x]==1:count_1+=1
                if map_screen[y+1][x]==1:count_1+=1
                if map_screen[y][x-1]==1:count_1+=1
                if map_screen[y][x+1]==1:count_1+=1
                if map_screen[y][x]==0:
                    if b != 9:
                        if isinstance(b, int): 
                            if count_1 == b: map_screen[y][x]=1
                        else:
                            for i in range(len(b)):
                                if count_1 == b[i]: map_screen[y][x]=1
                else:
                    if c != 9:
                        if isinstance(c, int):
                            if count_1 == c: map_screen[y][x]=0
                        else:
                            for i in range(len(c)):
                                if count_1 == c[i]: map_screen[y][x]=0
    otl_print(map_screen)
           
def  noise_editor1():
    for y in range(map_size):
        for x in range(map_size):
            if map_screen[y][x]==1:
                if randint(0,100)<=30: map_screen[y][x]=0
            if map_screen[y][x]==0:
                if randint(0,100)<=30: map_screen[y][x]=1
    otl_print(map_screen)

def  noise_editor2():
    for y in range(map_size):
        for x in range(map_size):
            if map_screen[y][x]==1:
                if randint(0,100)<=10: map_screen[y][x]=0
            if map_screen[y][x]==0:
                if randint(0,100)<=45: map_screen[y][x]=1
    otl_print(map_screen)

# функцию зума к примеру из карты 20 на 20 делать 200 на 200 и наоборот 
def zoom(mult):
    if mult > 0:
        global map_size
        if map_size < max_map_size:
            global map_screen
            global pixel_size
            pixel_size = pixel_size //mult
            map_size_old = map_size  
            map_size=map_size*mult # увеличить разрядность
            mat_new=np.zeros((map_size,map_size),dtype='int16')
            for y in range(map_size_old):
                for x in range(map_size_old):
                    mat_new[y * mult:(y + 1) * mult, x * mult:(x + 1) * mult] = map_screen[y, x]
            map_screen = mat_new
            otl_print(map_screen)

def river_create():
    chance=0
    v_s = randint(1,4)
    if v_s == 1:
        if randint(0,1) == 0:
            x = randint(0,map_size//2)
            if randint(0,100)>=chance: map_screen[0][x]=2
        else:
            y = randint(0,map_size//2)
            if randint(0,100)>=chance: map_screen[y][0]=2
    
    if v_s == 2:
        if randint(0,1) == 0:
            x = randint(map_size//2,map_size-1)
            if randint(0,100)>=chance: map_screen[0][x]=2
        else:
            y = randint(0,map_size//2)
            if randint(0,100)>=chance: map_screen[y][map_size-1]=2
    
    if v_s == 3:
        if randint(0,1) == 0:
            x = randint(0,map_size//2)
            if randint(0,100)>=chance: map_screen[map_size-1][x]=2
        else:
            y = randint(map_size//2,map_size-1)
            if randint(0,100)>=chance: map_screen[y][0]=2
    
    if v_s == 4:
        if randint(0,1) == 0:
            x = randint(map_size//2,map_size-1)
            if randint(0,100)>=chance: map_screen[map_size-1][x]=2
        else:
            y = randint(map_size//2,map_size-1)
            if randint(0,100)>=chance: map_screen[y][map_size-1]=2

def crop():
    for y in range(map_size):
        for x in range(map_size):
            if x == 0 :map_screen[y][x]=0 
                #if map_screen[y][x+1] == 0:map_screen[y][x]=0
                #else: map_screen[y][x]=1
            if x == map_size-1:map_screen[y][x]=0
            if y == 0:map_screen[y][x]=0
            if y == map_size-1:map_screen[y][x]=0
    otl_print(map_screen)

def river_to_apply_river():
        for y in range(map_size):
            for x in range(map_size):
                if map_screen[y][x]==2: 
                    print()
                    map_screen[y][x]=3

def river_to_apply_water():
        for y in range(map_size):
            for x in range(map_size):
                if map_screen[y][x]==3: 
                    print()
                    map_screen[y][x]=0

def river_extend_1(): #смотерть на какое то  количество вперед и искать воду добавить шанс озер(без соприкосновением с моррем), пройтись по кромке и заполнить либо водой либо землей 
    for y in range(0,map_size):
        for  x in range(0,map_size):
            if map_screen[y][x]==2:
                if y <= map_size//2 and x <= map_size//2:
                    for y in range(0,map_size//2):
                        for x in range(0,map_size//2):
                            if map_screen[y][x]==2:
                                if randint(0,100)>=50 and map_screen[y][x+1]!=3 and map_screen[y][x+2]!=3: map_screen[y][x+1] = 2 
                                else:
                                    if map_screen[y+1][x]!=3 and map_screen[y+2][x]!=3: map_screen[y+1][x] = 2
                                    else: break

                if y <= map_size//2 and x > map_size//2:
                    for y in range(0,map_size//2):
                        for x in range(map_size-1,map_size//2,-1):
                            if map_screen[y][x]==2:
                                if randint(0,100)>=50:map_screen[y][x-1] = 2 
                                else:map_screen[y+1][x] = 2

                if y > map_size//2 and x <= map_size//2:
                    for y in range(map_size-1,map_size//2,-1):
                        for x in range(0,map_size//2):
                            if map_screen[y][x]==2:
                                if randint(0,100)>=50:map_screen[y][x+1] = 2 
                                else:map_screen[y-1][x] = 2

                if y > map_size//2 and x > map_size//2:
                    for y in range(map_size-1,map_size//2,-1):
                        for x in range(map_size-1,map_size//2,-1):
                            if map_screen[y][x]==2:
                                if randint(0,100)>=50:map_screen[y][x-1] = 2 
                                else:map_screen[y-1][x] = 2

                river_to_apply_river()

def river_extend_2():
    for y in range(map_size-2):
        for x in range(map_size-2):
            if map_screen[y][x]==2:
                if randint(0,100)>=50 and map_screen[y][x+1]!=3 and map_screen[y][x+1]!=2 and map_screen[y][x+2]!=3 and map_screen[y][x+2]!=2: 
                    map_screen[y][x+1] = 2 
                else:
                    if map_screen[y+1][x]!=3 and map_screen[y+2][x]!=3 and map_screen[y+2][x]!=2 and map_screen[y+1][x]!=2: 
                        map_screen[y+1][x] = 2
                        break
    river_to_apply_river()
#                                elif 0:
 #                                   if randint(0,100)>=50 and map_screen[y][x+1]!=3:map_screen[y][x+1] = 2
  #                                  elif map_screen[y+1][x]!=3: 
  #                                      map_screen[y+1][x] = 2
   #                                     break
    #                                else: print('osh')

#не нравиться нужно писать от истока   

def middle_earth_sea():
    river_create()



def drew_map(map_in):
    screen.fill((14,83,167)) 
    for y in range(len(map_in)):
        for x in range(len(map_in)):
            pygame.draw.rect(screen, landscape.get(map_in[y][x],(255,255,255)),(x * pixel_size, y * pixel_size, pixel_size, pixel_size))

def drew_temperature_map(map_in): #отрисовывает температурную карту нужно оптимайз 
    pygame.draw.rect(screen, landscape.get(0,(255,255,255)), (0, 0, map_size+10, map_size+10))  
    for y in range(len(map_in)):
        for x in range(len(map_in)):
            if 32<=map_in[y][x]:
                pygame.draw.rect(screen, temperature.get(0, (255, 255, 255)), (x * min_pixel_size, y * min_pixel_size, min_pixel_size, min_pixel_size))
            elif 26<=map_in[y][x]<32:
                pygame.draw.rect(screen, temperature.get(1, (255, 255, 255)), (x * min_pixel_size, y * min_pixel_size, min_pixel_size, min_pixel_size))
            elif 20<=map_in[y][x]<26:
                pygame.draw.rect(screen, temperature.get(2, (255, 255, 255)), (x * min_pixel_size, y * min_pixel_size, min_pixel_size, min_pixel_size))
            elif 14<=map_in[y][x]<20:
                pygame.draw.rect(screen, temperature.get(3, (255, 255, 255)), (x * min_pixel_size, y * min_pixel_size, min_pixel_size, min_pixel_size))
            elif 8<=map_in[y][x]<14:
                pygame.draw.rect(screen, temperature.get(4, (255, 255, 255)), (x * min_pixel_size, y * min_pixel_size, min_pixel_size, min_pixel_size))
            elif 2<=map_in[y][x]<8:
                pygame.draw.rect(screen, temperature.get(5, (255, 255, 255)), (x * min_pixel_size, y * min_pixel_size, min_pixel_size, min_pixel_size))
            elif -4<=map_in[y][x]<2:
                pygame.draw.rect(screen, temperature.get(6, (255, 255, 255)), (x * min_pixel_size, y * min_pixel_size, min_pixel_size, min_pixel_size))
            elif -10<=map_in[y][x]<-4:
                pygame.draw.rect(screen, temperature.get(7, (255, 255, 255)), (x * min_pixel_size, y * min_pixel_size, min_pixel_size, min_pixel_size))
            elif -16<=map_in[y][x]<-10:
                pygame.draw.rect(screen, temperature.get(8, (255, 255, 255)), (x * min_pixel_size, y * min_pixel_size, min_pixel_size, min_pixel_size))
            elif -22<=map_in[y][x]<-16:
                pygame.draw.rect(screen, temperature.get(9, (255, 255, 255)), (x * min_pixel_size, y * min_pixel_size, min_pixel_size, min_pixel_size))
            elif -28<=map_in[y][x]<-22:
                pygame.draw.rect(screen, temperature.get(10, (255, 255, 255)), (x * min_pixel_size, y * min_pixel_size, min_pixel_size, min_pixel_size))
            elif -34<=map_in[y][x]<-28:
                pygame.draw.rect(screen, temperature.get(11, (255, 255, 255)), (x * min_pixel_size, y * min_pixel_size, min_pixel_size, min_pixel_size))
            elif -40<=map_in[y][x]<-34:
                pygame.draw.rect(screen, temperature.get(12, (255, 255, 255)), (x * min_pixel_size, y * min_pixel_size, min_pixel_size, min_pixel_size))
            elif -46<=map_in[y][x]<-40:
                pygame.draw.rect(screen, temperature.get(13, (255, 255, 255)), (x * min_pixel_size, y * min_pixel_size, min_pixel_size, min_pixel_size))
            elif -52<=map_in[y][x]<-46:
                pygame.draw.rect(screen, temperature.get(14, (255, 255, 255)), (x * min_pixel_size, y * min_pixel_size, min_pixel_size, min_pixel_size))
            elif -58<=map_in[y][x]<-52:
                pygame.draw.rect(screen, temperature.get(15, (255, 255, 255)), (x * min_pixel_size, y * min_pixel_size, min_pixel_size, min_pixel_size))
            elif map_in[y][x]<-58:
                pygame.draw.rect(screen, temperature.get(16, (255, 255, 255)), (x * min_pixel_size, y * min_pixel_size, min_pixel_size, min_pixel_size))

def otl_print(map_in):
    print()
    for y in range(len(map_in)):
        print(str(map_in[y])[1:][:-1])

create_continent()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                print('down')
                day_night(100,(3,6,7,8),(0,1,2,5))
            elif event.key == pygame.K_UP:
                print('up')
                map_size_64()
                create_continent()
            elif event.key == pygame.K_w:
                print('w')
                day_night(1,(6,5),(0,1,2,3,4))
            elif event.key == pygame.K_z:
                print('z')
                zoom(2)
            elif event.key == pygame.K_r:
                print('r')
                middle_earth_sea()
            elif event.key == pygame.K_y:
                print('y')
                river_to_apply_water()
            elif event.key == pygame.K_c:
                print('c')
                crop()
            elif event.key == pygame.K_t:
                print('t')
                river_extend_1()
    drew_map(map_screen)
    #drew_temperature_map(map_temperature)
    pygame.display.update()
    pygame.time.Clock().tick(10)