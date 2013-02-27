from itertools import permutations

"""abc = 012 = 2+3 = 5
acb = 021 = 1 + 6 = 7
bac = 102 = 2 + 9 = 11
bca = 120 = 6 + 9 = 15 
cab = 201 = 1 + 18 = 19
cba = 210 = 3 + 18 = 21"""

"""aab = 001 = 1
aba = 010 = 2
baa = 100 = 4"""

"""aabb = 0011 = 3
abab = 0101 = 5
abba = 0110 = 6
baab = 1001 = 9
baba = 1010 = 10
bbaa = 1100 = 12"""

"""permutation("aabb") =
    a ++ permutations("abb") = a ++ a ++ permutations("bb")
                               a ++ b ++ permutations("ab")
                      b ++ permutations("aab")
"""


def permutations(stringa):
    if len(stringa) == 1:
        return stringa
    l = []
    c = []
    for i in range(len(stringa)):
        if stringa[i] not in c:
            c.append(stringa[i])
            for p in permutations(stringa[:i] + stringa[i+1:]):
                l.append(stringa[i] + p)
    return l


print permutations("casa")
print (len(permutations('casa')))
