#%%
import numpy as np

field0 = np.zeros((500,500),np.int)
with open('20.txt','r') as f:
    y = -1
    for l in f:
        y += 1
        l = l.replace('\n','')

        for i,s in enumerate(l):
            field0[y,i] = ord(s)
        
xlim = np.where(field0[0,:] == 0)[0][0]
ylim = np.where(field0[:,0] == 0)[0][0]
field0 = field0[:ylim+1,:][:,:xlim]
field0[-1,:] = 32

def printascii(field):
    _field = field.copy()
    if (_field[0,0] == -1) or np.any(field > 128):
        # distance plot
        _field[_field > 0] = 46
        _field[_field==-1] = 35
        _field[np.isinf(field)] = 37
    _field[_field==32] = 58
    
    for l in _field:
        print("".join([chr(np.int(item)) for item in l]))

field0
printascii(field0)

#%%
field = field0.copy()
portals_pos = np.where(\
    (field>=65) & (field <=90) &\
    (np.roll(field,1,axis=1)>=65) & (np.roll(field,1,axis=1) <=90) &\
    (np.roll(field,2,axis=1)==46))
portals_pos = np.vstack(portals_pos).T
portals = [[p[0],p[1]-2,chr(field[p[0],p[1]-1])+chr(field[p[0],p[1]])] for p in portals_pos]

portals_pos = np.where(\
    (field>=65) & (field <=90) &\
    (np.roll(field,-1,axis=1)>=65) & (np.roll(field,-1,axis=1) <=90) &\
    (np.roll(field,-2,axis=1)==46))
portals_pos = np.vstack(portals_pos).T
portals2 = [[p[0],p[1]+2,chr(field[p[0],p[1]])+chr(field[p[0],p[1]+1])] for p in portals_pos]

portals_pos = np.where(\
    (field>=65) & (field <=90) &\
    (np.roll(field,1,axis=0)>=65) & (np.roll(field,1,axis=0) <=90) &\
    (np.roll(field,2,axis=0)==46))
portals_pos = np.vstack(portals_pos).T
portals3 = [[p[0]-2,p[1],chr(field[p[0]-1,p[1]])+chr(field[p[0],p[1]])] for p in portals_pos]

portals_pos = np.where(\
    (field>=65) & (field <=90) &\
    (np.roll(field,-1,axis=0)>=65) & (np.roll(field,-1,axis=0) <=90) &\
    (np.roll(field,-2,axis=0)==46))
portals_pos = np.vstack(portals_pos).T
portals4 = [[p[0]+2,p[1],chr(field[p[0],p[1]])+chr(field[p[0]+1,p[1]])] for p in portals_pos]

portals.extend(portals2)
portals.extend(portals3)
portals.extend(portals4)

portal_dict = {}
for p in portals:
    key = (p[0],p[1])
    for p2 in portals:
        if (p2[2] == p[2]) & ~(p2[0] == p[0]) & ~(p2[1] == p[1]):
            portal_dict.update({key:(p2[0],p2[1])})

for p in portals:
    if p[2] == 'AA':
        start = (p[0],p[1])
    if p[2] == 'ZZ':
        end = (p[0],p[1])

letters = {}
for p in portals:
    letters.update({(p[0],p[1]) : p[2]})

# %%
start = (start)
stack = [start]
s = np.shape(field)
MAX_LVL = 10
distance = np.ones((s[0],s[1]))*np.inf
distance[stack[0][0],stack[0][1]] = 0
path = {}

while len(stack) > 0:
    s = stack.pop()
    x = s[1]
    y = s[0]
    
    for d in [[-1,0],[1,0],[0,-1],[0,1]]:
        if field[y+d[0],x+d[1]] == 46:
            if distance[y+d[0],x+d[1]] > distance[y,x]+1:
                distance[y+d[0],x+d[1]] = distance[y,x]+1
                path.update({(y+d[0],x+d[1]):s})
                stack.append((y+d[0],x+d[1]))
    if s in portal_dict:
        warp = portal_dict[s]
        if field[warp[0],warp[1]] == 46:
            if distance[warp[0],warp[1]] > distance[y,x]+1:
                distance[warp[0],warp[1]] = distance[y,x]+1
                path.update({(warp[0],warp[1]):s})
                stack.append((warp[0],warp[1]))

# printascii(distance)
print(distance[end[0],end[1]])

# %%
start = (start[0],start[1],0)
stack = [start]
s = np.shape(field)
MAX_LVL = 30
distance = np.ones((s[0],s[1],MAX_LVL))*np.inf
distance[stack[0][0],stack[0][1],0] = 0

outer = {}
s = np.shape(field)
for p in portals:
    if (p[0] == 2) or (p[0] == s[0]-4) or (p[1] == 2) or (p[1] == s[1]-3):
        outer.update({(p[0],p[1]):-1})
    else:
        outer.update({(p[0],p[1]):1})

# for o in outer.keys():
#     print(o,outer[o],letters[o])

path = {}
while len(stack) > 0:
    s = stack.pop()
    x = s[1]
    y = s[0]
    lvl = s[2]

    for d in [[-1,0],[1,0],[0,-1],[0,1]]:
        if field[y+d[0],x+d[1]] == 46:
            if distance[y+d[0],x+d[1],lvl] > distance[y,x,lvl]+1:
                distance[y+d[0],x+d[1],lvl] = distance[y,x,lvl]+1
                stack.append((y+d[0],x+d[1],lvl))
                path.update({(y+d[0],x+d[1],lvl):s})

    if (s[0],s[1]) in portal_dict:
        warp = portal_dict[(s[0],s[1])]
        o = outer[(s[0],s[1])]

        if (lvl+o >= 0) & (lvl+o < MAX_LVL):
            if field[warp[0],warp[1]] == 46:
                if distance[warp[0],warp[1],lvl+o] > distance[y,x,lvl]+1:
                    distance[warp[0],warp[1],lvl+o] = distance[y,x,lvl]+1
                    stack.append((warp[0],warp[1],lvl+o))
                    path.update({(warp[0],warp[1],lvl+o):s})

# printascii(distance)

s = (end[0],end[1],0)
while s in path:
    s0 = s
    lvl = s[2]
    s = path[s]
    newlvl = s[2]
    if not (lvl==newlvl):
        print(s0, '<--', s, letters[(s[0],s[1])])

print(distance[end[0],end[1],0])

# cfield = field.copy()
# s = (start[0],start[1])
# while s in path:
#     cfield[s[0],s[1]] = 112
#     s = path[s]

# printascii(cfield)

#%%

