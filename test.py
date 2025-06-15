import numpy as np

options = ['number','date of birth','age','satiety','location']
def gen_map_new_people():
    global map_people
    map_people= np.zeros((1,len(options)),dtype='int32')

tek_time = 100
loc_parents = 1

def born_people():
    global map_people
    new_row = np.array([1,tek_time,0,100,loc_parents])
    map_people = np.insert(map_people, 0, new_row, axis=0)

def get_info_people(x):
    return map_people[x]

gen_map_new_people()
born_people() 
print(get_info_people(0))

