#%%
import numpy as np

field0 = np.zeros((500,500),np.int)

with open('18.txt','r') as f:
    y = -1
    for l in f.readlines():
        y += 1
        l = l.replace('\n','')
        for i,s in enumerate(l):
            field0[y,i] = ord(s)
        
xlim = np.where(field0[0,:] == 0)[0][0]
ylim = np.where(field0[:,0] == 0)[0][0]
field0 = field0[:ylim,:][:,:xlim]

def printascii(field):
    for l in field:
        print("".join([chr(item) for item in l]))

printascii(field0)

#%%
from numba import jit, int32

@jit(int32(int32,int32))
def checkbounds(y,x):
    if x > xlim:
        return 0
    if x < 0:
        return 0
    if y > ylim:
        return 0
    if y < 0:
        return 0
    return 1

distance_cache = {}

# @jit(int32[:](int32[:],int32,int32))
def pathfinder(doors,start):

    if (start[0],start[1],doors) in distance_cache:
        return distance_cache[(start[0],start[1],doors)]

    doors_num = [ord(d.upper()) for d in doors]
    closed_doors = np.setdiff1d(np.arange(65,91),np.array(doors_num))

    startx = start[1]
    starty = start[0]
    
    stack = [[starty,startx]]
    s = np.shape(field)
    distance = np.ones(np.shape(field),np.int)+np.inf
    distance[starty,startx] = 0

    while len(stack) > 0:
        s = stack.pop(0)
        x = s[1]
        y = s[0]

        for dx in [-1,0,1]:
            for dy in [-1,0,1]:
                if (abs(dx)+abs(dy) == 1) and checkbounds(y+dy,x+dx):
                    if not (field[y+dy,x+dx] == 35): #'#'
                        if not (np.isin(field[y+dy,x+dx],closed_doors)): #closed door

                            if distance[y+dy,x+dx] > distance[y,x] + 1:
                                distance[y+dy,x+dx] = distance[y,x] + 1
                                stack.append([y+dy,x+dx])


    distance_cache.update({(start[0],start[1],doors):distance})

    return distance

# test
ind = np.where(field0==ord('@'))
start = np.array([i[0] for i in ind])
distance = pathfinder('',start)
print(distance)

# %%

def get_pos(L):
    ind = np.where(field0==ord(L))
    if len(ind[0]) > 0:
        return np.array([i[0] for i in ind],np.int)
    else:
        return None

get_pos_cache = {}
for key in range(97,123):
    get_pos_cache.update({chr(key):get_pos(chr(key))})
for key in range(65,91):
    get_pos_cache.update({chr(key):get_pos(chr(key))})



steps = 0
start = get_pos('@')
field = field0.copy()
keys_left = 26
keys = ''
key_step = {}
states = [[start,steps,keys_left,keys]]
done_min = np.inf

while len(states) > 0:
    heuristic = states[0][2]*300+states[0][1]
    index = 0
    for i,s in enumerate(states):
        heuristic_ = s[2]*300+s[1]
        if heuristic > heuristic_:
            index = i
            heuristic = heuristic_
    
    state = states.pop(index)
    start = state[0]
    steps = state[1]
    keys_left = state[2]
    keys = state[3]

    if keys_left == 0:
        # none
        if steps < done_min:
            done_min = steps
            print(done_min)
        continue

    distance = pathfinder(''.join(sorted(keys)),start)

    # get all key positions
    access = []
    dist = []
    keys_have = [k for k in keys]
    for key in range(97,123):
        if chr(key) in keys_have:
            continue
        pos = get_pos_cache[chr(key)]
        if pos is not None:
            if distance[pos[0],pos[1]] < np.inf:
                access.append([chr(key),distance[pos[0],pos[1]]])

    while len(access) > 0:
        a = access.pop(0)
        d = a[1]
        a = a[0]

        steps_branch = steps + d
        # delete that key
        pos = get_pos_cache[a]
        start_branch = pos.copy()
        # field_branch = field.copy()
        # field_branch[pos[0],pos[1]] = ord('.')
        # # open that door
        # pos = get_pos_cache[a.upper()]
        # if pos is not None:
        #     field_branch[pos[0],pos[1]] = ord('.')

        keys_branch = keys+a#''.join(sorted(keys+a))
        if keys_branch in key_step:
            if key_step[keys_branch] <= steps_branch:
                continue
        key_step.update({keys_branch:steps_branch})

        if steps_branch < done_min:
            states.append([start_branch,steps_branch,keys_left-1,keys_branch])

    

print(done_min)
# printascii(field)

# %%
