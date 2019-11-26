
from itertools import permutations,combinations
from project.model import Facilities

L = []
perm = permutations([1,2,3,4])
for i in list(perm):
    L.append(i)

for i in list(permutations([1,1,1,2])):
    if  i in L:
        continue
    L.append(i)

for i in list(permutations([1,1,1,3])):
    if  i in L:
        continue
    L.append(i)

for i in list(permutations([1,1,1,4])):
    if  i in L:
        continue
    L.append(i)

for i in list(permutations([2,2,2,1])):
    if  i in L:
        continue
    L.append(i)

for i in list(permutations([2,2,2,3])):
    if  i in L:
        continue
    L.append(i)

for i in list(permutations([2,2,2,4])):
    if  i in L:
        continue
    L.append(i)

for i in list(permutations([3,3,3,1])):
    if  i in L:
        continue
    L.append(i)

for i in list(permutations([3,3,3,2])):
    if  i in L:
        continue
    L.append(i)

for i in list(permutations([3,3,3,4])):
    if  i in L:
        continue
    L.append(i)

L.append((1,1,1,1))
L.append((2,2,2,2))
L.append((3,3,3,3))
L.append((4,4,4,4))


for i in list(permutations([1,2,3,3])):
    if  i in L:
        continue
    L.append(i)

# print(L)
# perm = permutations
# print(L[0][0])
# print(len(L))

