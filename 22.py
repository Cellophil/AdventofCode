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

#%%
L = 119315717514047
# L = 10007
# L = 10

def rev_newstack_index(i):
    return L-1 - i

def rev_cut_index(i,N):
    return (i + N)%L

def rev_increment_index(i,incr):
    i = int(i)
    while not (i%incr == 0):
        i += L
    return int(i//incr)

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
