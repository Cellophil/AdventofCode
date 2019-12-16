import numpy as np

orbit = {}

with open("6.txt","r") as f:
    for i,s in enumerate(f):
        s = s.replace("\n","")
        sp = s.split(")")
        orbit.update({sp[1] : sp[0]})

dist = 0
for o in orbit.keys():
    while o in orbit:
        dist += 1
        o = orbit[o]

print(dist)

total_you = []
o = "YOU"
while o in orbit:
    total_you.append(o)
    o = orbit[o]

total_san = []
o = "SAN"
while o in orbit:
    total_san.append(o)
    if o in total_you:
        break
    o = orbit[o]


print(len(total_san)-1 + total_you.index(total_san[-1]) - 2)