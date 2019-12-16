import numpy as np

input0 = [3,8,1001,8,10,8,105,1,0,0,21,38,55,64,81,106,187,268,349,430,99999,3,9,101,2,9,9,1002,9,2,9,101,5,9,9,4,9,99,3,9,102,2,9,9,101,3,9,9,1002,9,4,9,4,9,99,3,9,102,2,9,9,4,9,99,3,9,1002,9,5,9,1001,9,4,9,102,4,9,9,4,9,99,3,9,102,2,9,9,1001,9,5,9,102,3,9,9,1001,9,4,9,102,5,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,99]
#input0 = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]


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
        index1 = input[pos+1]

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
        print('finished!')
        pos = -1
        return
    else:
        raise Exception(pos)
    


from sympy.utilities.iterables import multiset_permutations
phase = np.arange(5)
solutions = []

for p in multiset_permutations(phase):

    solution = 0
    for i in range(5):
        pos = 0
        input = input0
        FLAGS = [p[i],solution]

        while 1:
            r = execute()
            if r is not None:
                solution = r
                break

    solutions.append(solution)

solutions.sort()
print(solutions[-1])




