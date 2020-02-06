def coroutine(n):
    print('안녕!')
    yield n * 2

a = coroutine(10)
print(type(a)) # <class 'generator'>

rst = next(a) # print('안녕!')은 이 시점에 실행됨.
print(rst) # 10