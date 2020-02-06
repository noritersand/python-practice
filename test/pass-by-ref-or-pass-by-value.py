def append(list):
  list.append(1)

list = [0]
append(list)
print(list)

listA = [0]
listB = listA
listB.append(1)
print(listA)