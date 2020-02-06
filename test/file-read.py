def searching(name):
    code.seek(0, 0)
    lines = code.readlines()
    for line in lines:
        item = line.split()
        if name in item:
            return line

print(searching('4번'))

##print searching('5번')

code.close()

