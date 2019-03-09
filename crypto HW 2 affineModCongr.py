import math
from pprint import pprint
import operator
root = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p',
        'q','r','s','t','u','v','w','x','y','z']
def mod_inverse(a):
    counter = 0
    state = False
    while state == False:
        d=(counter*a)%26
        if d == 1:
            state = True
            return counter
        counter+=1
def affineE(a,b,t):
    N = []
    e=''
    for i in t:
        c = root.index(i)
        N.append(c)
    for p in N:
        E = (a*p + b)%26
        e += root[E]
    return e
def affineD(a,b,t):
    N = []
    d=''
    for i in t:
        c = root.index(i)
        N.append(c)
    A = mod_inverse(a)
    for c in N:
        D = (A*(c-b))%26
        d += root[D]
    return d
def affine_unknown_key(C, D):
    #finds the key for an affine cipher if
    #there is a sample of cipher text and plain text
    print('encrypting ', D, ' until ', C, ' is found')
    for i in range(26):
        for j in range(26):
          A = affineE(i,j, D)
          if A == C:
              print('alpha is ', i, ' beta is ', j)
def congruency_solver(a,b,m):
    counter = 0
    state = False
    while state == False:
        S = ((a*counter)-b)/m
        if (S).is_integer():
            state = True
            print('solving congruency')
            print('d = ',counter)
        counter+=1
A = affineE(3,1,'secret')
print('secret encrypts to ', A)
HWE = affineE(5, 7, 'howareyou')
print('how are you encrypts to ', HWE)
HWD = affineD(5,7,'qznhobxzd')
print('qznhobxzd decrypts to ',HWD)
F = affine_unknown_key('nonono', 'hahaha')
R = congruency_solver(3, 7, 59)
#Q = congruency_solver(9, 1, 28)
