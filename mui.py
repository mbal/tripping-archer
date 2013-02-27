""" check if is possible to get the string T using the alphabet A
For example: A = [0, 001, 10]
T = 1010 --> yes, using 10 and 10
T = 1001 --> no, we do not have '1'
Unfortunately a greedy approach doesn't work out: if T = 001, a greedy
algorithm would probably fail, since it would match 0, 0, and then it would
stop, because 1 is not in out alphabet. However, it is possible to create T
using A. Sorting A in a reverse order should work.
This game reminds the MIU game in Godel, Escher, Bach (so, a particular kind
of formal logic)."""
import time

def check(T, A):
    if T == '':
        return True
    if T in A:
        return True
    r = True
    for a in A:
        if T[:len(a)] == a:
            r = check(T[len(a):], A)
            if r == True:
                return True
    return False

print(check("010110111", sorted(["0", "01", "010"], key=len, reverse=True)))
