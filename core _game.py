import pygame
import numpy as np
import pygame_gui
from random import*
import sys

#сукаебаный гит как ты заебал
#dla div

#Fixedsys
#Verdana
#Consolas

time_over_clock=0
size_pixel = 10
red = (230, 0, 0)
map_size=5
need_eat=2


num = [[[1, 1, 1],
      [1, 0, 1],
      [1, 0, 1],
      [1, 0, 1],
      [1, 1, 1]],
     [[0, 1, 0],
      [0, 1, 0],
      [0, 1, 0],
      [0, 1, 0],
      [0, 1, 0]],
     [[1, 1, 1],
      [0, 0, 1],
      [1, 1, 1],
      [1, 0, 0],
      [1, 1, 1]],
     [[1, 1, 1],
      [0, 0, 1],
      [0, 1, 0],
      [0, 0, 1],
      [1, 1, 1]],
     [[1, 0, 1],
      [1, 0, 1],
      [1, 1, 1],
      [0, 0, 1],
      [0, 0, 1]],
     [[1, 1, 1],
      [1, 0, 0],
      [1, 1, 1],
      [0, 0, 1],
      [1, 1, 1]],
     [[1, 1, 1],
      [1, 0, 0],
      [1, 1, 1],
      [1, 0, 1],
      [1, 1, 1]],
     [[1, 1, 1],
      [0, 0, 1],
      [0, 0, 1],
      [0, 0, 1],
      [0, 0, 1]],
     [[1, 1, 1],
      [1, 0, 1],
      [1, 1, 1],
      [1, 0, 1],
      [1, 1, 1]],
     [[1, 1, 1],
      [1, 0, 1],
      [1, 1, 1],
      [0, 0, 1],
      [1, 1, 1]]]
def test_strok():
    a = '1'
    for text_test in range(2,33):# по идее 32 столца 
        a=a+str(text_test)
    test_strok = font_big.render(a, True, (0, 255, 0))
    for i in range(23): #23 строки 23 часы 
        window.blit(test_strok,(2,i*30))

#target_actions
map_actions = []
map_actions.append('|planting crops|')
map_actions.append('|f1|')
map_actions.append('|f2|')

def draw_target_actions():
    for x in range(len(map_actions)):
        block_map_actions = font_small.render(str(map_actions[x])[2:len(map_actions[x])-3], True, (0,0,0))
        window.blit(block_map_actions,(1,650))

# механика еды:
# м3 -> 3кг пшеницы
# клетка 10га
# 1 чел 0.3га 
# первобытном общине не 150 чел

def gen_map_eat():
    global map_eat
    map_eat= np.zeros((map_size,map_size),dtype='int32')
    global map_planting_crops
    map_planting_crops= np.zeros((map_size,map_size),dtype='int16')
    for x in range(map_size):
        for y in range(map_size):
            map_eat[x][y] = randint(24,25)

gen_map_eat()

def draw_map_eat_old(map_eat):
    for y in range(map_size):
        for x in range(map_size):
            block_map_out = font_small.render(str(map_eat[y][x]), True, (0,0,0))
            window.blit(block_map_out,(15*1+x*15*10,y*20*4+20*2))

def update_eat_old(map_eat):
    for y in range(map_size):
        for x in range(map_size):
            map_eat[y][x]=map_eat[y][x]+randint(25,35)
            if map_eat[y][x]<0:map_eat[y][x]=0\
            
def eat_planting_crops(): # посадка урожая
    if map_city[get_target_cursor()[0]][get_target_cursor()[1]] == 0 :
        map_planting_crops[get_target_cursor()[0]][get_target_cursor()[1]]=1
    else: print('ti dolbaeb ti ne mojesh zasadit gorot')

def eat_update_crops(): # обновление урожая
    for y in range(len(map_planting_crops)):
        for x in range(len(map_planting_crops[y])):
            if map_planting_crops[y][x]>0:
                map_planting_crops[y][x]=map_planting_crops[y][x]+1
            if map_planting_crops[y][x] >= 30*5 :
                map_planting_crops[y][x] = 0
                map_eat[y][x]+=30000 #*randint(1,100)/100
          
# механика город:
# необходим клеточный автомат 

def gen_map_city():
    global map_city
    map_city= np.zeros((map_size,map_size),dtype='int8')
    global map_id
    map_id= np.zeros((map_size,map_size),dtype='int16')
    for y in range(len(map_city)):
        for x in range(len(map_city[y])):
            map_city[x][y] = randint(0,1)
    map_id = [[i * map_size + j + 1 for j in range(map_size)] for i in range(map_size)]
      
gen_map_city()

def draw_city(map_city):
    for y in range(len(map_city)):
        for x in range(len(map_city[y])):
            if map_city[y][x] == 1:
                ans = "гор"
            else:
                ans = "пол"
            block_map_out = font_small.render((str(ans)), True, (0,0,0))
            window.blit(block_map_out,(15*1+x*15*10,y*20*4+20*1))

#голод

def hunger_update():
    print('hunger update')
    for y in range(map_size):
        for x in range(map_size):
            if map_eat[y][x] < need_eat * map_kol_people[y][x]: # проверка на голодающих
                
                map_kol_people_hunger[y][x]=(map_kol_people[y][x] - map_eat[y][x]/need_eat) # считаем голодных
                map_kol_day_hunger[y][x]+=1 # количество дней голда 
                map_percent_people_hunger[y][x]=((map_kol_people_hunger[y][x]/map_kol_people[y][x])*100000)//10/100 # процент голодных
                def_hunger=(0.1*map_kol_day_hunger[y][x])*100//10/10 # функция голода на выходе проценты 
                map_kol_people_death[y][x]=0.5*map_percent_people_hunger[y][x]*def_hunger*map_kol_people[y][x]//100 # перемножаем количество людишек на проценты получаем кол убыли

                minus_kol_people(map_kol_people_death[y][x],y,x) # вычитаем людей из матрицы 
                minus_eat_quantity(need_eat * map_kol_people[y][x],y,x) # вычитаем еду из матрицы

                if 1: # отладка \ логи
                    print('id',map_id[y][x],'kph',map_kol_people_hunger[y][x],'kp',map_kol_people[y][x],
                          '%h',map_percent_people_hunger[y][x],'fh',def_hunger,'dp',map_kol_people_death[y][x])

            else: # вычитаем еду для тех кого голод не коснулся 
                minus_eat_quantity(need_eat * map_kol_people[y][x],y,x) # вычитаем еду из матрицы
                map_kol_day_hunger[y][x]=0 # обнуление счётчика дней голода так как все сыты
    print("hunger updated")

# нужно наверное обьеденить
# нужно доделать функцию на практике, сдеалть тест мод            

#количество людей
def gen_map_kol_people(): #нужно сделать ген фор страт гейм и слить все сюда
    global map_kol_people #матрица кол людишек
    map_kol_people= np.zeros((map_size,map_size),dtype='int32')
    for y in range(len(map_kol_people)):
        for x in range(len(map_kol_people[y])):
            map_kol_people[y][x] = randint(10,15)

    global map_cursor_target # матрица для выделенной в текущий момент
    map_cursor_target = np.zeros((map_size,map_size),dtype='int16')
    map_cursor_target[0][0]=1
    #global map_hunger # матрица для голода
    #map_hunger = np.zeros((map_size,map_size),dtype='int8')
    global map_kol_day_hunger # матрица для количества дней голода
    map_kol_day_hunger = np.zeros((map_size,map_size),dtype='int8')
    global map_kol_people_death # матрица для количества смертей
    map_kol_people_death = np.zeros((map_size,map_size),dtype='int32')
    global map_percent_people_hunger # матрица для процент голодных
    map_percent_people_hunger = np.zeros((map_size,map_size),dtype='int32')
    global map_kol_people_hunger # матрица для количества голодных
    map_kol_people_hunger = np.zeros((map_size,map_size),dtype='int32')

def born_update_people(): # функция рождаемости  
    for y in range(map_size):
        for x in range(map_size): # настроить типы клеток 
            if map_city[y][x] == 1 and map_percent_people_hunger[y][x] <= 10: # люди рождаются только в городе при голоде менее 10%
                plus_kol_people(randint(2,map_kol_people[y][x]),y,x) #вызов функции увеличения людей 
                # дописать функцию

def minus_kol_people(kol,y,x):
    if map_kol_people[y][x]-kol>0: 
        map_kol_people[y][x]=map_kol_people[y][x]-kol
    elif map_kol_people[y][x]-kol<=0:
        map_kol_people[y][x]=0

def plus_kol_people(kol,y,x):
    map_kol_people[y][x]=map_kol_people[y][x]+kol

def minus_eat_quantity(kol,y,x):
    if map_eat[y][x]-kol>0: 
        map_eat[y][x]=map_eat[y][x]-kol
    elif map_eat[y][x]-kol<=0:
        map_eat[y][x]=0

def plus_eat_quantity(kol,y,x):
    map_eat[y][x]=map_eat[y][x]+kol
    
def draw_kol_people(map_kol_people):
    for y in range(len(map_kol_people)):
        for x in range(len(map_kol_people[y])):
            block_map_out = font_small.render((str(map_kol_people[y][x])), True, (0,0,0))
            window.blit(block_map_out,(15*8+x*15*10,y*20*4+20*3))

gen_map_kol_people()

def gen_block_map():
    global block_map
    block_map= np.zeros((map_size, map_size),dtype='int32')

def draw_block_map_v5():
    flag_color=True
    tab=[("+---------+"),
         ("|         |"),
         ("|         |"),
         ("|         |"),
         ("+---------+"),
         [9*15,4*20]]
    for y in range(map_size):
        for x in range(map_size):
            for strok in range(len(tab)-1):
                block_map_out = font_small.render(str(tab[strok]), True, (0,0,0))
                window.blit(block_map_out,(15*x+tab[-1][0]*x,strok*20+tab[-1][1]*y))
            if get_target_cursor() == (y,x):
                num_id = font_small.render(str(map_id[y][x]), True, (0,200,0))
                window.blit(num_id,(15*x+tab[-1][0]*x+5*15,strok*20+tab[-1][1]*y-4*15))
            else:
                num_id = font_small.render(str(map_id[y][x]), True, (0,0,0))
                window.blit(num_id,(15*x+tab[-1][0]*x+5*15,strok*20+tab[-1][1]*y-4*15))

def get_target_cursor():
    for y in range(len(map_cursor_target)):
        for x in range(len(map_cursor_target[y])):
            if map_cursor_target[y][x] == 1:return (y,x)

def zero_map_cursor():
    for y in range(len(map_cursor_target)):
        for x in range(len(map_cursor_target[y])):
            map_cursor_target[y][x]=0

def draw_block_dop_info():

    y = get_target_cursor()[0]
    x = get_target_cursor()[1]

    info_strok_full=[('id:'+ str(map_id[y][x])),
                     ('population:'+ str(map_kol_people[y][x])),
                     ('population growth:'),
                     ('population hunger:' + str(map_kol_people_hunger[y][x])),
                     ('percent hunger' + str(map_percent_people_hunger[y][x])),
                     ('food quantity:'+ str(map_eat[y][x])),
                     ('food progress:'+ str(map_planting_crops[y][x])),
                     ('death:'+ str(map_kol_people_death[y][x])),
                     ('type:'+str(map_city[y][x]))]
    
    info_strok_cuts=[('id:'+ str(map_id[y][x])),
                     ('pop:'+str(map_kol_people[y][x])),
                     ('pop gr:'),
                     ('pop h-r:' + str(map_kol_people_hunger[y][x])),
                     ('perc h-r:' + str(map_percent_people_hunger[y][x])),
                     ('f qua:'+ str(map_eat[y][x])),
                     ('f prog:'+ str(map_planting_crops[y][x])),
                     ('d h-r:'+ str(map_kol_day_hunger[y][x])),
                     ('death:'+ str(map_kol_people_death[y][x])),
                     ('type:'+ str(map_city[y][x]))]
    
    for strok in range(len(info_strok_cuts)):
        dop_info_block = font_small.render(str(info_strok_cuts[strok]), True, (0,0,0))
        window.blit(dop_info_block,(800,4+strok*20))   

def num0(x_cord,y_cord,img,kol_str):
    if 1:
        for j in range(len(img)):
            for i in range(len(img[0])):
                if img[j][i]==1:
                    vnut_y=(size_pixel*(y_cord+j))
                    vnut_x = ((i-1+x_cord)*size_pixel)+(size_pixel*4*kol_str)
                    pygame.draw.rect(window, red, (vnut_x, vnut_y, size_pixel, size_pixel))
#для 1 написать особое прилегание

window_size = (1080,720)
window = pygame.display.set_mode(window_size)

def clock_base(time_sec_in):
    time_hour=time_sec_in//60//60
    time_min=time_sec_in//60-(60*time_hour)
    time_sec=time_sec_in-(60*time_min)-(60*60*time_hour)
    return (str(time_hour)+':'+str(time_min)+':'+str(time_sec))
    

pause_flag=not True
def time_start(time_over_clock):
    clock_ex = font_big.render(clock_base(time_over_clock), True, (0, 255, 0))
    window.blit(clock_ex,(2, 720-44))


pygame.init()

clock = pygame.time.Clock()
#font_big = pygame.font.SysFont("Verdana", 30)
font_big = pygame.font.Font('Fixedsys.ttf', 50)
font_small = pygame.font.Font('Fixedsys.ttf', 30)

clock_delay=0
time_over=0
blink_console_time=0
blink_console=True

#консоль 
box_console = pygame.Rect(150, 683, 600, 40) # прямоугольник для колизии и отрисовки
text_console = '' # текст для отрисовки 
active_console = False # активация консолиz
def draw_console_text():
    txt_surface = font_small.render(text_console, True, (0,0,0))
    window.blit(txt_surface, (box_console.x, box_console.y))


gen_block_map()
while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN and active_console == True:
                if event.key == pygame.K_RETURN:
                    print(text_console)# Обработка введенного текста
                    if text_console== 'planting crops' or text_console== 'pl cr':
                        eat_planting_crops() 
                    text_console = ''
                    active_console = not active_console
                elif event.key == pygame.K_BACKSPACE:
                    text_console = text_console[:-1]
                else:
                    text_console += event.unicode

        elif event.type == pygame.KEYDOWN and active_console == False: #в случае нажатия конопки
            if event.key == pygame.K_SPACE \
                and active_console == False :
                if pause_flag==False:
                    pause_flag= not pause_flag
                else:
                    pause_flag= not pause_flag

                #[y][x]
            elif event.key == pygame.K_w:
                old_pos=get_target_cursor()
                zero_map_cursor()
                if int(old_pos[0])-1<0:
                    map_cursor_target[map_size-1][old_pos[1]]=1 
                else:
                    map_cursor_target[old_pos[0]-1][old_pos[1]]=1
                

            elif event.key == pygame.K_s:
                old_pos=get_target_cursor()
                zero_map_cursor()
                if int(old_pos[0])+1>map_size-1:
                    map_cursor_target[0][old_pos[1]]=1
                else:
                    map_cursor_target[old_pos[0]+1][old_pos[1]]=1

            elif event.key == pygame.K_a:
                old_pos=get_target_cursor()
                zero_map_cursor()
                if int(old_pos[1])-1<0:
                    map_cursor_target[old_pos[0]][map_size-1]=1
                else:
                    map_cursor_target[old_pos[0]][old_pos[1]-1]=1

            elif event.key == pygame.K_d:
                old_pos=get_target_cursor()
                zero_map_cursor()
                if int(old_pos[1])+1>map_size-1:
                    map_cursor_target[old_pos[0]][0]=1
                else:
                    map_cursor_target[old_pos[0]][old_pos[1]+1]=1
            elif event.key == pygame.K_RETURN:
                active_console = not active_console

        if event.type == pygame.MOUSEBUTTONDOWN:# в случаее нажатия мышки 
            if box_console.collidepoint(event.pos):
                active_console = not active_console
            else:
                active_console = False

    time_over+=1
    if pause_flag == True:
        time_over_clock+=1

    if pause_flag == True:
        if time_over-clock_delay >= 100:
            clock_delay=time_over
            #update_kol_people(map_kol_people)
            eat_update_crops()
            hunger_update()
            print('update')
            #update_eat(map_eat)
    
    
    clock.tick(10)
    window.fill((255, 255, 255)) 
    draw_block_map_v5()   
    draw_city(map_city)
    draw_kol_people(map_kol_people)
    #draw_target_actions()
    #draw_map_eat(map_eat)
    draw_block_dop_info()
    time_start(time_over_clock)

# консоль
    if active_console:
        pygame.draw.rect(window, (0,0,0), (150, 720-5,1080-150,3))
        if time_over-blink_console_time >= 15:
            blink_console_time=time_over
            blink_console = not blink_console
        if blink_console:
            pygame.draw.rect(window, (0,0,0), (150+15*len(text_console), 683,15,30))

    draw_console_text()
    pygame.display.flip()

