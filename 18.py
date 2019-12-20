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
    _field = field.copy()
    if _field[0,0] == -1:
        # distance plot
        _field[_field > 0] = 46
        _field[_field==-1] = 35
        
    for l in _field:
        print("".join([chr(item) for item in l]))

printascii(field0)

#%%
from numba import jit, int32, int16

distance_cache = {}

def pathfinder(doors,start):
    if (start[0],start[1],doors) in distance_cache:
        return distance_cache[(start[0],start[1],doors)]
    else:
        doors_num = np.array([ord(d.upper()) for d in doors])
        closed_doors = np.setdiff1d(np.arange(65,91),doors_num)
        closed_doors = closed_doors.astype(np.int16)
        startx = start[1].astype(np.int16)
        starty = start[0].astype(np.int16)

        distance = pathfinder_calc(closed_doors,startx,starty)

        distance_cache.update({(start[0],start[1],doors):distance})
        return distance


@jit(int16(int16,int16))
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

@jit(int16[:,:](int16[:],int16,int16),nopython=True,nogil=True)
def pathfinder_calc(closed_doors,startx,starty):

    stackx = [startx]
    stacky = [starty]
    distance = np.ones((81, 81),np.int16)*int16(-1)
    distance[starty,startx] = 0

    while len(stackx) > 0:
        x = stackx.pop(0)
        y = stacky.pop(0)

        for dx in np.array([-1,0,1],np.int16):
            for dy in np.array([-1,0,1],np.int16):
                if (abs(dx)+abs(dy) == int16(1)) and checkbounds(y+dy,x+dx):
                    if not (field0[y+dy,x+dx] == int16(35)): #'#'
                        for c in closed_doors:
                            if field0[y+dy,x+dx]==c:
                                break
                        else:
                            if (distance[y+dy,x+dx] > distance[y,x] + int16(1)) or (distance[y+dy,x+dx] == int16(-1)):
                                distance[y+dy,x+dx] = distance[y,x] + int16(1)
                                stackx.append(x+dx)
                                stacky.append(y+dy)
                                
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

n = 0

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

    n += 1
    if n%100 == 0:
        print(keys)

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
            if not (distance[pos[0],pos[1]] == -1):
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


        keys_branch = ''.join(sorted(keys))+a
        if keys_branch in key_step:
            if key_step[keys_branch] <= steps_branch:
                continue
        key_step.update({keys_branch:steps_branch})

        if steps_branch < done_min:
            states.append([start_branch,steps_branch,keys_left-1,keys_branch])

    

print(done_min)
# printascii(field)

# %%
field0 = np.zeros((500,500),np.int)

with open('18_2.txt','r') as f:
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

# %%

@jit(int16[:,:](int16[:],int16,int16),nopython=True,nogil=True)
def pathfinder_calc(closed_doors,startx,starty):

    stackx = [startx]
    stacky = [starty]
    distance = np.ones((81, 81),np.int16)*int16(-1)
    distance[starty,startx] = 0

    while len(stackx) > 0:
        x = stackx.pop(0)
        y = stacky.pop(0)

        for dx in np.array([-1,0,1],np.int16):
            for dy in np.array([-1,0,1],np.int16):
                if (abs(dx)+abs(dy) == int16(1)) and checkbounds(y+dy,x+dx):
                    if not (field0[y+dy,x+dx] == int16(35)): #'#'
                        for c in closed_doors:
                            if field0[y+dy,x+dx]==c:
                                break
                        else:
                            if (distance[y+dy,x+dx] > distance[y,x] + int16(1)) or (distance[y+dy,x+dx] == int16(-1)):
                                distance[y+dy,x+dx] = distance[y,x] + int16(1)
                                stackx.append(x+dx)
                                stacky.append(y+dy)
                                
    return distance

def pathfinder_multi(doors,starts):

    distance1 = pathfinder(''.join(sorted(keys)),np.array(starts[0]))
    distance2 = pathfinder(''.join(sorted(keys)),np.array(starts[1]))
    distance3 = pathfinder(''.join(sorted(keys)),np.array(starts[2]))
    distance4 = pathfinder(''.join(sorted(keys)),np.array(starts[3]))
    distance = distance1
    distance[:40,40:] = distance2[:40,40:]
    distance[40:,:40] = distance3[40:,:40]
    distance[40:,40:] = distance4[40:,40:]

    return distance


starts = [[39, 39], [39, 41], [41, 39], [41, 41]]
start = []
del start
distance_cache = {}

steps = 0
field = field0.copy()
keys_left = 26
keys = ''
key_step = {}
states = [[starts,steps,keys_left,keys]]
done_min = np.inf

n = 0

while len(states) > 0:
    heuristic = states[0][2]*300+states[0][1]
    index = 0
    for i,s in enumerate(states):
        heuristic_ = s[2]*300+s[1]
        if heuristic > heuristic_:
            index = i
            heuristic = heuristic_
    
    state = states.pop(index)
    starts = state[0]
    steps = state[1]
    keys_left = state[2]
    keys = state[3]

    n += 1
    # if n%100 == 0:
        # print(keys)

    if keys_left == 0:
        # none
        if steps < done_min:
            done_min = steps
            print(done_min)
        continue

    distance = pathfinder_multi(''.join(sorted(keys)),starts)

    # get all key positions
    access = []
    dist = []
    keys_have = [k for k in keys]
    for key in range(97,123):
        if chr(key) in keys_have:
            continue
        pos = get_pos_cache[chr(key)]
        if pos is not None:
            if not (distance[pos[0],pos[1]] == -1):
                access.append([chr(key),distance[pos[0],pos[1]]])

    while len(access) > 0:
        a = access.pop(0)
        d = a[1]
        a = a[0]

        steps_branch = steps + d
        # delete that key
        pos = get_pos_cache[a]
        if pos[0] >=40:
            if pos[1] >= 40:
                start_branch = [starts[0],starts[1],starts[2],pos]
            else:
                start_branch = [starts[0],starts[1],pos,starts[3]]
        else:
            if pos[1] >= 40:
                start_branch = [starts[0],pos,starts[2],starts[3]]
            else:
                start_branch = [pos,starts[1],starts[2],starts[3]]
        # field_branch = field.copy()
        # field_branch[pos[0],pos[1]] = ord('.')
        # # open that door
        # pos = get_pos_cache[a.upper()]
        # if pos is not None:
        #     field_branch[pos[0],pos[1]] = ord('.')


        keys_branch = ''.join(sorted(keys))+a
        # if keys_branch in key_step:
        #     if key_step[keys_branch] <= steps_branch:
        #         continue
        # key_step.update({keys_branch:steps_branch})

        if steps_branch < done_min:
            states.append([start_branch,steps_branch,keys_left-1,keys_branch])

    

print(done_min)

# %%
