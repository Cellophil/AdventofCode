import numpy as np
from math import gcd

with open('10.txt','r') as f:
    astro_list = []
    for l in f.readlines():
        astro_list.append([s for s in l.replace('.','0').replace('#','1').replace('\n','')])

astro = np.array(astro_list,dtype=np.int)
size = np.shape(astro)
sight = np.zeros(size)

def inbounds(x,y):
    if x < size[0]:
        if x >= 0:
            if y < size[1]:
                if y >= 0:
                    return True
    return False

for i in range(size[0]):
    for j in range(size[1]):
        if astro[i,j] == 0:
            continue

        c = astro.copy()
        for L in range(1,max(size[0],size[1])):
            for i2 in range(size[0]):
                for j2 in range(size[1]):
                    if max(abs(i2-i),abs(j2-j)) == L:
                        dx = i2-i
                        dy = j2-j

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
                            
        sight[i,j] = len(np.where(c==1)[0]) - 1

ind = np.argmax(sight)
y = ind%size[1]
x = np.int(np.floor(ind/size[1]))
print(f'best position: x={x}, y={y}')
print(sight[x,y])

astro[x,y] = 2
astro0 = astro.copy()