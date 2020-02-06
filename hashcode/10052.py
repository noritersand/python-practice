n=4
m=3
k = {}
a=1
b=0
c=0

while c< m*n:
    for i in range(abs(m)):
        b=b+1
        c=c+1
        k[(a,b)] = c
        if c==m*n:
            break

    for i in range(abs(n-1)):
        a=a+1
        c=c+1
        k[(a,b)] = c
        if c==m*n:
            break

    for i in range(abs(m-1)):
        b=b-1
        c=c+1
        k[(a,b)] = c
        if c==m*n:
            break

    for i in range(abs(n-2)):
        a= a-1
        c=c+1
        k[(a,b)] = c
        if c==m*n:
            break

print(k)