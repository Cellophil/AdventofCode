import numpy as np
from matplotlib import pyplot as plt

form = [25,6]

with open('8.txt','r') as f:
    numbers = f.read()

    n = 0
    layers = []
    layer = np.zeros((form[0],form[1]))

    for s in numbers:
        try:
            a = np.int(s)
        except:
            continue

        layer[np.int(n%form[0]),np.int(np.floor(n/form[0]))] = np.int(s)
        n += 1
        if np.floor(n/(form[0]*form[1]))==1:
            layers.append(layer)
            layer = np.zeros((form[0],form[1]))
            n = 0

for layer in layers:
    nr0 = len(np.where(layer==0)[0])
    nr1 = len(np.where(layer==1)[0])
    nr2 = len(np.where(layer==2)[0])
    tot = nr0+nr1+nr2

    print(f'0: {nr0}, 1: {nr1}, 2: {nr2}, tot: {tot}')
    

pic = np.zeros((form[0],form[1]),int)
for i in range(form[0]):
    for j in range(form[1]):
        n = 0
        pixel = 2
        while pixel==2:
            pixel = np.int(layers[n][i,j])
            n += 1

        pic[i,j] = pixel

plt.pcolor(pic.T[::-1,:])