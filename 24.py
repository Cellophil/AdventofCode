import numpy as np

def pic2num(s):
    s = s.replace('\n','')
    bugs = np.zeros((7,7))
    for i in range(5):
        for j in range(5):
            if s[i*5+j] == '#':
                bugs[i+1,j+1] = 1
    return bugs

def num2pic(bugs):
    s = ''
    for i in range(5):
        for j in range(5):
            if bugs[i+1,j+1] == 1:
                s += '#'
            else:
                s += '.'
        s += '\n'
    return s


bugs = pic2num('....##..#.#..##..#..#....')

def evolve(bugs):
    _bugs = np.copy(bugs)
    neighbor = np.zeros((7,7))
    neighbor = np.roll(_bugs,1,axis=0) + \
        np.roll(_bugs,-1,axis=0) + \
        np.roll(_bugs,1,axis=1) + \
        np.roll(_bugs,-1,axis=1)

    newbugs = np.zeros((7,7))
    newbugs[neighbor==1] = 1
    newbugs[(neighbor==2) & (_bugs==0)] = 1
    
    newbugs[0,:] = 0
    newbugs[6,:] = 0
    newbugs[:,0] = 0
    newbugs[:,6] = 0
    
    return newbugs

print(num2pic(bugs))
bugs = evolve(bugs)
print(num2pic(bugs))
bugs = evolve(bugs)
print(num2pic(bugs))
bugs = evolve(bugs)

#%%
bugs = pic2num('###..#...#.#.####.#.#.###')
states = {}
while 1:
    s = num2pic(bugs).replace('\n','')
    if s in states:
        print(num2pic(bugs))
        break
    states.update({s:0})
    bugs = evolve(bugs)

# %%
def biodiv(bugs):
    _bugs = bugs[1:6,:][:,1:6]
    b = 0
    p = 1
    for i in range(5):
        for j in range(5):
            b += _bugs[i,j]*p
            p *= 2
    return b

print(biodiv(bugs))

# %%
N = 401

def evolve_rec(bugs):
    _bugs = np.copy(bugs)
    _bugs[:,0,1:6] = np.reshape(np.roll(_bugs,1,axis=0)[:,2,3],(N,1))
    _bugs[:,6,1:6] = np.reshape(np.roll(_bugs,1,axis=0)[:,4,3],(N,1))
    _bugs[:,1:6,0] = np.reshape(np.roll(_bugs,1,axis=0)[:,3,2],(N,1))
    _bugs[:,1:6,6] = np.reshape(np.roll(_bugs,1,axis=0)[:,3,4],(N,1))
    
    # temp = np.copy(_bugs)
    # _bugs[:,3,3] = np.sum(np.roll(_bugs,1,axis=0)[:,1,1:6],axis=1)
    # _bugs[:,3,3] += np.sum(np.roll(_bugs,1,axis=0)[:,5,1:6],axis=1)
    # _bugs[:,3,3] += np.sum(np.roll(_bugs,1,axis=0)[:,2:5,1],axis=1)
    # _bugs[:,3,3] += np.sum(np.roll(_bugs,1,axis=0)[:,2:5,5],axis=1)

    neighbor = np.zeros((N,7,7))
    neighbor = np.roll(_bugs,1,axis=1) + \
        np.roll(_bugs,-1,axis=1) + \
        np.roll(_bugs,1,axis=2) + \
        np.roll(_bugs,-1,axis=2)

    neighbor[:,2,3] += np.sum(np.roll(_bugs,-1,axis=0)[:,1,1:6],axis=1)
    neighbor[:,4,3] += np.sum(np.roll(_bugs,-1,axis=0)[:,5,1:6],axis=1)
    neighbor[:,3,2] += np.sum(np.roll(_bugs,-1,axis=0)[:,1:6,1],axis=1)
    neighbor[:,3,4] += np.sum(np.roll(_bugs,-1,axis=0)[:,1:6,5],axis=1)

    newbugs = np.zeros((N,7,7))
    newbugs[neighbor==1] = 1
    newbugs[(neighbor==2) & (_bugs==0)] = 1
    
    newbugs[:,0,:] = 0
    newbugs[:,6,:] = 0
    newbugs[:,:,0] = 0
    newbugs[:,:,6] = 0
    newbugs[:,3,3] = 0
    
    return newbugs


temp = pic2num('....##..#.#.?##..#..#....')
bugs = np.zeros((N,7,7))
bugs[200,:,:] = temp
for i in range(10):
    bugs = evolve_rec(bugs)

for i in range(-5,6):
    print(f'Depth {i}:')
    print(num2pic(bugs[200+i,:,:]))


bugs = np.zeros((N,7,7))
temp = pic2num('###..#...#.#.####.#.#.###')
bugs[200,:,:] = temp
for i in range(200):
    bugs = evolve_rec(bugs)
print(len(np.where(bugs==1)[0]))




# %%
