import numpy as np

input0 = [3,8,1005,8,311,1106,0,11,0,0,0,104,1,104,0,3,8,1002,8,-1,10,101,1,10,10,4,10,108,0,8,10,4,10,1002,8,1,28,2,103,7,10,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,1,10,4,10,1001,8,0,55,2,3,6,10,1,101,5,10,1,6,7,10,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,0,10,4,10,1001,8,0,89,1,1108,11,10,2,1002,13,10,1006,0,92,1,2,13,10,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,0,10,4,10,101,0,8,126,3,8,1002,8,-1,10,101,1,10,10,4,10,108,1,8,10,4,10,1002,8,1,147,1,7,0,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,0,8,10,4,10,101,0,8,173,1006,0,96,3,8,102,-1,8,10,101,1,10,10,4,10,108,0,8,10,4,10,1001,8,0,198,1,3,7,10,1006,0,94,2,1003,20,10,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,1,10,4,10,102,1,8,232,3,8,102,-1,8,10,101,1,10,10,4,10,108,1,8,10,4,10,102,1,8,253,1006,0,63,1,109,16,10,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,1,10,4,10,101,0,8,283,2,1107,14,10,1,105,11,10,101,1,9,9,1007,9,1098,10,1005,10,15,99,109,633,104,0,104,1,21102,837951005592,1,1,21101,328,0,0,1105,1,432,21101,0,847069840276,1,21101,0,339,0,1106,0,432,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21102,179318123543,1,1,21102,386,1,0,1106,0,432,21102,1,29220688067,1,21102,1,397,0,1106,0,432,3,10,104,0,104,0,3,10,104,0,104,0,21102,709580567396,1,1,21102,1,420,0,1105,1,432,21102,1,868498694912,1,21102,431,1,0,1106,0,432,99,109,2,22101,0,-1,1,21101,40,0,2,21101,0,463,3,21101,0,453,0,1105,1,496,109,-2,2106,0,0,0,1,0,0,1,109,2,3,10,204,-1,1001,458,459,474,4,0,1001,458,1,458,108,4,458,10,1006,10,490,1102,1,0,458,109,-2,2105,1,0,0,109,4,1202,-1,1,495,1207,-3,0,10,1006,10,513,21102,0,1,-3,21201,-3,0,1,21202,-2,1,2,21101,0,1,3,21101,0,532,0,1106,0,537,109,-4,2106,0,0,109,5,1207,-3,1,10,1006,10,560,2207,-4,-2,10,1006,10,560,22102,1,-4,-4,1105,1,628,21201,-4,0,1,21201,-3,-1,2,21202,-2,2,3,21101,0,579,0,1105,1,537,22101,0,1,-4,21102,1,1,-1,2207,-4,-2,10,1006,10,598,21102,1,0,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,620,22102,1,-1,1,21101,0,620,0,106,0,495,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2106,0,0]

def execute():
    global pos, FLAGS, BASE
    s = str(input[pos])
    for l in range(5-len(s)):
        s = '0'+s
    opcode = np.int(s[3:5])
    mod1 = np.int(s[2])
    mod2 = np.int(s[1])
    mod3 = np.int(s[0])

    index1 = np.nan
    index2 = np.nan
    index3 = np.nan

    if mod1==1:
        index1 = pos+1
    elif mod1==2:
        index1 = BASE+input[pos+1]
    else:
        index1 = input[pos+1]

    if opcode in [1,2,5,6,7,8]:
        if mod2==1:
            index2 = pos+2
        elif mod2==2:
            index2 = BASE+input[pos+2]
        else:
            index2 = input[pos+2]

    if opcode in [1,2,7,8]:
        if mod3==1:
            index3 = pos+3
        elif mod3==2:
            index3 = BASE+input[pos+3]
        else:
            index3 = input[pos+3]


    if opcode == 1:
        input[index3] = input[index2] + input[index1]
        pos += 4
        return 

    elif opcode == 2:
        input[index3] = input[index2] * input[index1]
        pos += 4
        return 

    elif opcode == 3:
        input[index1] = FLAGS.pop(0)
        pos += 2
        return 

    elif opcode == 4:
        # print(input[index1])
        pos += 2
        return input[index1]
        
    elif opcode == 5:
        if input[index1]:
            pos = input[index2]
            return 
        pos += 3
        return 
        
    elif opcode == 6:
        if not input[index1]:
            pos = input[index2]
            return 
        pos += 3
        return 
        
    elif opcode == 7:
        if input[index1] < input[index2]:
            input[index3] = 1
        else:
            input[index3] = 0
        pos += 4
        return 
        
    elif opcode == 8:
        if input[index1] == input[index2]:
            input[index3] = 1
        else:
            input[index3] = 0
        pos += 4
        return 

    elif opcode == 9:
        BASE += input[index1]
        pos += 2
        return 

    elif opcode == 99:
        print('finished!')
        pos = -1
        return -1
    else:
        raise Exception([pos,opcode])
    




pos = 0
input = np.array(input0,dtype=np.int64)
L = 1000
input = np.append(input,np.zeros(np.int(L),dtype=np.int64))
FLAGS = [0]
BASE = 0

field = np.zeros((200,200),dtype=np.int)
painted = np.zeros((200,200),dtype=np.int)
x = 100
y = 100
field[x,y] = 0
d = [0,1]

while 1:
    # camera
    FLAGS = [field[x,y]]
    r = execute()
    if r is not None:
        if r == -1:
            break
        # first out
        if ~(r == field[x,y]):
            painted[x,y] = 1
            field[x,y] = r

        while 1:
            r = execute()
            if r is not None:
                # second out
                if r == 0:
                    temp = d
                    d = [-temp[1],temp[0]]
                    
                elif r == 1:
                    temp = d
                    d = [temp[1],-temp[0]]

                x += d[0]
                y += d[1]
                break
        

print(len(np.where(painted==1)[0]))

from matplotlib import pyplot as plt
plt.pcolor(field[75:150,90:110].T)
plt.figure()
plt.pcolor(field.T[50:150,50:150])