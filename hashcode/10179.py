def get_generation(x):
    return str((x//10)*10) + '대'

age = int(input('나이를 입력하세요:'))

print(get_generation(age) + "군요")