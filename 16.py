import numpy as np
from numba import jit, int64, int16
from matplotlib import pyplot as plt

#%%
@jit(int64[:](int64,int64),nogil=True)
def pattern(N,L):
    # p = np.zeros(np.ceil(L/N)*(N+1))
    # for i in range(np.int(np.ceil(L/N))):
    #     p[i*N-1:(i+1)*N-1] = 

    p = []
    for i in range(N):
        p.append(0)
    for i in range(N):
        p.append(1)
    for i in range(N):
        p.append(0)
    for i in range(N):
        p.append(-1)
    while len(p)-1 < L:
        p = p + p
    p.pop(0)
    return np.array(p,dtype=np.int64)[:L]

@jit(int64[:](int64,int64),nogil=True)
def pattern2(K,L):

    # pki = sum pkj*pji
    # pNi = pattern fct

    pki = np.zeros(L,dtype=np.int64)
    pkj = pattern(K,L)
    for j in range(L):
        pki += pkj[j]*pattern(j+1,L)

    return pki

@jit(int64[:](int64[:],int64),nogil=True)
def phaseit(input,offset=0):
    out = np.zeros(len(input),dtype=np.int64)
    for i in range(len(input)):
        conv = pattern(i+1+offset,len(input))*input
        out[i] += np.abs(np.sum(conv))%10
        
    return out

@jit(int64[:](int64[:]),nogil=True)
def phaseit2(input):
    out = np.zeros(len(input),dtype=np.int64)
    for i in range(len(input)):
        conv = pattern2(i+1,len(input))*input
        out[i] += np.abs(np.sum(conv))%10
        
    return out

def direct(phases,signal):
    L = len(signal)
    out = signal.copy()
    for i in range(L-2,-1,-1):
        out[i] = abs(out[i] + phases*out[i+1])%10

    return out




# def phaseit2(input):
#     global patterns
#     out = np.zeros(len(input),dtype=np.int)
#     for i in range(len(input)):
#         out[i] = abs(np.sum(patterns[i,:]*input))%10
#     return out

input0 = np.array([1,1,1,1,1,1,1,1],np.int64)
input = input0.copy()
print(input)
print('')
input = phaseit(input,0)
print(direct(1,input0))
print(input)
input = phaseit(input,0)
print(direct(2,input0))
print(input)
input = phaseit(input,0)
print(direct(3,input0))
print(input)
input = phaseit(input,0)
print(direct(4,input0))
print(input)
input = phaseit(input,0)
print(direct(5,input0))
print(input)
input = phaseit(input,0)
print(direct(6,input0))
print(input)
input = phaseit(input,0)
print(direct(7,input0))
print(input)
input = phaseit(input,0)
print(direct(8,input0))
print(input)



input = np.array([1,1,1,1,1,1,1,2],np.int64)
inputmatrix = np.zeros((50,8),dtype=np.int64)
inputmatrix[0,:] = input
for i in range(1,50):
    inputmatrix[i,:] = phaseit(inputmatrix[i-1,:],0)

print('')

input = np.array([1,2,3,4,5,6,7,8],np.int64)
input = input[::-1]
print(input)
input = phaseit2(input)
print(input)
input = phaseit2(input)
print(input)
input = phaseit2(input)
print(input)
input = phaseit2(input)
print(input)


input_str = '59717238168580010599012527510943149347930742822899638247083005855483867484356055489419913512721095561655265107745972739464268846374728393507509840854109803718802780543298141398644955506149914796775885246602123746866223528356493012136152974218720542297275145465188153752865061822191530129420866198952553101979463026278788735726652297857883278524565751999458902550203666358043355816162788135488915722989560163456057551268306318085020948544474108340969874943659788076333934419729831896081431886621996610143785624166789772013707177940150230042563041915624525900826097730790562543352690091653041839771125119162154625459654861922989186784414455453132011498'
input = [np.int(s) for s in input_str]
input = np.array(input,np.int64)

for i in range(100):
    input = phaseit(input,0)
print(input[:8])

#%%
# input_str = '03036732577212944063491565474664'
input = [np.int(s) for s in input_str]

offsetnr = input[:7]
offset = np.sum([offsetnr[i]*10**(6-i) for i in range(7)])

signal = []
for i in range(10000):
    signal += input
signal = np.array(signal,np.int64)
signal = signal[offset-1:]

# for i in range(100):
    # print(i)
    # signal = phaseit(signal,offset)

for i in range(100):
    # print(i)
    newsignal = np.cumsum(signal[::-1])[::-1]
    signal = np.mod(newsignal,10)

print(signal[1:9])


# %%
