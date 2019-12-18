import numpy as np
from math import gcd

if 0:
    astro = astro0.copy()
else:
    with open('10.txt','r') as f:
        astro_list = []
        for l in f.readlines():
            astro_list.append([s for s in l.replace('.','0').replace('X','2').replace('#','1').replace('\n','')])

    astro = np.array(astro_list,dtype=np.int)

size = np.shape(astro)
sight = np.zeros(size)

astrorev = np.zeros((size[1],size[0]))
for i in range(size[1]):
    for j in range(size[0]):
        astrorev[i,j] = astro[j,i]
# astrorev = astro.copy()

del astro
size = np.shape(astrorev)

def inbounds(x,y):
    if x < size[0]:
        if x >= 0:
            if y < size[1]:
                if y >= 0:
                    return True
    return False

if len(np.where(astrorev==2)[0]):
    stationx = np.where(astrorev==2)[0][0]
    stationy = np.where(astrorev==2)[1][0]
else:
    stationy=27 # i
    stationx=19 # j

# get order
alpha = np.zeros(size)
for x in range(size[0]):
    for y in range(size[1]):
        # if y-stationy == 0:
        #     alpha[x,y] = np.pi/2*np.sign(j-stationj)
        # else:
        alpha[x,y] = np.arctan2(y-stationy,x-stationx)

alpha *= 360/2/np.pi
alpha += 90
alpha = np.mod(alpha+360,360)
# alpha *= -1 
s = np.argsort(alpha.ravel())
sx = np.ndarray.astype(np.floor(s/size[1]),np.int)
sy = np.mod(s,size[1])

# for z in range(40):
#     print(f'x={sx[z]},y={sy[z]}')

# each round
hit = 0
c = astrorev*0
while 1:

    if len(np.where(c==1)[0]) == 0: # new rotation
        c = astrorev.copy()
        for L in range(1,max(size[0],size[1])):
            for i2 in range(size[0]):
                for j2 in range(size[1]):
                    if max(abs(i2-stationx),abs(j2-stationy)) == L:
                        dx = i2-stationx
                        dy = j2-stationy

                        if dx==0:
                            dy = np.sign(dy)
                        if dy==0:
                            dx = np.sign(dx)

                        d = gcd(abs(dx),abs(dy))
                        dx = np.int(dx/d)
                        dy = np.int(dy/d)
                        
                        if c[i2,j2] == 1:
                            cx = i2 + dx
                            cy = j2 + dy

                            while inbounds(cx,cy):
                                c[cx,cy] = 0
                                cx += dx
                                cy += dy

        astrorev -= c

        if len(np.where(c==1)[0]) == 0:
            print('finished')
            break

    for coords in zip(sx,sy):
        x = coords[0]
        y = coords[1]
        if c[x,y] == 1:
            c[x,y] = 0
            hit += 1
            if hit == 200:
                print('hit 200:')
                print(x,y)
                
