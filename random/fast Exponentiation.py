


import math
def fastExpon(x,y):
    p = 1
    s = x 
    r = y 
    while r>0:
        if math.floor(r % 2) == 1:
            print(p)
            p = p*s
            print("s:",s)
        #
        s = math.floor(s*s)
        r = math.floor(r/2)
    return p



def fastmodExp(x,y,n):
    p = 1
    s = x 
    r = y 
    while r>0:
        if math.floor(r % 2) == 1:
            print(p)
            p = p*s % n
        #
        s = math.floor(s*s%n)
        r = math.floor(r/2)
    return p





