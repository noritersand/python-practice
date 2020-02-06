a=int(input())
d=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

e=[c,c,c,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d,d]

for i in range(a):

    b , c=input().split(' ')
    b=int(b)
    print(b)
    c=int(c)
    print(c)
    e[b-1][c-1]=1
print(e)
