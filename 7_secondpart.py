import numpy as np

input0 = [3,8,1001,8,10,8,105,1,0,0,21,38,55,64,81,106,187,268,349,430,99999,3,9,101,2,9,9,1002,9,2,9,101,5,9,9,4,9,99,3,9,102,2,9,9,101,3,9,9,1002,9,4,9,4,9,99,3,9,102,2,9,9,4,9,99,3,9,1002,9,5,9,1001,9,4,9,102,4,9,9,4,9,99,3,9,102,2,9,9,1001,9,5,9,102,3,9,9,1001,9,4,9,102,5,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,99]
#input0 = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
#input0 = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
#input0 = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
#-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
#53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]

def execute():
    global pos, FLAGS
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

    if mod1:   
        index1 = pos+1
    else:
        try:
            index1 = input[pos+1]
        except:
            index1 = np.nan

    if opcode in [1,2,5,6,7,8]:
        if mod2:   
            index2 = pos+2
        else:
            index2 = input[pos+2]
    if opcode in [1,2,7,8]:
        if mod3:   
            index3 = pos+3
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
        #print(input[index1])
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

    elif opcode == 99:
        #print('finished!')
        pos = -1
        return -1
    else:
        raise Exception(pos)
    


from sympy.utilities.iterables import multiset_permutations
phase = np.arange(5)+5
solutions = []

for p in multiset_permutations(phase):

    states = []
    poss = []
    for i in range(5):
        states.append(input0.copy())
        poss.append(0)
    solution = 0

    i = -1
    n = 0
    r = None
    while 1:
        i = (i+1)%5
        n += 1

        input = states[i]
        pos = poss[i]

        if n < 6:
            FLAGS = [p[i],solution]
        else:
            FLAGS = [solution]

        while 1:
            r = execute()
            if r is not None:
                if r == -1:
                    break
                solution = r
                break

        states[i] = input
        poss[i] = pos

        if r == -1:
            break

    solutions.append(solution)
    

solutions.sort()
print(solutions[-1])




