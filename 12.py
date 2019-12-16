import numpy as np

pos0 = np.zeros((4,3),dtype=np.int)
pos = np.zeros((4,3),dtype=np.int)

pos0[0,0]=-10
pos0[0,1]=-10
pos0[0,2]=-13

pos0[1,0]=5
pos0[1,1]=5
pos0[1,2]=-9

pos0[2,0]=3
pos0[2,1]=8
pos0[2,2]=-16

pos0[3,0]=1
pos0[3,1]=3
pos0[3,2]=-3

pos = pos0.copy()

vel = np.zeros((4,3),dtype=np.int)

def update_vel():
    global vel, pos
    for i in range(4):
        for j in range(i+1,4):
            vel[i,:] -= np.sign(pos[i,:]-pos[j,:])
            vel[j,:] += np.sign(pos[i,:]-pos[j,:])

def update_pos():
    global vel, pos
    pos += vel

def energy():
    e = 0
    for i in range(4):
        p = np.sum(np.abs(pos[i,:]))
        k = np.sum(np.abs(vel[i,:]))
        e += p*k
    return e

for i in range(np.int(1e7)):
    update_vel()
    update_pos()
    if np.all(pos == pos0):
        print('finished',i)
        break

# print(energy())