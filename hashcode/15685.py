a,b,c = input().split()
a = int(a)
b = int(b)
c = int(c)
global gcd1
global gcd2


def gcd1(a, b):
    while a%b != 0:
        temp = a%b
        a = b
        b = temp
        global gcd1
        return b


print(gcd1(a, b))

def gcd2(gcd1, a, b, c):
    while gcd1(a, b) % c != 0:
        temp = gcd1%c
        gcd1 = c
        c = temp
        global gcd2
        return c 


lcm1 = (a * b) / gcd2(gcd1, a, b, c)
lcm2 = (lcm1 * c) / gcd2(gcd1, a, b, c)
print(gcd2, "%g" %(lcm2))









