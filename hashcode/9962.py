def amicable(num):
    a = 0
    for i in range(3, num):
        if num % i == 0:
            a = a + i
    return a
for j in range(1, 500):
    amicable(j)
for k in range(1, 500):
    amicable(k)

print(amicable(j))
print(amicable(k))

if amicable(j) == amicable(k) and j != k:
    print(j, '의 친화수는', k)



