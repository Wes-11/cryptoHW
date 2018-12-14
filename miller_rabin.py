import math
from random import random, randint
def LSB_one(n):
    #find the least signfigant one bit
    for i in range(0, n):
        if (n>>i) & 1 == 1:
            return i
def miller_rabin(n):
    if n==2 or n==3:
        return True
    a = randint(2, n-1)
    k = LSB_one(n-1)
    q = (n-1)>>k
    x = pow(a,q,n)
    if x == 1 or x==n-1:
        return True
    for j in range(0,k-1):
        x = pow(x,2,n)
        if x == n-1:
            return True
    return False
def is_probably_prime(n,p):
    for i in range(p):
        x = miller_rabin(n)
        if x == False:
            return x
    return ("probability of prime is:",1-(4**-p))

if __name__ == "__main__" :
    print(is_probably_prime(53, 10))

