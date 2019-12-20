#%%

import numpy as np
import Intcode
from matplotlib import pyplot as plt

c = Intcode.intcomputer('109,424,203,1,21102,1,11,0,1106,0,282,21101,18,0,0,1105,1,259,2101,0,1,221,203,1,21101,0,31,0,1105,1,282,21101,38,0,0,1105,1,259,21001,23,0,2,22101,0,1,3,21102,1,1,1,21101,57,0,0,1106,0,303,2102,1,1,222,20102,1,221,3,20102,1,221,2,21101,0,259,1,21102,80,1,0,1105,1,225,21102,1,130,2,21102,1,91,0,1106,0,303,2101,0,1,223,21002,222,1,4,21102,259,1,3,21102,1,225,2,21101,0,225,1,21102,1,118,0,1106,0,225,21002,222,1,3,21101,0,106,2,21102,1,133,0,1106,0,303,21202,1,-1,1,22001,223,1,1,21101,148,0,0,1105,1,259,2102,1,1,223,20101,0,221,4,20102,1,222,3,21102,1,19,2,1001,132,-2,224,1002,224,2,224,1001,224,3,224,1002,132,-1,132,1,224,132,224,21001,224,1,1,21101,195,0,0,106,0,109,20207,1,223,2,20101,0,23,1,21102,-1,1,3,21101,0,214,0,1105,1,303,22101,1,1,1,204,1,99,0,0,0,0,109,5,1201,-4,0,249,21201,-3,0,1,21202,-2,1,2,21201,-1,0,3,21102,1,250,0,1105,1,225,22102,1,1,-4,109,-5,2106,0,0,109,3,22107,0,-2,-1,21202,-1,2,-1,21201,-1,-1,-1,22202,-1,-2,-2,109,-3,2106,0,0,109,3,21207,-2,0,-1,1206,-1,294,104,0,99,21201,-2,0,-2,109,-3,2105,1,0,109,5,22207,-3,-4,-1,1206,-1,346,22201,-4,-3,-4,21202,-3,-1,-1,22201,-4,-1,2,21202,2,-1,-1,22201,-4,-1,1,22102,1,-2,3,21102,343,1,0,1105,1,303,1105,1,415,22207,-2,-3,-1,1206,-1,387,22201,-3,-2,-3,21202,-2,-1,-1,22201,-3,-1,3,21202,3,-1,-1,22201,-3,-1,2,21201,-4,0,1,21101,384,0,0,1106,0,303,1106,0,415,21202,-4,-1,-4,22201,-4,-3,-4,22202,-3,-2,-2,22202,-2,-4,-4,22202,-3,-2,-3,21202,-4,-1,-2,22201,-3,-2,1,21201,1,0,-4,109,-5,2106,0,0')

field = np.ones((50,50),np.int)-1
y = 0
x = 0

def getxy(x,y):
    c.reset()
    c.step_until()
    c.put_input(x)
    c.put_input(y)
    c.step_until()
    c.step_until()

    return(np.int(c.get_output()))

while c.ACTIVE:
    c.step_until()

    if c.REQUIRE_INPUT:
        c.put_input(x)
        c.put_input(y)
        c.step_until()
        c.step_until()
        
        if c.OUTPUT_AVAILABLE:
            field[y,x] = c.get_output()
            x += 1
            if x > 49:
                x = 0
                y += 1

    if ~c.ACTIVE:
        c.reset()

    if (x==49) and (y==49):
        break

def printascii(field):
    _field = field.copy()
    if np.amax(_field) < 5:
        # distance plot
        _field[_field == 0] = 46
        _field[_field == 1] = 43
        _field[_field == 2] = 111
        _field[_field == 3] = 61
        _field[_field == 4] = 38
        _field[_field==-1] = 35
        
    for l in _field:
        print("".join([chr(item) for item in l]))

printascii(field)

print(len(np.where(field==1)[0]))

#%%

testy = np.int(np.round(50/7*100*2))
testx = np.int(np.round(45/50*testy))

print(getxy(testx,testy))

def get_cross(x,y):
    if getxy(x,y) == 0:
        return [-1,-1,-1,-1]

    _x = x
    _y = y
    while 1:
        if getxy(_x,_y) == 0:
            break
        _x += 1
    upperx = _x
    _x = x
    _y = y
    while 1:
        if getxy(_x,_y) == 0:
            break
        _y += 1
    uppery = _y
    _x = x
    _y = y
    while 1:
        if getxy(_x,_y) == 0:
            break
        _x -= 1
    lowerx = _x
    _x = x
    _y = y
    while 1:
        if getxy(_x,_y) == 0:
            break
        _y -= 1
    lowery = _y

    return [upperx,uppery,lowerx,lowery]

testx = 1261
testy = 1391
upperx,uppery,lowerx,lowery = get_cross(testx,testy)

test = [testx,uppery]

while getxy(test[0]+99,test[1]-99):
    print(test)
    new = test.copy()
    new[1] -= 1
    while getxy(new[0]-1,new[1]):
        new[0] -= 1
    if getxy(new[0]+99,new[1]-99):
        test = new.copy()
    else:
        break

print(test)
print(getxy(test[0]+99,test[1]-99) & getxy(test[0],test[1]))
print(getxy(test[0]+99-1,test[1]-99) & getxy(test[0]-1,test[1]))
print(getxy(test[0]+99,test[1]-99-1) & getxy(test[0],test[1]-1))

testx = 1261
testy = 1391
upperx,uppery,lowerx,lowery = get_cross(testx,testy)

test = [upperx,testy]

while getxy(test[0]-99,test[1]+99):
    print(test)
    new = test.copy()
    new[0] -= 1
    while getxy(new[0],new[1]-1):
        new[1] -= 1
    if getxy(new[0]-99,new[1]+99):
        test = new.copy()
    else:
        break

print(test)
print(getxy(test[0]-99,test[1]+99) & getxy(test[0],test[1]))
print(getxy(test[0]-99-1,test[1]+99) & getxy(test[0]-1,test[1]))
print(getxy(test[0]-99,test[1]+99-1) & getxy(test[0],test[1]-1))

print('final')
test = [1122,1248]

print(getxy(test[0],test[1]))
print(getxy(test[0]+99,test[1]))
print(getxy(test[0],test[1]+99))
print(getxy(test[0]+99,test[1]) & getxy(test[0],test[1]+99))

print(getxy(test[0]+99-1,test[1]-1) & getxy(test[0]-1,test[1]+99-1))
print(getxy(test[0]+99-1,test[1]) & getxy(test[0]-1,test[1]+99))
print(getxy(test[0]+99,test[1]-1) & getxy(test[0],test[1]+99-1))
print(getxy(test[0]+99-1,test[1]+1) & getxy(test[0]-1,test[1]+99+1))
print(getxy(test[0]+99+1,test[1]-1) & getxy(test[0]+1,test[1]+99-1))
print(getxy(test[0]+99+1,test[1]) & getxy(test[0]+1,test[1]+99))
print(getxy(test[0]+99,test[1]+1) & getxy(test[0],test[1]+99+1))
print(getxy(test[0]+99+1,test[1]+1) & getxy(test[0]+1,test[1]+99+1))

print(test[0]*10000+test[1])

# %%
