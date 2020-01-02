import numpy as np

#%%
cards = np.arange(10007)

def newstack(cards):
    return cards[::-1]

def cut(cards,N):
    s1 = cards[N:]
    s2 = cards[:N]
    return np.concatenate((s1,s2))

def increment(cards,incr):
    index = np.mod(np.arange(len(cards))*incr,len(cards))
    s = np.argsort(index)
    return cards[s]

with open('22.txt','r') as f:
    for l in f:
        l = l.replace('\n','')
        print(l)
        if l[:9] == 'deal with':
            incr = int(l[20:])
            cards = increment(cards,incr)
        elif l[:9] == 'deal into':
            cards = newstack(cards)
        elif l[:4] == 'cut ':
            N = int(l[4:])
            cards = cut(cards,N)
        else:
            raise Exception(l)

print(np.where(cards==2019)[0])
# 6289

def newstack_index(i):
    return L-1 - i

def cut_index(i,N):
    return (i - N)%L

def increment_index(i,incr):
    return (i*incr) % L

def ic_index(i,N,incr):
    # return (((i - N)%L)*incr) % L
    return (i*incr - N*incr)%L

def ci_index(i,incr,N):
    # return (((i*incr) % L) - N)%L
    return (i*incr - N)%L

def ni_index(i,incr):
    return L - 1 - (i*incr) % L 

def in_index(i,incr):
    return ((L-1 - i)*incr) % L
    # return ((L-1)*incr - i*incr) % L

def ii_index(i,incr1,incr2):
    return (((i*incr1) % L)*incr2) % L

#%%
L = 119315717514047
# L = 10007
# L = 10

def rev_newstack_index(i):
    return L-1 - i

def rev_cut_index(i,N):
    return (i + N)%L

# Python3 program to do modular division 
import math 
  
# Function to find modulo inverse of b. It returns  
# -1 when inverse doesn't  
# modInverse works for prime m 
def modInverse(b,m): 
    g = math.gcd(b, m)  
    if (g != 1): 
        # print("Inverse doesn't exist")  
        return -1
    else:  
        # If b and m are relatively prime,  
        # then modulo inverse is b^(m-2) mode m  
        return pow(b, m - 2, m) 
  
  
# Function to compute a/b under modulo m  
def modDivide(a,b,m): 
    a = a % m 
    inv = modInverse(b,m) 
    if(inv == -1): 
        print("Division not defined") 
    else: 
        print("Result of Division is ",(inv*a) % m)
        return (inv*a) % m

def rev_increment_index(i,incr):
    return modDivide(i,incr,L)

# def rev_increment_index(i,incr):
#     i = int(i)
#     while not (i%incr == 0):
#         i += L

#     return int(i//incr)

shuffles = []
shuffles2 = []
with open('22.txt','r') as f:
    for l in f:
        l = l.replace('\n','')
        # print(l)
        if l[:9] == 'deal with':
            incr = int(l[20:])
            shuffles.append([lambda i, incr: rev_increment_index(i,incr), incr])
            shuffles2.append([lambda i, incr: increment(i,incr), incr])
            del incr
        elif l[:9] == 'deal into':
            shuffles.append([lambda i, x: rev_newstack_index(i), None])
            shuffles2.append([lambda i, x: newstack(i), None])
        elif l[:4] == 'cut ':
            N = int(l[4:])
            shuffles.append([lambda i, N: rev_cut_index(i,N), N])
            shuffles2.append([lambda i, N: cut(i,N), N])
            del N
        else:
            raise Exception(l)
rev_shuffles = shuffles[::-1]

# cards = np.arange(10)
# for s in shuffles2:
#     cards = s[0](cards,s[1])
# print(cards)

# for i in range(10):
#     _i = i
#     for s in rev_shuffles:
#         _i = s[0](_i,s[1])
#     print(_i)

#%%
i = 2020
# i = 6289

for n in range(1000):
    for s in rev_shuffles:
        i = s[0](i,s[1])
    print(i)

# %%
shuffles = []
with open('22.txt','r') as f:
    for l in f:
        l = l.replace('\n','')
        # print(l)
        if l[:9] == 'deal with':
            incr = int(l[20:])
            shuffles.append(['increment', incr])
            del incr
        elif l[:9] == 'deal into':
            shuffles.append(['new stack', 0])
        elif l[:4] == 'cut ':
            N = int(l[4:])
            shuffles.append(['cut', N])
            del N
        else:
            raise Exception(l)

def apply(cards,shuffles):
    for s in shuffles:
        if s[0] == 'new stack':
            cards = newstack(cards)
        elif s[0] == 'cut':
            cards = cut(cards,s[1])
        elif s[0] == 'increment':
            cards = increment(cards,s[1])
        else:
            raise Exception(s)
    return cards

L = 10007
cards = np.arange(L)
cards = apply(cards,shuffles)
print(np.where(cards==2019)[0])

# test 1
# cards = np.arange(L)
# shuffles = [['increment',17],['cut',4*17]]
# cards = apply(cards,shuffles)
# print(cards[:10])

# cards = np.arange(L)
# shuffles = [['cut',4],['increment',17]]
# cards = apply(cards,shuffles)
# print(cards[:10])

# # test 2
# cards = np.arange(L)
# shuffles = [['new stack',0],['increment',17]]
# cards = apply(cards,shuffles)
# print(cards[:10])

# cards = np.arange(L)
# shuffles = [['increment',17],['new stack',0],['cut',16]]
# cards = apply(cards,shuffles)
# print(cards[:10])

# test 3
# cards = np.arange(L)
# shuffles = [['new stack',0],['cut',2]]
# cards = apply(cards,shuffles)
# print(cards[:10])

# cards = np.arange(L)
# shuffles = [['cut',-2],['new stack',0]]
# cards = apply(cards,shuffles)
# print(cards[:10])

# test 4
# cards = np.arange(L)
# shuffles = [['increment',17],['increment',1057]]
# cards = apply(cards,shuffles)
# print(cards[:10])

# cards = np.arange(L)
# shuffles = [['increment',1057*17%L]]
# cards = apply(cards,shuffles)
# print(cards[:10])

L = 119315717514047

def reduce(shuffles):
    while len(shuffles) > 3:
        index = 0
        shuffles2 = []
        while index < len(shuffles):
            if index == len(shuffles)-1:
                shuffles2.append(shuffles[index])
                index += 1
            elif (shuffles[index][0] == 'cut') and (shuffles[index+1][0] == 'increment'):
                j = shuffles[index][1]
                i = shuffles[index+1][1]
                shuffles2.append(['increment',i])
                shuffles2.append(['cut',j*i%L])
                index += 2
            elif (shuffles[index][0] == 'new stack') and (shuffles[index+1][0] == 'increment'):
                i = shuffles[index+1][1]
                shuffles2.append(['increment',i])
                shuffles2.append(['new stack',0])
                if not i-1 == 0:
                    shuffles2.append(['cut',i-1])
                index += 2
            elif (shuffles[index][0] == 'cut') and (shuffles[index+1][0] == 'new stack'):
                shuffles2.append(shuffles[index+1])
                shuffles2.append(['cut',-shuffles[index][1]])
                index += 2
            elif (shuffles[index][0] == 'cut') and (shuffles[index+1][0] == 'cut'):
                j = shuffles[index][1]
                i = shuffles[index+1][1]
                shuffles2.append(['cut',(j+i)%L])
                index += 2
            elif (shuffles[index][0] == 'new stack') and (shuffles[index+1][0] == 'new stack'):
                index += 2
            elif (shuffles[index][0] == 'increment') and (shuffles[index+1][0] == 'increment'):
                j = shuffles[index][1]
                i = shuffles[index+1][1]
                shuffles2.append(['increment',(i*j)%L])
                index += 2
            else:
                if (shuffles[index][0] == 'new stack')  or ~(shuffles[index][1] == 0):
                    shuffles2.append(shuffles[index])
                index += 1

        shuffles = shuffles2.copy()
    return shuffles
        
shuffles0 = shuffles.copy()

# %%
shuffles = shuffles0.copy()
print(bin(101741582076661))
b = '10111001000100010001110110110111100101011110101'
final_shuffles = shuffles.copy()
N = 1

factor = 1
pos = len(b)-1
while factor*2 < 101741582076661:
    shuffles.extend(shuffles)
    shuffles = reduce(shuffles)
    factor *= 2

    pos -= 1
    if b[pos] == '1':
        N += factor
        final_shuffles.extend(shuffles)

final_shuffles = reduce(final_shuffles)
# final_shuffles.insert(0,['cut',-2019])
# final_shuffles.insert(2,['cut',2019*final_shuffles[1][1]%L])

index = 2020
for f in final_shuffles[::-1]:
    if f[0] == 'cut':
        index = rev_cut_index(index,f[1])
    else:
        index = rev_increment_index(index,f[1])
start = index
print('start',start)

# test
for f in final_shuffles:
    if f[0] == 'cut':
        start = cut_index(start,f[1])
    else:
        start = increment_index(start,f[1])
end= start
print('end',end)

# %%
