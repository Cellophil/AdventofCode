import numpy as np
a = 387638
b = 919123

pos = 0
for i in range(a,b+1):
    s = str(i)
    for j in range(1,10):
        if s.find(str(j*11)) > -1:
            if s.find(str(j*111)) == -1:
                break
    else:
        continue

    for j in range(len(s)-1):
        if np.int(s[j+1]) < np.int(s[j]):
            break
    else:
        pos += 1

print(pos)